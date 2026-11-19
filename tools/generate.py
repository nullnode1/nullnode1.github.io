#!/usr/bin/env python3
"""Markdown -> statik SEO sayfaları, arama indeksi, sitemap.xml, robots.txt ve RSS."""
import html
import json
import re
import shutil
import subprocess
from datetime import date, datetime, time, timezone
from email.utils import format_datetime
from pathlib import Path
from urllib.parse import quote, urlsplit
from xml.etree import ElementTree as ET
import markdown

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / 'dist'
BASE = 'https://nullnode1.github.io'
EXCLUDE = {'.git', '.github', 'tools', 'dist', '.venv', 'venv', 'node_modules', '__pycache__'}
MONTHS = dict(zip('ocak şubat mart nisan mayıs haziran temmuz ağustos eylül ekim kasım aralık'.split(), range(1, 13)))


def git_modified(path):
    p = subprocess.run(['git', 'log', '-1', '--format=%cI', '--', str(path.relative_to(ROOT))], cwd=ROOT, capture_output=True, text=True)
    try:
        return datetime.fromisoformat(p.stdout.strip()).astimezone(timezone.utc)
    except ValueError:
        return None


def publish_date(slug, source, modified):
    ymd = re.match(r'^(\d{4})[.-](\d{2})[.-](\d{2})[-_. ]', slug)
    dmy = re.match(r'^(\d{2})[.-](\d{2})[.-](\d{4})[-_. ]', slug)
    if ymd or dmy:
        try:
            y, m, d = map(int, ymd.groups()) if ymd else (int(dmy[3]), int(dmy[2]), int(dmy[1]))
            return datetime.combine(date(y, m, d), time(12, 0), timezone.utc)
        except ValueError:
            pass
    m = re.search(r'^\s*[*_]?\s*(\d{1,2})\s+([a-zA-ZçğıöşüÇĞİÖŞÜ]+)\s+(\d{4})\s*[*_]?\s*$', source, re.M)
    if m and m[2].lower() in MONTHS:
        try:
            return datetime(int(m[3]), MONTHS[m[2].lower()], int(m[1]), 12, tzinfo=timezone.utc)
        except ValueError:
            pass
    return modified or datetime.now(timezone.utc)


def clean(s):
    s = re.sub(r'!?\[([^]]+)\]\([^)]+\)', r'\1', s)
    return html.unescape(re.sub(r'<[^>]+>|[*_`~]+', '', s)).strip()


def details(source, slug):
    m = re.search(r'^#\s+(.+)$', source, re.M)
    title = clean(m[1]) if m else clean(slug.replace('-', ' ').replace('_', ' '))
    description = title
    for block in re.split(r'\n\s*\n', source):
        block = block.strip()
        if (not block or block.startswith(('#', '```', '~~~', '|', '<', '- ', '* '))
                or re.fullmatch(r'[*_]\d{1,2}\s+\w+\s+\d{4}[*_]', block)):
            continue
        paragraph = clean(re.sub(r'\s+', ' ', block))
        if len(paragraph) > 20:
            description = paragraph[:220]
            break
    return title, description


def render(source):
    content = markdown.markdown(source, extensions=['fenced_code', 'tables', 'sane_lists'])
    # Göreli görsel adresleri, kaynak Markdown dosyasının konumuna göre ayarla.
    def fix(m):
        name, q, value = m.groups()
        parts = urlsplit(html.unescape(value))
        if parts.scheme or parts.netloc or value.startswith(('/', '#', '//')):
            return m[0]
        if name.lower() == 'href' and parts.path.lower().endswith('.md'):
            dest = '/#/posts/' + quote(Path(parts.path).stem, safe='')
        else:
            from posixpath import normpath
            dest = '/' + quote(normpath('posts/' + parts.path), safe='/-_.~')
        if parts.query:
            dest += '?' + parts.query
        if parts.fragment:
            dest += '#' + parts.fragment
        return name + '=' + q + html.escape(dest, quote=True) + q
    return re.sub(r'\b(src|href)=(\"|\')(.*?)\2', fix, content, flags=re.I | re.S)


def page(title, description, markup, url):
    title_e = html.escape(title, quote=True)
    desc_e = html.escape(description, quote=True)
    url_e = html.escape(url, quote=True)
    return f'''<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{desc_e}"><meta name="robots" content="index,follow">
<link rel="canonical" href="{url_e}"><link rel="icon" href="/favicon.ico">
<link rel="alternate" type="application/rss+xml" title="nullnode1 Blog" href="/rss.xml">
<link rel="stylesheet" href="/assets/blog.css">
<meta property="og:title" content="{title_e}"><meta property="og:description" content="{desc_e}">
<meta property="og:url" content="{url_e}"><meta property="og:type" content="article">
<title>{title_e} — nullnode1</title>
<style>
body {{ display: flex !important; flex-direction: column !important; min-height: 100vh !important; }}
main.static-main {{ flex: 1 0 auto !important; width: 100% !important; position: static !important; }}
.site-footer {{ margin-top: auto !important; }}
</style>
</head>
<body>
<header class="site-header"><div class="shell header-inner">
<a class="site-title" href="/#/">nullnode1<span aria-hidden="true">.</span></a>
<nav class="site-nav" aria-label="Ana menü"><a href="/#/">Yazılar</a><a href="/#/hakkimda">Hakkımda</a><a href="https://github.com/nullnode1" target="_blank" rel="noopener noreferrer">GitHub</a></nav>
</div></header>
<main class="static-main"><article class="markdown-section">{markup}</article></main>
<footer class="site-footer"><div class="shell footer-inner"><span>© 2026 · Kişisel notlar</span><span><a href="/rss.xml">RSS</a> · Markdown ile hazırlandı.</span></div></footer>
</body></html>
'''


def xml_output(root, filename):
    (DIST / filename).write_text('<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(root, encoding='unicode') + '\n', encoding='utf-8')


def main():
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()
    # İş akışı kaynak kodunu ve geçmişi yayımlama, site dosyalarını koru.
    for source in ROOT.rglob('*'):
        if source.is_symlink() or not source.is_file():
            continue
        path = source.relative_to(ROOT)
        if path.parts[0] in EXCLUDE or source.suffix.lower() == '.zip':
            continue
        target = DIST / path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    (DIST / '.nojekyll').touch()

    posts = []
    for path in sorted((ROOT / 'posts').glob('*.md')) if (ROOT / 'posts').is_dir() else []:
        slug = path.stem
        source = path.read_text(encoding='utf-8-sig')
        title, desc = details(source, slug)
        modified = git_modified(path)
        published = publish_date(slug, source, modified)
        url = BASE + '/yazi/' + quote(slug, safe='-_.~') + '/'
        rendered = render(source)
        html_path = DIST / 'yazi' / slug / 'index.html'
        html_path.parent.mkdir(parents=True, exist_ok=True)
        html_path.write_text(page(title, desc, rendered, url), encoding='utf-8')
        posts.append(dict(slug=slug, title=title, excerpt=desc, text=source, date=published.date().isoformat(),
                          published=published, modified=modified or published, url=url, rendered=rendered))
    posts.sort(key=lambda x: (x['published'], x['slug']), reverse=True)
    (DIST / 'search-index.json').write_text(json.dumps([
        {k: p[k] for k in ('slug', 'title', 'excerpt', 'text', 'date')} for p in posts
    ], ensure_ascii=False, separators=(',', ':')), encoding='utf-8')

    sitemap_ns = 'http://www.sitemaps.org/schemas/sitemap/0.9'
    ET.register_namespace('', sitemap_ns)
    sitemap = ET.Element('{' + sitemap_ns + '}urlset')
    urls = [(BASE + '/', None)]
    if (ROOT / 'hakkimda.md').is_file():
        about_source = (ROOT / 'hakkimda.md').read_text(encoding='utf-8')
        title, description = details(about_source, 'hakkimda')
        dest = DIST / 'hakkimda' / 'index.html'
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(page(title, description, markdown.markdown(about_source), BASE + '/hakkimda/'), encoding='utf-8')
        urls.append((BASE + '/hakkimda/', git_modified(ROOT / 'hakkimda.md')))
    urls.extend((p['url'], p['modified']) for p in posts)
    for url, lastmod in urls:
        row = ET.SubElement(sitemap, '{' + sitemap_ns + '}url')
        ET.SubElement(row, '{' + sitemap_ns + '}loc').text = url
        if lastmod:
            ET.SubElement(row, '{' + sitemap_ns + '}lastmod').text = lastmod.date().isoformat()
    xml_output(sitemap, 'sitemap.xml')

    content_ns = 'http://purl.org/rss/1.0/modules/content/'
    ET.register_namespace('content', content_ns)
    rss = ET.Element('rss', {'version': '2.0'})
    channel = ET.SubElement(rss, 'channel')
    for tag, value in [('title', 'nullnode1 — Blog'), ('link', BASE + '/'),
                       ('description', 'Açık kaynak, yazılım ve kişisel notlar.'), ('language', 'tr-TR'),
                       ('lastBuildDate', format_datetime(datetime.now(timezone.utc))), ('ttl', '60')]:
        ET.SubElement(channel, tag).text = value
    for p in posts[:50]:
        item = ET.SubElement(channel, 'item')
        for tag, value in [('title', p['title']), ('link', p['url']),
                           ('description', p['excerpt']), ('pubDate', format_datetime(p['published']))]:
            ET.SubElement(item, tag).text = value
        ET.SubElement(item, 'guid', {'isPermaLink': 'true'}).text = p['url']
        ET.SubElement(item, '{' + content_ns + '}encoded').text = p['rendered']
    xml_output(rss, 'rss.xml')
    (DIST / 'robots.txt').write_text('User-agent: *\nAllow: /\n\nSitemap: ' + BASE + '/sitemap.xml\n', encoding='utf-8')
    print(f'{len(posts)} yazı, XML dosyaları, arama indeksi ve SEO sayfaları hazırlandı.')


if __name__ == '__main__':
    main()
