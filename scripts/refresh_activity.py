import argparse
import datetime
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen


class Calendar(HTMLParser):
    def __init__(self):
        super().__init__()
        self.days = []

    def handle_starttag(self, tag, attributes):
        values = dict(attributes)
        if 'data-date' in values and 'data-level' in values:
            self.days.append({'date': values['data-date'], 'level': int(values['data-level'])})


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--user', default='efebedelcigil')
    args = parser.parse_args()
    if not args.user.replace('-', '').isalnum():
        parser.error('Use a GitHub username.')
    url = f'https://github.com/users/{args.user}/contributions'
    calendar = Calendar()
    request = Request(url, headers={'User-Agent': 'profile-workbench'})
    with urlopen(request, timeout=30) as response:
        calendar.feed(response.read().decode('utf-8'))
    today = datetime.datetime.now(datetime.timezone.utc).date().isoformat()
    days = sorted((day for day in calendar.days if day['date'] <= today), key=lambda day: day['date'])[-28:]
    if len(days) != 28 or len({day['date'] for day in days}) != 28 or any(not 0 <= day['level'] <= 4 for day in days):
        raise RuntimeError('Contribution calendar did not contain 28 valid days; existing data was kept.')
    target = Path(__file__).resolve().parents[1] / 'assets/workbench-data.json'
    target.write_text(json.dumps({'source': url, 'updated': today, 'days': days}, indent=2)+'\n', encoding='utf-8')
    print(f'Updated 28 public calendar days through {days[-1]["date"]}.')


if __name__ == '__main__':
    main()
