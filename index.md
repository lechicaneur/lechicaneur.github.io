---
layout: default
title: Accueil
---

{% if site.posts.size == 0 %}
<article>
    <p style="font-style: italic; color: var(--muted-color); text-align: center;">
        Les archives de la rédaction sont en cours de constitution. Les premiers dossiers d'investigation seront publiés prochainement.
    </p>
</article>
{% else %}
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
{% endif %}