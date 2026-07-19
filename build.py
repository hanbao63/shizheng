#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build.py - Scan directory and regenerate index.html"""
import os, json, re
ROOT = os.path.dirname(os.path.abspath(__file__))
def get_top_dirs():
    """自动检测根目录下包含 PDF 的所有大类文件夹"""
    dirs = []
    for item in sorted(os.listdir(ROOT)):
        dp = os.path.join(ROOT, item)
        if not os.path.isdir(dp) or item.startswith('.'):
            continue
        has_pdf = False
        for r, _, files in os.walk(dp):
            if any(f.endswith('.pdf') for f in files):
                has_pdf = True
                break
        if has_pdf:
            dirs.append(item)
    return dirs

def date_key(f):
    m = re.search(r'(\d{4})年(\d{1,2})月(\d{1,2})日', f)
    if m: return int(m.group(1))*10000+int(m.group(2))*100+int(m.group(3))
    m = re.search(r'(\d{4})年(\d{1,2})月', f)
    if m: return int(m.group(1))*10000+int(m.group(2))*100
    return 0
def build_tree():
    top_dirs = get_top_dirs()
    tree = {'name': '时政汇总', 'children': []}
    for d in top_dirs:
        dp = os.path.join(ROOT, d)
        if not os.path.isdir(dp): continue
        node = {'n': d, 'c': []}
        for item in sorted(os.listdir(dp)):
            ip = os.path.join(dp, item)
            rp = os.path.join(d, item)
            if os.path.isdir(ip):
                files = [f for f in os.listdir(ip) if f.endswith('.pdf')]
                if not files: continue
                files.sort(key=date_key)
                subs = [{'n': f, 'p': os.path.join(d, item, f)} for f in files]
                node['c'].append({'n': item, 'c': subs})
            elif item.endswith('.pdf'):
                node['c'].append({'n': item, 'p': rp})
        tree['children'].append(node)
    return tree
def count_files(n):
    if n.get('c'): return sum(count_files(c) for c in n['c'])
    return 1
def main():
    tree = build_tree()
    tree_json = json.dumps(tree, ensure_ascii=False, separators=(',', ':'))
    total = sum(count_files(c) for c in tree['children'])
    html_path = os.path.join(ROOT, 'index.html')
    with open(html_path, 'r', encoding='utf-8') as f: html = f.read()
    s = 'var TREE = ' + tree_json + ';\n\nvar total = ' + str(total) + ';'
    html = re.sub(r'var TREE = .+?;\s*var total = \d+;', s, html, count=1, flags=re.DOTALL)
    html = re.sub(r'<span id="total">\d+</span>', '<span id="total">' + str(total) + '</span>', html)
    with open(html_path, 'w', encoding='utf-8') as f: f.write(html)
    print('Updated: ' + str(total) + ' PDFs')
    for c in tree['children']: print('  ' + c['n'] + ': ' + str(count_files(c)))
if __name__ == '__main__': main()
