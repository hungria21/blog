async function loadArticles() {
    const container = document.getElementById('articles-container');
    try {
        const response = await fetch(`manifest.json?t=${Date.now()}`);
        const articles = await response.json();

        container.innerHTML = articles.map(article => `
            <a href="posts/${article.id}.html" class="article-card block p-6 rounded-xl border border-zinc-800 bg-zinc-900/50 hover:bg-zinc-900 transition-all">
                ${article.image ? `<img src="${article.image}" class="w-full h-48 object-cover rounded-lg mb-4" alt="${article.title}">` : ''}
                <div class="flex justify-between items-center mb-2">
                    <span class="text-xs font-semibold text-zinc-500 uppercase tracking-wider">${article.date}</span>
                </div>
                <h2 class="text-2xl font-bold text-white mb-2">${article.title}</h2>
                <p class="text-zinc-400 line-clamp-2">${article.description}</p>
            </a>
        `).join('');
    } catch (error) {
        console.error('Erro ao carregar artigos:', error);
        container.innerHTML = '<p class="text-red-500">Erro ao carregar a lista de artigos.</p>';
    }
}

// Mantendo para compatibilidade ou uso futuro, mas o site agora foca em posts/*.html
async function loadArticleContent() {
    // ... logic would go here if needed ...
}