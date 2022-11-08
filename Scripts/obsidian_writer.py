from collections import defaultdict
from glob import glob
import os
from os import path
import re

from webtoons_out import main_strips, extra_strips

TALE_SECTION_ORDER = ('Synopsis', 'Interpretation', 'Caption', 'Hidden Item',  'Characters', 'External Links')
TALE_REQUIRED_SECTIONS = ('Synopsis', 'Caption', 'Characters', 'External Links')

filenames = glob('../Tale *.md')

def find_tale_filename(tale_number):
    for fn in filenames:
        if re.match(f'../Tale {tale_number}\\b', fn):
            return fn

def get_heading(line):
    assert line.startswith('# ')
    return line[2:].strip()

def parse_sections(tale_lines):
    sections = {}
    section_name = get_heading(tale_lines[0])
    for l in tale_lines:
        if l.startswith('# '):
            section_name = get_heading(l)
            sections[section_name] = []
            continue
        sections[section_name].append(l)
    return sections
    
def update_caption(sections, caption):
    if not caption:
        return
        
    caption = caption.strip().replace('\r', '')
    sections['Caption'] = []
    for c in caption.split('\n'):
        sections['Caption'].append('> ' + c + '\n')
    sections['Caption'].append('\n')

def update_webtoons_external_link(sections, url):
    links = sections['External Links']
    
    def _update_webtoons_link(l):
        if 'Webtoons' not in l:
            return l
        if '()' not in l:
            return l
        return l.replace('()', f'({url})')
    
    sections['External Links'][:] = [_update_webtoons_link(l) for l in links]
   
def write_tale_sections(tale_filename, sections):
    with open(tale_filename, 'w') as f:
        for section_name in TALE_SECTION_ORDER:
            if section_name not in sections:
                continue
            section = sections[section_name]
            f.write(f'# {section_name}\n')
            f.writelines(section)

def update_sections_from_webtoons():
    for (tale_number, title, url, info) in main_strips:
        tale_filename = find_tale_filename(tale_number)
        print(tale_filename)
        with open(tale_filename, 'r') as f:
            tale_lines = list(f.readlines())
        sections = parse_sections(tale_lines)
        update_caption(sections, info)
        update_webtoons_external_link(sections, url)
        write_tale_sections(tale_filename, sections)
 
def rename_with_titles():
    for (tale_number, title, info) in main_strips:
        tale_filename = find_tale_filename(tale_number)
        title = title.replace('?', ' QM')
        new_filename = path.join(path.dirname(tale_filename), f'Tale {tale_number} - {title}.md')
        os.rename(tale_filename, new_filename)

def count_character_stats():
    char_tales = defaultdict(set)
    char_re = re.compile(r'\* \[\[(.+)\]\]')
    
    for tale_number in range(1, 121):
        tale_filename = find_tale_filename(tale_number)
        with open(tale_filename, 'r') as f:
            tale_lines = list(f.readlines())
        sections = parse_sections(tale_lines)
        for l in sections['Characters']:
            m = char_re.match(l)
            if m:
                char_tales[m[1]].add(tale_number)
    
    counts = {char: len(s) for char, s in char_tales.items()}
    print(sorted(counts.items(), reverse=True, key=lambda i: i[1]))
    
count_character_stats()