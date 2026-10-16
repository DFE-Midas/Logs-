#!/usr/bin/env python3
"""Check published listing values; do not silently change the shop."""
from pathlib import Path
from html.parser import HTMLParser
import json,re,urllib.request,concurrent.futures
root=Path(__file__).resolve().parent.parent
products=json.loads((root/'assets/products.js').read_text().split('=',1)[1].strip().removesuffix(';'))
class Links(HTMLParser):
 def __init__(self):super().__init__();self.current=None;self.rows=[]
 def handle_starttag(self,t,a):
  if t=='a':self.current=[dict(a).get('href',''),[]]
 def handle_data(self,d):
  if self.current is not None:self.current[1].append(d)
 def handle_endtag(self,t):
  if t=='a' and self.current is not None:self.rows.append((self.current[0],''.join(self.current[1])));self.current=None
url='https://www.altrinchamlogs.com/?products=all'
s=urllib.request.urlopen(url,timeout=40).read().decode();parser=Links();parser.feed(s)
rows={href.rstrip('/').split('/')[-1]:text for href,text in parser.rows if '£' in text}
# Fetch the three additional live product pages once each.
extra_urls=sorted({p['source'] for p in products if 'altrinchamlogs.co.uk/' in p['source']})
def fetch_extra(url):
 try:
  raw=urllib.request.urlopen(url,timeout=40).read().decode()
  raw=re.sub(r'<(?:script|style)\b[^>]*>.*?</(?:script|style)>',' ',raw,flags=re.S|re.I)
  return url,re.sub(r'\s+',' ',re.sub('<[^>]+>',' ',raw))
 except Exception:return url,''
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:extra=dict(pool.map(fetch_extra,extra_urls))
patterns={'p16':r'30\s*L\s+NET OF KILN DRIED PREMIUM ASH LOGS\s*£\s*(\d+(?:\.\s*\d{2})?)','p17':r'BULK BAG BARN DRIED LOGS\s*£\s*(\d+(?:\.\s*\d{2})?)','p18':r'Premium Smokeless coal 20\s*Kg\s*£\s*(\d+(?:\.\s*\d{2})?)'}
failed=False
for p in products:
 if 'altrinchamlogs.com/' in p['source']:
  title=rows.get(p['source'].rstrip('/').split('/')[-1],'')
  values=re.findall(r'£\s*(\d+(?:\.\s*\d{2})?)',title)
  current=round(float(values[-1].replace(' ',''))*100) if values else None
  ok=current==p['price'];failed|=not ok
  print(('MATCH' if ok else 'REVIEW'),p['name'],p['unit'],'build £%.2f'%(p['price']/100),'live '+('£%.2f'%(current/100) if current is not None else 'not found'))
 else:
  m=re.search(patterns[p['id']],extra[p['source']],re.I)
  current=round(float(m[1].replace(' ',''))*100) if m else None
  ok=current==p['price'];failed|=not ok
  print(('MATCH' if ok else 'REVIEW'),p['name'],p['unit'],'build £%.2f'%(p['price']/100),'live '+('£%.2f'%(current/100) if current is not None else 'not found'))
print('Supplier confirmation is required for availability, delivery and the final selling price.')
raise SystemExit(1 if failed else 0)
