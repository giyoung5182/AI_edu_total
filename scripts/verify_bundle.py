"""Validate public bundle syntax and static local links (no network requests)."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import ast,json,re
ROOT=Path(__file__).resolve().parents[1]
class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[]
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if tag in {'a','link','img','script','video','source','iframe'}:
   for key in ('href','src'):
    if d.get(key):self.links.append(d[key])
def main():
 errors=[];counts={'files':0,'json':0,'python':0,'static_local_links':0}
 for p in sorted(ROOT.rglob('*')):
  if not p.is_file() or any(x in {'.git','__pycache__','node_modules','test-output'} for x in p.relative_to(ROOT).parts):continue
  counts['files']+=1;ext=p.suffix.lower()
  if ext not in {'.html','.md','.json','.py'}:continue
  try:t=p.read_text(encoding='utf-8-sig')
  except UnicodeError:errors.append({'file':str(p.relative_to(ROOT)),'error':'not UTF-8'});continue
  try:
   if ext=='.json':json.loads(t);counts['json']+=1
   if ext=='.py':ast.parse(t);counts['python']+=1
  except (ValueError,SyntaxError) as e:errors.append({'file':str(p.relative_to(ROOT)),'error':str(e)})
  links=[]
  if ext=='.html':parser=Links();parser.feed(t);links=parser.links
  if ext=='.md':links=re.findall(r'\[[^\]]*\]\(([^)]+)\)',t)
  for link in links:
   # Skip dynamic snippets and explanatory API/sample paths.
   if not link or link.startswith(('#','/')) or '${' in link or '__' in link or '<' in link:continue
   parsed=urlsplit(link)
   if parsed.scheme or parsed.netloc:continue
   path=unquote(parsed.path.strip('<>'))
   if not path:continue
   counts['static_local_links']+=1
   if not (p.parent/path).exists():errors.append({'file':str(p.relative_to(ROOT)),'error':'missing local link','target':path})
 result={'scope':'UTF-8, JSON, Python syntax, static local file links only','counts':counts,'errors':errors,'ok':not errors}
 print(json.dumps(result,ensure_ascii=False,indent=2))
 return 0 if not errors else 1
if __name__=='__main__':raise SystemExit(main())
