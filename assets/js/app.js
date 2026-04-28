document.addEventListener('DOMContentLoaded', () => {
    const articlesGrid = document.getElementById('articles-grid');
    const postContainer = document.getElementById('post-container');
    const postSkeleton = document.getElementById('post-skeleton');
    const postError = document.getElementById('post-error');

    // Utility to get URL parameters
    const getQueryParam = (param) => {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get(param);
    };

    // Fetch and render articles on index.html
    const loadArticles = async () => {
        try {
            const response = await fetch(`manifest.json?t=${Date.now()}`);
            const articles = await response.json();

            if (articlesGrid) {
                articlesGrid.innerHTML = articles.map(article => `
                    <a href="post.html?id=${article.id}" class="group block card-hover">
                        <article class="bg-zinc-900/50 border border-white/5 rounded-2xl overflow-hidden h-full flex flex-col transition-all duration-300 group-hover:border-white/10">
                            <div class="aspect-video overflow-hidden">
                                <img src="${article.image}" alt="${article.title}" class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105">
                            </div>
                            <div class="p-6 flex flex-col flex-grow">
                                <div class="flex items-center gap-3 text-xs text-zinc-500 font-medium mb-3">
                                    <span>${article.date}</span>
                                    <span class="w-1 h-1 bg-zinc-700 rounded-full"></span>
                                    <span class="text-zinc-400">Artigo</span>
                                </div>
                                <h3 class="text-xl font-bold mb-3 group-hover:text-zinc-300 transition-colors">${article.title}</h3>
                                <p class="text-zinc-400 text-sm leading-relaxed line-clamp-3">${article.description}</p>
                                <div class="mt-auto pt-6 flex items-center gap-2 text-sm font-semibold text-white">
                                    Ler mais
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="transition-transform group-hover:translate-x-1"><path d="M5 12h14m-7-7 7 7-7 7"/></svg>
                                </div>
                            </div>
                        </article>
                    </a>
                `).join('');
            }
        } catch (error) {
            console.error('Erro ao carregar manifest.json:', error);
            if (articlesGrid) {
                articlesGrid.innerHTML = '<p class="col-span-full text-center py-20 text-zinc-500">Erro ao carregar artigos. Tente novamente mais tarde.</p>';
            }
        }
    };

    // Fetch and render specific article on post.html
    const loadPost = async () => {
        const id = getQueryParam('id');
        if (!id) {
            console.error('ID do artigo não fornecido na URL');
            showError();
            return;
        }

        try {
            const manifestResponse = await fetch(`manifest.json?t=${Date.now()}`);
            const manifest = await manifestResponse.json();
            const articleMeta = manifest.find(a => a.id === id);

            if (!articleMeta) {
                console.error(`Artigo com ID "${id}" não encontrado no manifest.json`);
                showError();
                return;
            }

            console.log(`Carregando artigo: ${articleMeta.path}`);
            const response = await fetch(articleMeta.path);
            if (!response.ok) {
                console.error(`Erro ao buscar markdown: ${response.status} ${response.statusText}`);
                throw new Error('Falha ao carregar o arquivo markdown');
            }

            let markdown = await response.text();

            // Remove frontmatter if present
            markdown = markdown.replace(/^---[\s\S]*?---/, '');

            // Update DOM
            document.title = `${articleMeta.title} - Moonshot Blog`;
            document.getElementById('post-image').src = articleMeta.image;
            document.getElementById('post-date').textContent = articleMeta.date;
            document.getElementById('post-content').innerHTML = marked.parse(markdown);

            // Toggle visibility
            postSkeleton.classList.add('hidden');
            postContainer.classList.remove('hidden');

        } catch (error) {
            console.error('Erro ao carregar post:', error);
            showError();
        }
    };

    const showError = () => {
        postSkeleton.classList.add('hidden');
        postError.classList.remove('hidden');
    };

    // Init
    if (articlesGrid) {
        loadArticles();
    } else if (postContainer) {
        loadPost();
    }
});
