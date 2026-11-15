"""Check API authentication boundaries without live network requests."""
import ast,os,time,urllib.request,urllib.error,unittest
from pathlib import Path
from unittest.mock import patch
source=ast.parse(Path(__file__).with_name('refresh_public_profile.py').read_text())
function=next(n for n in source.body if isinstance(n,ast.FunctionDef) and n.name=='read')
namespace={'os':os,'urllib':urllib,'time':time,'MAX_READ_ATTEMPTS':5,'RETRYABLE_HTTP_STATUSES':{408,429,500,502,503,504}}
exec(compile(ast.Module(body=[function],type_ignores=[]),'refresh_public_profile.py','exec'),namespace)
class TransportTests(unittest.TestCase):
 def request(self,url,token='test-public-token'):
  seen=[]
  class Response:
   def __enter__(self):return self
   def __exit__(self,*args):pass
   def read(self):return b'{}'
  def open_request(req,**kwargs):seen.append(req);return Response()
  with patch.dict(os.environ,{'GH_TOKEN':token},clear=True),patch('urllib.request.urlopen',open_request):namespace['read'](url)
  return seen[0]
 def test_public_api_uses_workflow_token(self):
  self.assertEqual(self.request('https://api.github.com/users/example/repos').get_header('Authorization'),'Bearer test-public-token')
 def test_other_hosts_receive_no_token(self):
  for url in ['https://github.com/example','https://api.github.com.evil.invalid/','http://api.github.com/users/example']:
   self.assertIsNone(self.request(url).get_header('Authorization'))
 def test_no_token_keeps_anonymous_request(self):
  self.assertIsNone(self.request('https://api.github.com/users/example/repos','').get_header('Authorization'))
if __name__=='__main__':unittest.main()
