import unittest,json
from pathlib import Path
from public_activity import public_activity

class ActivityTests(unittest.TestCase):
 def fixture(self):
  raw={key:[{'repository':{'isPrivate':False},'contributions':{'totalCount':count}},{'repository':{'isPrivate':True},'contributions':{'totalCount':999}}] for key,count in [('commitContributionsByRepository',566),('issueContributionsByRepository',5),('pullRequestContributionsByRepository',17),('pullRequestReviewContributionsByRepository',1)]}
  raw['repositoryContributions']={'nodes':[{'repository':{'isPrivate':False}},{'repository':{'isPrivate':True}}],'pageInfo':{'hasNextPage':False,'endCursor':None}}
  return raw
 def test_complete_public_total(self):
  result=public_activity(self.fixture(),lambda cursor:self.fail('Unexpected page'))
  self.assertEqual(result,{'Commits':566,'Issues':5,'Pull requests':17,'Reviews':1,'Repositories':1})
  self.assertEqual(sum(result.values()),590)
 def test_repository_creation_pagination(self):
  raw=self.fixture();raw['repositoryContributions']['pageInfo']={'hasNextPage':True,'endCursor':'next'}
  def more(cursor):
   self.assertEqual(cursor,'next');return {'nodes':[{'repository':{'isPrivate':False}}],'pageInfo':{'hasNextPage':False}}
  self.assertEqual(public_activity(raw,more)['Repositories'],2)
 def test_repeated_cursor_rejected(self):
  raw=self.fixture();page=raw['repositoryContributions'];page['pageInfo']={'hasNextPage':True,'endCursor':'loop'}
  with self.assertRaises(ValueError):public_activity(raw,lambda cursor:page)
 def test_published_snapshot_totals_match(self):
  data=json.loads((Path(__file__).resolve().parents[1]/'assets/public-profile.json').read_text(encoding='utf-8'))
  self.assertEqual(sum(data['activity'].values()),sum(data['day_counts'].values()))

if __name__=='__main__':unittest.main()
