from pathlib import Path
import datetime
import json
import re
import subprocess
import time
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
user = 'efebedelcigil'
MAX_READ_ATTEMPTS = 5
RETRYABLE_HTTP_STATUSES = {408, 429, 500, 502, 503, 504}


def read(url):
    """Fetch GitHub public data, retrying transient network and server errors."""
    for attempt in range(MAX_READ_ATTEMPTS):
        request = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'public-profile-artwork',
                'Accept': 'application/vnd.github+json' if url.startswith('https://api.github.com/') else 'text/html',
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                return response.read().decode('utf-8')
        except urllib.error.HTTPError as error:
            if error.code not in RETRYABLE_HTTP_STATUSES or attempt == MAX_READ_ATTEMPTS - 1:
                raise
            retry_after = error.headers.get('Retry-After')
            try:
                delay = min(max(float(retry_after), 0), 60) if retry_after else 2 ** attempt
            except ValueError:
                delay = 2 ** attempt
            print(f'GitHub returned HTTP {error.code} for {url}; retrying in {delay:g}s '
                  f'({attempt + 1}/{MAX_READ_ATTEMPTS - 1}).', flush=True)
            time.sleep(delay)
        except (urllib.error.URLError, TimeoutError, ConnectionError) as error:
            if attempt == MAX_READ_ATTEMPTS - 1:
                raise
            delay = 2 ** attempt
            print(f'Temporary network error fetching {url}: {error}; retrying in {delay}s '
                  f'({attempt + 1}/{MAX_READ_ATTEMPTS - 1}).', flush=True)
            time.sleep(delay)

    raise RuntimeError(f'Unable to fetch {url} after {MAX_READ_ATTEMPTS} attempts')


page = read(f'https://github.com/users/{user}/contributions')
from public_calendar import parse_calendar
days, day_counts = parse_calendar(page)

repos = []
for page_num in range(1, 20):
    batch = json.loads(read(
        f'https://api.github.com/users/{user}/repos?per_page=100&page={page_num}&type=owner'
    ))
    for repo in batch:
        if not repo.get('private', True):
            repos.append({key: repo[key] for key in (
                'name', 'description', 'html_url', 'language', 'stargazers_count', 'fork'
            )})
    if len(batch) < 100:
        break

profile_html = read(f'https://github.com/{user}')
pinned = []
for block in profile_html.split('pinned-item-list-item-content')[1:]:
    match = re.search(r'href="/([^"?]+/[^"?]+)"[^>]*class="Link', block)
    if match:
        owner, name = match[1].split('/', 1)
        detail = json.loads(read(f'https://api.github.com/repos/{owner}/{name}'))
        if not detail.get('private', True):
            pinned.append({key: detail[key] for key in (
                'name', 'full_name', 'description', 'html_url', 'language',
                'stargazers_count', 'fork'
            )})

for repo in pinned:
    repo['languages'] = json.loads(read(
        f'https://api.github.com/repos/{repo["full_name"]}/languages'
    ))

languages = {}
language_sources = {}
for repo in repos:
    if repo['fork'] or repo['name'] == user:
        continue
    repo_languages = json.loads(read(
        f'https://api.github.com/repos/{user}/{repo["name"]}/languages'
    ))
    language_sources[repo['name']] = repo_languages
    for language, count in repo_languages.items():
        languages[language] = languages.get(language, 0) + count

previous = json.loads((ROOT / 'assets/public-profile.json').read_text(encoding='utf-8'))
activity = previous.get('activity', {})
try:
    query = (ROOT / 'scripts/public-profile.graphql').read_text(encoding='utf-8')
    raw = json.loads(subprocess.check_output(
        ['gh', 'api', 'graphql', '-f', 'query=' + query], text=True
    ))['data']['user']['contributionsCollection']
    activity = {
        label: sum(
            repo['contributions']['totalCount']
            for repo in raw[key]
            if not repo['repository']['isPrivate']
        )
        for label, key in (
            ('Commits', 'commitContributionsByRepository'),
            ('Issues', 'issueContributionsByRepository'),
            ('Pull requests', 'pullRequestContributionsByRepository'),
            ('Reviews', 'pullRequestReviewContributionsByRepository'),
        )
    }
except (subprocess.CalledProcessError, KeyError, FileNotFoundError):
    raise RuntimeError('Public activity refresh failed; retaining previous snapshot and artwork')

snapshot = {
    'fetched': datetime.date.today().isoformat(),
    'source': 'Public calendar, public repository metadata and languages; '
              'contribution types filtered by public repository.',
    'days': days,
    'day_counts': day_counts,
    'calendar_fetched': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'repos': repos,
    'pinned': pinned,
    'languages': languages,
    'language_sources': language_sources,
    'activity': activity,
}
(ROOT / 'assets/public-profile.json').write_text(
    json.dumps(snapshot, indent=2) + '\n', encoding='utf-8'
)
