---
title: Ana Sayfa
---

<link rel="icon" type="image/x-icon" href="{{ '/favicon.ico' | relative_url }}">

# Son Gönderilerim

{% assign tum_yazilar = site.pages | where_exp: "item", "item.path contains 'posts/'" | where_exp: "item", "item.name != 'index.md'" | where_exp: "item", "item.date != nil" | sort: "date" | reverse %}

{% if tum_yazilar.size > 0 %}
  {% for yazi in tum_yazilar %}
* **{{ yazi.date | date: "%d.%m.%Y" }}** — [{{ yazi.title | default: yazi.name }}]({{ yazi.url | relative_url }})
  {% endfor %}
{% else %}
Henüz yayınlanmış bir yazı bulunmuyor.
{% endif %}
