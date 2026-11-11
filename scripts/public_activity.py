"""Count public contribution types, including repository creation."""
import json,subprocess

def graphql(query):
 return json.loads(subprocess.check_output(['gh','api','graphql','-f','query='+query],text=True))['data']['user']['contributionsCollection']

def public_activity(raw,more):
 activity={label:sum(repo['contributions']['totalCount'] for repo in raw[key] if not repo['repository']['isPrivate']) for label,key in [('Commits','commitContributionsByRepository'),('Issues','issueContributionsByRepository'),('Pull requests','pullRequestContributionsByRepository'),('Reviews','pullRequestReviewContributionsByRepository')]}
 page=raw['repositoryContributions'];created=0;seen=set()
 while True:
  created+=sum(not node['repository']['isPrivate'] for node in page['nodes'])
  if not page['pageInfo']['hasNextPage']:break
  cursor=page['pageInfo']['endCursor']
  if not cursor or cursor in seen:raise ValueError('Invalid repository contribution pagination')
  seen.add(cursor);page=more(cursor)
 activity['Repositories']=created
 return activity

def repository_page(cursor):
 query='query {user(login:"efebedelcigil") {contributionsCollection {repositoryContributions(first:100,after:'+json.dumps(cursor)+') {nodes {repository {isPrivate}} pageInfo {hasNextPage endCursor}}}}}'
 return graphql(query)['repositoryContributions']
