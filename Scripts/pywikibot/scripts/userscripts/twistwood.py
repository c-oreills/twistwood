from glob import glob
from os import path
import re

import pywikibot

site = pywikibot.Site()

def upload_file(filename, edit_message):
    pagename = path.basename(filename)[:-3].replace(" ", "_").replace("_QM", "?")
    
    text = convert_obsidian_to_mediawiki(filename)
    print(text)
    
    page = pywikibot.Page(site, pagename)
    if page.text == text:
        return
    
    page.text = text
    page.save('Initial Tales upload')

def convert_obsidian_to_mediawiki(filename):
    with open(filename) as f:
        lines = list(f.readlines())
    
    def _convert_line(l):
        l = _convert_heading(l)
        l = _convert_quote(l)
        l = _convert_citation(l)
        l = _convert_ext_link(l)
        return l
    
    text = ''.join(_convert_line(l) for l in lines).strip()
    # Remove Table of Contents
    text = "__NOTOC__\n" + text
    
    if path.basename(filename).startswith('Tale '):
        text += "\n\n[[Category:Tale]]"
    
    return text

def _convert_heading(l):
    if not (m:= re.match(r'(#+) (.*)$', l)):
        return l
    head_depth = len(m[1])
    # 1 deeper due to MediaWiki reserving H1 for page titles
    new_head = '=' * (head_depth + 1)
    
    heading = m[2]
    
    return f'{new_head} {heading} {new_head}\n'

def _convert_quote(l):
    if not l.startswith('> '):
        return l
    l = l[2:].strip()
    return f'{{{{Quote|{l}}}}}\n'

def _convert_citation(l):
    if not (m := re.search(r'\^\[', l)):
        return l
    
    s = m.start()
    d = 0
    for i, c in enumerate(l[s+1:]):
        if c == '[': d += 1
        if c == ']': d -= 1
        if d == 0:
            return l[:s] + '<ref>' + l[s+2:s+i+1] + '</ref>' + _convert_citation(l[s+i+2:])
    assert False, "Unmatched []s"

def _convert_ext_link(l):
    return re.sub(r'\[([^]]*)\]\(([^)]*)\)', r'[\2 \1]', l)

#msg = input()
for filename in glob("../../Tale *.md"):
    upload_file(filename, "")