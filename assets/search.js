/* Küçük site içi arama: /search-index.json dosyasını okur (build sırasında üretilir). */
(() => {
  'use strict';
  const form = document.getElementById('site-search-form');
  const input = document.getElementById('site-search-input');
  const results = document.getElementById('site-search-results');
  if (!form || !input || !results) return;

  let indexPromise = null;
  let sequence = 0;

  const normalize = (text) => String(text ?? '')
    .replace(/ı/g, 'i')
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLocaleLowerCase('tr-TR');

  const clear = () => {
    results.hidden = true;
    results.replaceChildren();
    input.setAttribute('aria-expanded', 'false');
  };
  const message = (text) => {
    const el = document.createElement('p');
    el.className = 'search-status';
    el.textContent = text;
    results.replaceChildren(el);
    results.hidden = false;
    input.setAttribute('aria-expanded', 'true');
  };

  function loadIndex() {
    if (!indexPromise) {
      indexPromise = fetch('/search-index.json')
        .then((response) => {
          if (!response.ok) throw new Error('Arama dizini yüklenemedi.');
          return response.json();
        })
        .then((data) => (Array.isArray(data) ? data : []))
        .catch((error) => { indexPromise = null; throw error; });
    }
    return indexPromise;
  }

  async function search() {
    const query = input.value.trim();
    const id = ++sequence;
    if (query.length < 2) { clear(); return; }
    message('Aranıyor…');
    try {
      const posts = await loadIndex();
      if (id !== sequence) return;
      const terms = normalize(query).split(/\s+/).filter(Boolean);
      const found = posts.filter((post) => {
        const haystack = normalize([post.title, post.excerpt, post.text].join(' '));
        return terms.every((term) => haystack.includes(term));
      }).slice(0, 8);
      if (!found.length) { message('Sonuç bulunamadı.'); return; }
      results.replaceChildren();
      for (const post of found) {
        const link = document.createElement('a');
        link.className = 'search-result';
        link.href = post.path;
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
      if (id === sequence) message(error.message || 'Arama kullanılamıyor.');
    }
  }

  input.addEventListener('focus', () => { loadIndex().catch(() => {}); }, { once: true });
  input.addEventListener('input', search);
  input.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') { input.value = ''; ++sequence; clear(); input.blur(); }
  });
  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const first = results.querySelector('a.search-result');
    if (first) window.location.href = first.getAttribute('href');
  });
  document.addEventListener('pointerdown', (event) => {
    if (!form.contains(event.target)) clear();
  });
})();
