document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    const resultsContainer = document.getElementById('search-results');
    const mainFeed = document.getElementById('main-feed');
    let postsData = [];

    if (!searchInput) return;

    // Chargement de l'index généré par Jekyll
    fetch('/search.json')
        .then(response => response.json())
        .then(data => {
            postsData = data;
        })
        .catch(err => console.error('Erreur de chargement de l\'index :', err));

    searchInput.addEventListener('input', function() {
        const query = this.value.trim().toLowerCase();

        if (query.length < 2) {
            resultsContainer.innerHTML = '';
            resultsContainer.style.display = 'none';
            if (mainFeed) mainFeed.style.display = 'block';
            return;
        }

        if (mainFeed) mainFeed.style.display = 'none';
        resultsContainer.style.display = 'block';

        const matches = postsData.filter(post => {
            const titleMatch = post.title && post.title.toLowerCase().includes(query);
            const contentMatch = post.content && post.content.toLowerCase().includes(query);
            const catMatch = post.category && post.category.toLowerCase().includes(query);
            return titleMatch || contentMatch || catMatch;
        });

        if (matches.length === 0) {
            resultsContainer.innerHTML = '<p style="font-style: italic; color: var(--muted-color);">Aucun dossier ne correspond à cette requête dans les archives.</p>';
        } else {
            resultsContainer.innerHTML = matches.map(post => `
                <article>
                    <h2><a href="${post.url}">${post.title}</a></h2>
                    <div class="meta">
                        ${post.date} ${post.category ? '• ' + post.category : ''}
                    </div>
                    <p>${post.excerpt}</p>
                    <a class="read-more" href="${post.url}">Consulter le dossier complet →</a>
                </article>
            `).join('');
        }
    });
});