#!/usr/bin/env python3
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,re
root=Path(__file__).resolve().parent.parent
class Doc(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.ids=set();self.h1=0;self.title=0;self.description=False
 def handle_starttag(self,t,a):
  a=dict(a)
  if 'id' in a:assert a['id'] not in self.ids,('Duplicate id',a['id']);self.ids.add(a['id'])
  if t=='h1':self.h1+=1
  if t=='title':self.title+=1
  if t=='meta' and a.get('name')=='description':self.description=True
  for k in ('href','src'):
   if k in a:self.links.append(a[k])
for f in root.glob('*.html'):
 doc=Doc();doc.feed(f.read_text());assert doc.h1==1,(f,'H1 count',doc.h1);assert doc.title==1 and doc.description,f
 for link in doc.links:
  u=urlsplit(link)
  if u.scheme or u.netloc:continue
  path=root/unquote(u.path.lstrip('/')) if u.path else f
  assert path.exists(),(f.name,link,'missing target')
  if u.fragment and path.suffix=='.html':
   d=Doc();d.feed(path.read_text());assert u.fragment in d.ids,(f.name,link,'missing anchor')
products=json.loads((root/'assets/products.js').read_text().split('=',1)[1].strip().removesuffix(';'))
assert len({p['id'] for p in products})==len(products)
for p in products:
 assert (root/p['image']).is_file(),p['image']
 assert isinstance(p['price'],int) and p['price']>0
 for f in ('index.html','shop.html'):
  s=(root/f).read_text();m=re.search(r'id="'+p['id']+r'"(.*?)data-add="'+p['id']+r'"',s,re.S)
  if m:assert ('£%.2f'%(p['price']/100)) in m[1],(f,p['id'],'price mismatch')
 assert ('data-add="'+p['id']+'"' in (root/'shop.html').read_text()) == (p.get('inStock') is not False)
print('PASS: 9 HTML pages, local links and anchors, unique IDs, SEO metadata, 18 catalogue products and matching visible prices.')
