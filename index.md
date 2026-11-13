---
layout: default
title: Accueil
---

{% for post in site.posts %}
<article>
    <h2><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h2>
    <div class="meta">
        {{ post.date | date: "%d/%m/%Y" }}
        {% if post.author %} • Par {{ post.author }}{% endif %}
        {% if post.category %} • {{ post.category }}{% endif %}
    </div>
    <p>{{ post.excerpt | strip_html | truncatewords: 45 }}</p>
    <a class="read-more" href="{{ post.url | relative_url }}">Consulter le dossier complet →</a>
</article>
{% endfor %}