"""Read the anonymous GitHub calendar without changing its daily intensity levels."""
import datetime,json,re,urllib.request
from html.parser import HTMLParser
from pathlib import Path
class CalendarParser(HTMLParser):
 def __init__(self):super().__init__();self.days={};self.ids={};self.counts={};self.tip=None
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='td' and 'data-date' in a and 'data-level' in a:
   d=a['data-date'];self.days[d]=int(a['data-level']);self.ids[a.get('id','')]=d
  if tag=='tool-tip':self.tip=a.get('for')
 def handle_data(self,text):
  if self.tip in self.ids:
   m=re.match(r'\s*(No|[\d,]+) contributions? on ',text)
   if m:self.counts[self.ids[self.tip]]=0 if m[1]=='No' else int(m[1].replace(',',''))
 def handle_endtag(self,tag):
  if tag=='tool-tip':self.tip=None

def parse_calendar(html):
 parser=CalendarParser();parser.feed(html)
 dates=sorted(parser.days)
 if len(dates)<350:raise ValueError('Incomplete GitHub calendar')
 if set(parser.counts)!=set(parser.days):raise ValueError('Missing daily contribution counts')
 if any((parser.counts[d]>0)!=(v>0) for d,v in parser.days.items()):raise ValueError('Contribution count and level disagree')
 if any(not 0<=v<=4 for v in parser.days.values()):raise ValueError('Invalid level')
 for a,b in zip(dates,dates[1:]):
  if (datetime.date.fromisoformat(b)-datetime.date.fromisoformat(a)).days!=1:raise ValueError('Missing calendar day')
 return parser.days,parser.counts

def cell_map(days):
 dates=sorted(days);first=datetime.date.fromisoformat(dates[0]);sunday=first-datetime.timedelta(days=(first.weekday()+1)%7)
 result={d:((datetime.date.fromisoformat(d)-sunday).days//7,(datetime.date.fromisoformat(d).weekday()+1)%7) for d in dates}
 return result,max(x for x,y in result.values())+1

if __name__=='__main__':
 root=Path(__file__).resolve().parents[1];p=root/'assets/public-profile.json';data=json.loads(p.read_text(encoding='utf-8'))
 request=urllib.request.Request('https://github.com/users/efebedelcigil/contributions',headers={'User-Agent':'public-profile-artwork'})
 with urllib.request.urlopen(request,timeout=30) as response:days,counts=parse_calendar(response.read().decode())
 data.update(days=days,day_counts=counts,calendar_fetched=datetime.datetime.now(datetime.timezone.utc).isoformat())
 p.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
