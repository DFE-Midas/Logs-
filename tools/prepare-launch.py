#!/usr/bin/env python3
"""Apply final-domain SEO after reviewing the deployment and supplier's price list."""
from pathlib import Path
import argparse,re,html
from urllib.parse import urlsplit
p=argparse.ArgumentParser();p.add_argument('site_url');a=p.parse_args()
u=urlsplit(a.site_url)
if u.scheme!='https' or not u.netloc or u.path not in ('','/') or u.query or u.fragment or u.username or u.password:p.error('Use the final https:// domain without a path, query, or credentials.')
base=a.site_url.rstrip('/');root=Path(__file__).resolve().parent.parent
public=['index','shop','delivery','about','contact','privacy']
for f in root.glob('*.html'):
 s=f.read_text();s=re.sub(r'<link rel="canonical"[^>]*>','',s);s=re.sub(r'<meta property="og:(?:url|image)"[^>]*>','',s)
 if f.stem in public:
  s=s.replace('<meta name="robots" content="noindex,nofollow">','<meta name="robots" content="index,follow">')
  url=base+('/' if f.stem=='index' else '/'+f.name)
  tags=f'<link rel="canonical" href="{html.escape(url,quote=True)}"><meta property="og:url" content="{html.escape(url,quote=True)}"><meta property="og:image" content="{html.escape(base,quote=True)}/assets/hearth.webp">'
  s=s.replace('</head>',tags+'</head>')
 f.write_text(s)
config=root/'netlify.toml';config.write_text(config.read_text().replace('    X-Robots-Tag = "noindex, nofollow"\n',''))
(root/'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {base}/sitemap.xml\n')
urls=[base+('/' if slug=='index' else '/'+slug+'.html') for slug in public]
(root/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+html.escape(url)+'</loc></url>' for url in urls)+'</urlset>\n')
print('SEO configured for',base,'— redeploy the folder to apply it.')
