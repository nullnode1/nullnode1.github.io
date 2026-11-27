---
title: Ana Sayfa
---

<link rel="icon" type="image/x-icon" href="{{ '/favicon.ico' | relative_url }}">
<link rel="shortcut icon" type="image/x-icon" href="{{ '/favicon.ico' | relative_url }}">

<style>
  .blog-container {
    max-width: 720px;
    margin: 2rem auto;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    line-height: 1.6;
    color: #1f2328;
  }
  .blog-header {
    border-bottom: 2px solid #eaecef;
    padding-bottom: 1rem;
    margin-bottom: 2rem;
  }
  .blog-header h1 {
    margin: 0;
    font-size: 2rem;
  }
  .blog-header p {
    margin: 0.4rem 0 0;
    color: #656d76;
  }
  .post-list {
    list-style: none;
    padding: 0;
    margin: 0;
  }
  .post-item {
    display: flex;
    flex-direction: column;
    padding: 1.2rem;
    margin-bottom: 1rem;
    border: 1px solid #d0d7de;
    border-radius: 8px;
    background-color: #ffffff;
    transition: transform 0.15s ease, box-shadow 0.15s ease, border-color 0.15s ease;
  }
  .post-item:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
    border-color: #0969da;
  }
  .post-meta {
    font-size: 0.85rem;
    color: #656d76;
    margin-bottom: 0.35rem;
    font-weight: 500;
  }
  .post-title {
    font-size: 1.25rem;
    font-weight: 600;
    color: #0969da;
    text-decoration: none;
  }
  .post-title:hover {
    text-decoration: underline;
  }
  .post-excerpt {
    margin: 0.5rem 0 0;
    font-size: 0.95rem;
    color: #424a53;
  }
</style>

<div class="blog-container">
  <header class="blog-header">
    <h1>Son Gönderilerim</h1>
    <p>Notlar, yazılar ve paylaşımlar</p>
  </header>

  {% comment %} Sadece posts/ klasöründeki ve tarihi tanımlı olan .md dosyalarını alıp tarihe göre sıralar {% endcomment %}
  {% assign tum_yazilar = site.pages | where_exp: "item", "item.path contains 'posts/'" | where_exp: "item", "item.name != 'index.md'" | where_exp: "item", "item.date != nil" | sort: "date" | reverse %}

  {% if tum_yazilar.size > 0 %}
    <ul class="post-list">
      {% for yazi in tum_yazilar %}
        <li class="post-item">
          <span class="post-meta">📅 {{ yazi.date | date: "%d.%m.%Y" }}</span>
          <a class="post-title" href="{{ yazi.url | relative_url }}">
            {{ yazi.title | default: yazi.name }}
          </a>
          {% if yazi.description %}
            <p class="post-excerpt">{{ yazi.description }}</p>
          {% endif %}
        </li>
      {% endfor %}
    </ul>
  {% else %}
    <p>Henüz yayınlanmış bir yazı bulunmuyor.</p>
  {% endif %}
</div>
