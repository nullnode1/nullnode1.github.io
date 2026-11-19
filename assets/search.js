/* GitHub Pages için küçük arama: yayındaki JSON indeksini okur.
   Actions henüz etkin değilse depodaki .md dosyalarından arama yapabilir. */
(() => {
  'use strict';
  const form = document.getElementById('site-search-form');
  const input = document.getElementById('site-search-input');
  const results = document.getElementById('site-search-results');
  if (!form || !input || !results) return;

  let indexPromise = null;
  let searchSequence = 0;
  let matching = [];

  const normalize = (text) => String(text ?? '')
    .replace(/ı/g, 'i')
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLocaleLowerCase('tr-TR');

  const clear = () => {
    results.hidden = true;
    results.replaceChildren();
    input.setAttribute('aria-expanded', 'false');
    matching = [];
  };
  const message = (text) => {
    results.replaceChildren();
    const el = document.createElement('p');
    el.className = 'search-status';
    el.textContent = text;
    results.append(el);
    results.hidden = false;
    input.setAttribute('aria-expanded', 'true');
  };

  function postFromFilename(name) {
    const slug = name.replace(/\.md$/i, '');
    const match = /^(?:(\d{4})[-.](\d{2})[-.](\d{2})|(?:(\d{2})[-.](\d{2})[-.](\d{4})))-(.+)$/.exec(slug);
    const title = (match ? match[7] : slug).replace(/[-_]+/g, ' ');
    return { slug, title, excerpt: '', text: '' };
  }

  async function fallbackIndex() {
    const api = 'https://api.github.com/repos/nullnode1/nullnode1.github.io/contents/posts?ref=main';
    const response = await fetch(api, { headers: { Accept: 'application/vnd.github+json' } });
    if (!response.ok) throw new Error('Yazılar alınamadı. GitHub API erişim sınırına ulaşılmış olabilir.');
    const files = await response.json();
    if (!Array.isArray(files)) throw new Error('Yazı dizini bulunamadı.');
    const posts = files.filter(p => p.type === 'file' && /\.md$/i.test(p.name));
    const output = [];
    // Tarayıcıyı boğmamak için aynı anda en fazla 5 Markdown isteği.
    for (let offset = 0; offset < posts.length; offset += 5) {
      const chunk = await Promise.all(posts.slice(offset, offset + 5).map(async (file) => {
        const item = postFromFilename(file.name);
        try {
          const url = 'https://raw.githubusercontent.com/nullnode1/nullnode1.github.io/main/posts/' + encodeURIComponent(file.name);
          const response = await fetch(url);
          if (response.ok) {
            item.text = await response.text();
            const heading = /^#\s+(.+)$/m.exec(item.text);
            if (heading) item.title = heading[1].replace(/[*_`]/g, '');
          }
        } catch (_) { /* Başlıkla arama yapılabilir. */ }
        item.excerpt = item.text.replace(/[#*`_>\[\]()]/g, ' ').replace(/\s+/g, ' ').slice(0, 120);
        return item;
      }));
      output.push(...chunk);
    }
    return output;
  }

  function loadIndex() {
    if (!indexPromise) {
      indexPromise = (async () => {
        try {
          const response = await fetch('./search-index.json');
          if (response.ok) {
            const data = await response.json();
            if (Array.isArray(data)) return data;
          }
        } catch (_) { /* İlk deploy'da GitHub API'ye dön. */ }
        return fallbackIndex();
      })().catch(error => {
        indexPromise = null;
        throw error;
      });
    }
    return indexPromise;
  }

  async function search() {
    const query = input.value.trim();
    const id = ++searchSequence;
    if (query.length < 2) { clear(); return; }
    message('Aranıyor…');
    try {
      const allPosts = await loadIndex();
      if (id !== searchSequence) return;
      const terms = normalize(query).split(/\s+/).filter(Boolean);
      matching = allPosts.filter(post => {
        const haystack = normalize([post.title, post.excerpt, post.text].join(' '));
        return terms.every(term => haystack.includes(term));
      }).slice(0, 8);
      results.replaceChildren();
      if (!matching.length) { message('Sonuç bulunamadı.'); return; }
      for (const post of matching) {
        const link = document.createElement('a');
        link.className = 'search-result';
        link.href = '#/posts/' + encodeURIComponent(post.slug);
        const title = document.createElement('span');
        title.className = 'search-result-title';
        title.textContent = post.title;
        link.append(title);
        if (post.excerpt) {
          const excerpt = document.createElement('span');
          excerpt.className = 'search-result-excerpt';
          excerpt.textContent = post.excerpt.slice(0, 105);
          link.append(excerpt);
        }
        results.append(link);
      }
      results.hidden = false;
      input.setAttribute('aria-expanded', 'true');
    } catch (error) {
      if (id === searchSequence) message(error.message || 'Arama kullanılamıyor.');
    }
  }

  input.addEventListener('input', search);
  input.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
      input.value = '';
      ++searchSequence;
      clear();
      input.blur();
    }
  });
  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const first = results.querySelector('a.search-result');
    if (first) {
      window.location.hash = first.getAttribute('href');
      input.value = '';
      ++searchSequence;
      clear();
    }
  });
  document.addEventListener('pointerdown', (event) => {
    if (!form.contains(event.target)) clear();
  });
  window.addEventListener('hashchange', () => {
    input.value = '';
    ++searchSequence;
    clear();
  });
})();
