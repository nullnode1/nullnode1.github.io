---
layout: default
title: Ana Sayfa
---

# Yazılarım

{% assign gonderiler = site.pages | where_exp: "item", "item.path contains 'posts/'" | sort: "date" | reverse %}

{% if gonderiler.size > 0 %}
<ul>
  {% for yazi in gonderiler %}
    {% if yazi.name != 'index.md' %}
      <li>
        <span>{{ yazi.date | date: "%d.%m.%Y" }}</span> — 
        <a href="{{ yazi.url | relative_url }}">{{ yazi.title | default: yazi.name }}</a>
      </li>
    {% endif %}
  {% endfor %}
</ul>
{% else %}
<p>Henüz yayınlanmış bir yazı bulunmuyor.</p>
{% endif %}
