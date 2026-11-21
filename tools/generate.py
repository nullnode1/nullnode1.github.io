#!/usr/bin/env python3
"""posts/*.md -> statik site (ana sayfa, yazılar, hakkımda), arama indeksi,
sitemap.xml, rss.xml ve robots.txt. Çıktı dist/ klasörüne yazılır."""
import hashlib
import html
import json
import re
import shutil
import subprocess
from datetime import date, datetime, time, timezone
from email.utils import format_datetime
from pathlib import Path
from posixpath import normpath
from urllib.parse import quote, urlsplit
from xml.etree import ElementTree as ET
import markdown

# ---- Ayarlar -----------------------------------------------------------
BASE = 'https://nullnode1.github.io'
SITE = 'nullnode1'
TAGLINE = 'Yazılım geliştirme, açık kaynak ve kişisel notlarım.'
DESCRIPTION = 'Açık kaynak, yazılım ve kişisel notlar.'
GITHUB = 'https://github.com/nullnode1'
EMAIL = ''  # Örn: 'ornek@mail.com' yaz, üst menüye "E-posta" bağlantısı eklenir.
# ------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / 'dist'
EXCLUDE = {'.git', '.github', 'tools', 'dist', '.venv', 'venv', 'node_modules', '__pycache__'}
MONTHS = dict(zip('ocak şubat mart nisan mayıs haziran temmuz ağustos eylül ekim kasım aralık'.split(), range(1, 13)))
MONTH_NAMES = [None] + 'Ocak Şubat Mart Nisan Mayıs Haziran Temmuz Ağustos Eylül Ekim Kasım Aralık'.split()
DATE_LINE = re.compile(r'[*_]*\s*\d{1,2}\s+[A-Za-zçğıöşüÇĞİÖŞÜ]+\s+\d{4}\s*[*_]*')
DATE_PREFIX = re.compile(r'^(\d{4}[.-]\d{2}[.-]\d{2}|\d{2}[.-]\d{2}[.-]\d{4})[-_. ]+')


def git_modified(path):
    try:
        p = subprocess.run(['git', 'log', '-1', '--format=%cI', '--', str(path.relative_to(ROOT))],
                           cwd=ROOT, capture_output=True, text=True)
        return datetime.fromisoformat(p.stdout.strip()).astimezone(timezone.utc)
    except (ValueError, OSError):
        return None


def publish_date(slug, source, modified):
    """Öncelik: dosya adındaki tarih -> yazı içindeki tarih satırı -> son git commit tarihi."""
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


def tr_date(d):
    return f'{d.day} {MONTH_NAMES[d.month]} {d.year}'


def clean(s):
    s = re.sub(r'!?\[([^]]*)\]\([^)]+\)', r'\1', s)
    return html.unescape(re.sub(r'<[^>]+>|[*_`~]+', '', s)).strip()


def shorten(s, limit):
    if len(s) <= limit:
        return s
    return s[:limit].rsplit(' ', 1)[0].rstrip(',;:.-– ') + '…'


def details(source, slug):
    m = re.search(r'^#{1,6}\s+(.+?)\s*#*\s*$', source, re.M)
    title = clean(m[1]) if m else clean(DATE_PREFIX.sub('', slug).replace('-', ' ').replace('_', ' '))
    description = title
    for block in re.split(r'\n\s*\n', source):
        lines = [l for l in block.strip().splitlines()
                 if not re.match(r'\s*#{1,6}\s', l) and not DATE_LINE.fullmatch(l.strip())]
        text = '\n'.join(lines).strip()
        if not text or text.startswith(('```', '~~~', '|', '<', '- ', '* ', '>', '!', '---')):
            continue
        paragraph = clean(re.sub(r'\s+', ' ', text))
        if len(paragraph) > 20:
            description = shorten(paragraph, 160)
            break
    return title, description


def render(source):
    content = markdown.markdown(source, extensions=['fenced_code', 'tables', 'sane_lists', 'toc'])

    def fix(m):
        name, q, value = m.groups()
        parts = urlsplit(html.unescape(value))
        if parts.scheme or parts.netloc or value.startswith(('/', '#', '//')):
            return m[0]
        if name.lower() == 'href' and parts.path.lower().endswith('.md'):
            stem = Path(parts.path).stem
            dest = '/hakkimda/' if stem == 'hakkimda' else '/yazi/' + quote(stem, safe='-_.~') + '/'
        else:
            dest = '/' + quote(normpath('posts/' + parts.path), safe='/-_.~')
        if parts.query:
            dest += '?' + parts.query
        if parts.fragment:
            dest += '#' + parts.fragment
        return name + '=' + q + html.escape(dest, quote=True) + q

    content = re.sub(r'\b(src|href)=(\"|\')(.*?)\2', fix, content, flags=re.I | re.S)
    return re.sub(r'<img (?![^>]*loading=)', '<img loading="lazy" decoding="async" ', content)


def with_h1(markup, title):
    """Her sayfada tek bir <h1> olsun (SEO). İlk başlık h1 değilse h1'e yükseltilir."""
    if re.search(r'<h1[\s>]', markup):
        return markup
    if re.search(r'<h[2-6][\s>]', markup):
        return re.sub(r'<h[2-6]([^>]*)>(.*?)</h[2-6]>', r'<h1\1>\2</h1>', markup, count=1, flags=re.S)
    return f'<h1>{html.escape(title)}</h1>\n' + markup


def ld_json(data):
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False).replace('</', '<\\/') + '</script>'


def layout(title, description, url, body, *, full_title=None, og_type='website', ld=None,
           current='', robots='index,follow', extra_meta=''):
    e = lambda s: html.escape(s, quote=True)
    page_title = e(full_title or f'{title} — {SITE}')
    nav = [('Yazılar', '/', 'home'), ('Hakkımda', '/hakkimda/', 'about')]
    links = ''.join(f'<a href="{href}"{" aria-current=\"page\"" if key == current else ""}>{name}</a>' for name, href, key in nav)
    links += f'<a href="{GITHUB}" rel="me noopener noreferrer" target="_blank">GitHub</a>'
    if EMAIL:
        links += f'<a href="mailto:{e(EMAIL)}">E-posta</a>'
    contact = f'<a href="{GITHUB}" rel="me noopener noreferrer" target="_blank">GitHub</a> · ' + \
              (f'<a href="mailto:{e(EMAIL)}">E-posta</a> · ' if EMAIL else '') + '<a href="/rss.xml">RSS</a>'
    return f'''<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{page_title}</title>
<meta name="description" content="{e(description)}">
<meta name="robots" content="{robots}">
<meta name="author" content="{SITE}">
<meta name="theme-color" content="#ffffff">
<link rel="canonical" href="{e(url)}">
<link rel="icon" href="/favicon.ico?v=2">
<link rel="alternate" type="application/rss+xml" title="{SITE} RSS" href="/rss.xml">
<link rel="sitemap" type="application/xml" href="/sitemap.xml">
<link rel="stylesheet" href="/assets/blog.css?v={ASSET_VERSION}">
<meta property="og:site_name" content="{SITE}">
<meta property="og:locale" content="tr_TR">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{e(url)}">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(description)}">
{extra_meta}{ld_json(ld) if ld else ''}
</head>
<body>
<header class="site-header"><div class="shell header-inner">
<a class="site-title" href="/">{SITE}<span aria-hidden="true">.</span></a>
<form class="site-search" id="site-search-form" role="search" autocomplete="off">
<label class="visually-hidden" for="site-search-input">Yazılarda ara</label>
<input id="site-search-input" type="search" name="q" placeholder="Yazılarda ara..." aria-controls="site-search-results" aria-expanded="false" minlength="2" maxlength="100">
<svg class="search-icon" aria-hidden="true" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="square"><circle cx="10.5" cy="10.5" r="6.5"></circle><path d="M15.5 15.5 21 21"></path></svg>
<div class="search-results" id="site-search-results" role="status" aria-live="polite" hidden></div>
</form>
<nav class="site-nav" aria-label="Ana menü">{links}</nav>
</div></header>
<main>{body}</main>
<footer class="site-footer"><div class="shell footer-inner">
<span>© {datetime.now().year} {SITE} · Kişisel notlar</span>
<span>{contact}</span>
</div></footer>
<script src="/assets/search.js?v={ASSET_VERSION}" defer></script>
</body>
</html>
'''


def xml_output(root, filename):
    (DIST / filename).write_text('<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(root, encoding='unicode') + '\n', encoding='utf-8')


ASSET_VERSION = hashlib.md5(b''.join(p.read_bytes() for p in sorted((ROOT / 'assets').glob('*')) if p.suffix in {'.css', '.js'})).hexdigest()[:8]


def main():
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()
    # Site dosyalarını kopyala. .md kaynakları yayınlanmaz (yinelenen içerik olmasın).
    for source in ROOT.rglob('*'):
        if source.is_symlink() or not source.is_file():
            continue
        path = source.relative_to(ROOT)
        if path.parts[0] in EXCLUDE or source.suffix.lower() in {'.zip', '.md'}:
            continue
        target = DIST / path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    (DIST / '.nojekyll').touch()

    posts = []
    posts_dir = ROOT / 'posts'
    for path in sorted(posts_dir.glob('*.md')) if posts_dir.is_dir() else []:
        slug = path.stem
        source = path.read_text(encoding='utf-8-sig')
        title, desc = details(source, slug)
        modified = git_modified(path)
        published = publish_date(slug, source, modified)
        last = max(published, modified) if modified else published
        route = '/yazi/' + quote(slug, safe='-_.~') + '/'
        rendered = with_h1(render(source), title)
        posts.append(dict(slug=slug, title=title, excerpt=desc, text=source, published=published,
                          modified=last, path=route, url=BASE + route, rendered=rendered))
    # Sıralama: yazının (dosya adındaki) tarihine göre, yeniden eskiye.
    posts.sort(key=lambda x: (x['published'].date(), x['modified'], x['slug']), reverse=True)

    author = {'@type': 'Person', 'name': SITE, 'url': GITHUB}
    for p in posts:
        body = f'<article class="prose">{p["rendered"]}<p class="back"><a href="/">← Tüm yazılar</a></p></article>'
        meta = (f'<meta property="article:published_time" content="{p["published"].date().isoformat()}">'
                f'<meta property="article:modified_time" content="{p["modified"].date().isoformat()}">\n')
        ld = {'@context': 'https://schema.org', '@type': 'BlogPosting', 'headline': p['title'],
              'description': p['excerpt'], 'inLanguage': 'tr', 'url': p['url'],
              'mainEntityOfPage': p['url'], 'author': author,
              'datePublished': p['published'].date().isoformat(), 'dateModified': p['modified'].date().isoformat()}
        out = DIST / 'yazi' / p['slug'] / 'index.html'
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(layout(p['title'], p['excerpt'], p['url'], body, og_type='article', ld=ld, extra_meta=meta), encoding='utf-8')

    # Ana sayfa
    items = ''.join(
        f'<li class="post-item"><time class="post-date" datetime="{p["published"].date().isoformat()}">{tr_date(p["published"])}</time>'
        f'<div><a class="post-link" href="{p["path"]}">{html.escape(p["title"])}</a>'
        f'<p class="post-excerpt">{html.escape(shorten(p["excerpt"], 140))}</p></div></li>' for p in posts)
    listing = f'<ul class="post-list">{items}</ul>' if posts else '<p>Henüz yayımlanmış bir yazı yok.</p>'
    home = f'<section class="shell home"><h1>Yazılar</h1><p class="tagline">{html.escape(TAGLINE)}</p>{listing}</section>'
    home_ld = {'@context': 'https://schema.org', '@type': 'Blog', 'name': SITE, 'url': BASE + '/',
               'description': DESCRIPTION, 'inLanguage': 'tr', 'author': author}
    (DIST / 'index.html').write_text(layout(SITE, DESCRIPTION, BASE + '/', home, current='home', ld=home_ld,
                                            full_title=f'{SITE} — Yazılım, açık kaynak ve kişisel notlar'), encoding='utf-8')

    # Hakkımda
    about_file = ROOT / 'hakkimda.md'
    about_modified = None
    if about_file.is_file():
        about_source = about_file.read_text(encoding='utf-8-sig')
        title, description = details(about_source, 'hakkimda')
        about_modified = git_modified(about_file)
        body = f'<article class="prose">{with_h1(render(about_source), title)}</article>'
        out = DIST / 'hakkimda' / 'index.html'
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(layout(title, description, BASE + '/hakkimda/', body, current='about'), encoding='utf-8')

    # 404 (GitHub Pages bu dosyayı otomatik kullanır)
    (DIST / '404.html').write_text(layout('Sayfa bulunamadı', 'Aradığın sayfa bulunamadı.', BASE + '/404.html',
        '<section class="shell home"><h1>Sayfa bulunamadı</h1><p class="tagline"><a href="/">Ana sayfaya dön</a></p></section>',
        robots='noindex,follow'), encoding='utf-8')

    # Arama indeksi
    (DIST / 'search-index.json').write_text(json.dumps([
        {'slug': p['slug'], 'path': p['path'], 'title': p['title'], 'excerpt': p['excerpt'], 'text': p['text'],
         'date': p['published'].date().isoformat()} for p in posts
    ], ensure_ascii=False, separators=(',', ':')), encoding='utf-8')

    # sitemap.xml (otomatik: posts/ içindeki her .md için bir adres)
    ns = 'http://www.sitemaps.org/schemas/sitemap/0.9'
    ET.register_namespace('', ns)
    sitemap = ET.Element('{' + ns + '}urlset')
    newest = max((p['modified'] for p in posts), default=None)
    urls = [(BASE + '/', newest)]
    if about_file.is_file():
        urls.append((BASE + '/hakkimda/', about_modified))
    urls.extend((p['url'], p['modified']) for p in posts)
    for url, lastmod in urls:
        row = ET.SubElement(sitemap, '{' + ns + '}url')
        ET.SubElement(row, '{' + ns + '}loc').text = url
        if lastmod:
            ET.SubElement(row, '{' + ns + '}lastmod').text = lastmod.date().isoformat()
    xml_output(sitemap, 'sitemap.xml')

    # rss.xml
    content_ns = 'http://purl.org/rss/1.0/modules/content/'
    atom_ns = 'http://www.w3.org/2005/Atom'
    ET.register_namespace('content', content_ns)
    ET.register_namespace('atom', atom_ns)
    rss = ET.Element('rss', {'version': '2.0'})
    channel = ET.SubElement(rss, 'channel')
    for tag, value in [('title', f'{SITE} — Blog'), ('link', BASE + '/'), ('description', DESCRIPTION),
                       ('language', 'tr-TR'), ('lastBuildDate', format_datetime(datetime.now(timezone.utc))), ('ttl', '60')]:
        ET.SubElement(channel, tag).text = value
    ET.SubElement(channel, '{' + atom_ns + '}link', {'href': BASE + '/rss.xml', 'rel': 'self', 'type': 'application/rss+xml'})
    for p in posts[:50]:
        item = ET.SubElement(channel, 'item')
        for tag, value in [('title', p['title']), ('link', p['url']), ('description', p['excerpt']),
                           ('pubDate', format_datetime(p['published']))]:
            ET.SubElement(item, tag).text = value
        ET.SubElement(item, 'guid', {'isPermaLink': 'true'}).text = p['url']
        ET.SubElement(item, '{' + content_ns + '}encoded').text = re.sub(r'\b(src|href)="/(?!/)', rf'\1="{BASE}/', p['rendered'])
    xml_output(rss, 'rss.xml')

    (DIST / 'robots.txt').write_text('User-agent: *\nAllow: /\n\nSitemap: ' + BASE + '/sitemap.xml\n', encoding='utf-8')
    print(f'{len(posts)} yazı, sitemap.xml, rss.xml, arama indeksi ve sayfalar hazırlandı.')


if __name__ == '__main__':
    main()
