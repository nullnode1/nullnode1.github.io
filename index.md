
---
title: Ana Sayfa
---

<link rel="icon" type="image/x-icon" href="{{ '/favicon.ico' | relative_url }}">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.7.2/css/all.min.css">

<style>
/* =========================================
   DARK EDITORIAL THEME
   Tek dosyalık Jekyll ana sayfa tasarımı
   ========================================= */

:root {
  color-scheme: dark;

  --bg: #090909;
  --surface: #101010;
  --surface-hover: #151515;
  --border: #252525;
  --border-hover: #3a3a3a;

  --text: #ededed;
  --secondary: #a0a0a0;
  --muted: #686868;

  --radius: 7px;
  --width: 860px;
}

html {
  background: var(--bg);
}

body {
  margin: 0;
  background: var(--bg);
  color: var(--text);

  font-family: Inter, -apple-system, BlinkMacSystemFont,
    "Segoe UI", sans-serif;

  font-size: 15px;
  line-height: 1.7;

  -webkit-font-smoothing: antialiased;
}

.home-container,
.home-container * {
  box-sizing: border-box;
}

.home-container {
  width: min(var(--width), calc(100% - 48px));
  margin: 0 auto;
}

.home-container a {
  color: inherit;
  text-decoration: none;
}

/* Header */

.home-header {
  height: 76px;

  display: flex;
  align-items: center;
  justify-content: space-between;

  border-bottom: 1px solid var(--border);
}

.header-brand {
  display: flex;
  align-items: center;
  gap: 11px;

  color: var(--secondary);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 2px;
}

.brand-indicator {
  width: 7px;
  height: 7px;
  background: #eee;
  border-radius: 2px;
}

.rss-button {
  display: inline-flex;
  align-items: center;
  gap: 9px;

  padding: 8px 13px;

  color: var(--secondary);
  background: var(--surface);

  border: 1px solid var(--border);
  border-radius: var(--radius);

  font-size: 12px;
  font-weight: 600;
}

.rss-button:hover {
  color: var(--text);
  border-color: var(--border-hover);
  background: var(--surface-hover);
}

/* Hero */

.hero-section {
  padding: 85px 0 65px;
  border-bottom: 1px solid var(--border);
}

.hero-label {
  color: var(--muted);
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 2px;
}

.hero-section h1 {
  margin: 15px 0 12px;

  color: var(--text);
  font-size: clamp(34px, 6vw, 53px);
  font-weight: 750;
  letter-spacing: -2.5px;
  line-height: 1.15;
}

.hero-section h1 span {
  color: #777;
}

.hero-section p {
  max-width: 500px;
  margin: 0;
  color: var(--secondary);
  font-size: 14px;
}

/* Posts */

.posts-section {
  padding: 55px 0 75px;
}

.section-heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.section-heading h2 {
  margin: 0;
  font-size: 16px;
  font-weight: 650;
}

.section-heading span {
  color: var(--muted);
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 1px;
}

.posts-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.post-card {
  min-height: 82px;

  display: grid;
  grid-template-columns: 145px 1fr 24px;
  align-items: center;
  gap: 15px;

  padding: 17px 20px;

  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
}

.post-date {
  display: flex;
  align-items: center;
  gap: 9px;

  color: var(--muted);
  font-size: 12px;
  white-space: nowrap;
}

.post-content h3 {
  margin: 0;
  color: var(--text);
  font-size: 14px;
  font-weight: 600;
  line-height: 1.5;
}

.post-content a:hover {
  color: #bdbdbd;
}

.post-arrow {
  color: var(--muted);
  font-size: 12px;
  text-align: right;
}

.post-card:hover {
  background: var(--surface-hover);
  border-color: var(--border-hover);
}

/* Empty state */

.empty-state {
  padding: 55px 20px;
  text-align: center;

  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
}

.empty-state i {
  color: var(--muted);
  font-size: 25px;
}

.empty-state h3 {
  margin: 15px 0 5px;
  font-size: 15px;
}

.empty-state p {
  margin: 0;
  color: var(--secondary);
  font-size: 13px;
}

/* Footer */

.home-footer {
  min-height: 85px;

  display: flex;
  align-items: center;
  justify-content: space-between;

  border-top: 1px solid var(--border);

  color: var(--muted);
  font-size: 11px;
}

.social-links {
  display: flex;
  align-items: center;
  gap: 9px;
}

.social-links a {
  width: 35px;
  height: 35px;

  display: flex;
  align-items: center;
  justify-content: center;

  color: var(--secondary);
  background: var(--surface);

  border: 1px solid var(--border);
  border-radius: var(--radius);
}

.social-links a:hover {
  color: var(--text);
  border-color: var(--border-hover);
}

/* Responsive */

@media (max-width: 600px) {

  .home-container {
    width: calc(100% - 32px);
  }

  .home-header {
    height: 65px;
  }

  .hero-section {
    padding: 65px 0 45px;
  }

  .hero-section h1 {
    letter-spacing: -1.7px;
  }

  .posts-section {
    padding: 40px 0 55px;
  }

  .post-card {
    grid-template-columns: 1fr 20px;
    gap: 8px;
    padding: 15px;
  }

  .post-date {
    grid-column: 1;
    grid-row: 1;
  }

  .post-content {
    grid-column: 1;
    grid-row: 2;
  }

  .post-arrow {
    grid-column: 2;
    grid-row: 1 / 3;
  }

  .home-footer {
    min-height: 75px;
  }

}

@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation: none !important;
    transition: none !important;
    scroll-behavior: auto !important;
  }
}
</style>

<div class="home-container">

  <header class="home-header">

    <div class="header-brand">
      <span class="brand-indicator"></span>
      <span>KİŞİSEL BLOG</span>
    </div>

    <a class="rss-button" href="{{ '/rss.xml' | relative_url }}" aria-label="RSS Feed">
      <i class="fas fa-rss"></i>
      <span>RSS Feed</span>
    </a>

  </header>

  <main>

    <section class="hero-section">
      <span class="hero-label">BLOG / YAZILAR</span>

      <h1>Son Gönderilerim<span>.</span></h1>

      <p>Yayınladığım yazılar, notlar ve üzerinde çalıştığım konular.</p>
    </section>

    {% assign tum_yazilar = site.pages
      | where_exp: "item", "item.path contains 'posts/'"
      | where_exp: "item", "item.name != 'index.md'"
      | where_exp: "item", "item.date != nil"
      | sort: "date"
      | reverse %}

    <section class="posts-section">

      <div class="section-heading">
        <h2>Yayınlar</h2>
        <span>{{ tum_yazilar.size }} YAZI</span>
      </div>

      {% if tum_yazilar.size > 0 %}

        <div class="posts-list">

          {% for yazi in tum_yazilar %}

            <article class="post-card">

              <div class="post-date">
                <i class="far fa-calendar-alt"></i>
                <time>{{ yazi.date | date: "%d.%m.%Y" }}</time>
              </div>

              <div class="post-content">
                <h3>
                  <a href="{{ yazi.url | relative_url }}">
                    {{ yazi.title | default: yazi.name }}
                  </a>
                </h3>
              </div>

              <div class="post-arrow">
                <i class="fas fa-arrow-right"></i>
              </div>

            </article>

          {% endfor %}

        </div>

      {% else %}

        <div class="empty-state">
          <i class="far fa-folder-open"></i>
          <h3>Henüz yayın yok.</h3>
          <p>Yeni yazılar yayınlandığında burada görünecek.</p>
        </div>

      {% endif %}

    </section>

  </main>

  <footer class="home-footer">

    <span>© {{ site.time | date: "%Y" }} {{ site.title }}</span>

    <div class="social-links">

      <a href="https://github.com/nullnode1"
         target="_blank"
         rel="noopener noreferrer"
         aria-label="GitHub">
        <i class="fab fa-github"></i>
      </a>

      <a href="https://www.linkedin.com/"
         target="_blank"
         rel="noopener noreferrer"
         aria-label="LinkedIn">
        <i class="fab fa-linkedin-in"></i>
      </a>

      <a href="{{ '/rss.xml' | relative_url }}"
         aria-label="RSS">
        <i class="fas fa-rss"></i>
      </a>

    </div>

  </footer>

</div>
