// ==UserScript==
// @name         Nyaa Search and Save (PT-BR)
// @namespace    http://tampermonkey.net/
// @version      0.6
// @description  Busca no nyaa.si, salva os resultados 1080p em português, com botão de parar.
// @match        https://nyaa.si/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    const IS_SCRAPING_KEY = 'nyaa_is_scraping';
    const RESULTS_KEY = 'nyaa_results';
    const SEARCH_TERM_KEY = 'nyaa_search_term';

    function setupButton() {
        const formContainer = document.querySelector('form.search-form');
        const existingButton = document.getElementById('nyaa-scraper-button');
        if (existingButton) existingButton.remove(); // Remove o botão antigo se existir

        const actionButton = document.createElement('button');
        actionButton.id = 'nyaa-scraper-button';
        actionButton.className = 'btn btn-primary';
        actionButton.style.marginLeft = '10px';

        const isScraping = sessionStorage.getItem(IS_SCRAPING_KEY) === 'true';

        if (isScraping) {
            actionButton.innerHTML = 'Parar e Salvar Agora';
            actionButton.classList.add('btn-danger'); // Cor vermelha para indicar "parar"
            actionButton.addEventListener('click', stopAndSave);
        } else {
            actionButton.innerHTML = 'Buscar e Salvar 1080p (PT-BR)';
            actionButton.addEventListener('click', startSearchAndSave);
        }

        if (formContainer) {
            const buttonGroup = formContainer.querySelector('.input-group');
            if (buttonGroup) buttonGroup.appendChild(actionButton);
            else formContainer.appendChild(actionButton);
        } else {
            Object.assign(actionButton.style, {
                position: 'fixed', top: '15px', right: '15px', zIndex: '9999'
            });
            document.body.appendChild(actionButton);
        }
    }

    function startSearchAndSave() {
        const searchTerm = prompt('Digite o termo para buscar e salvar:', '');
        if (searchTerm === null || searchTerm.trim() === '') return;

        if (confirm(`Isso iniciará uma nova busca por "${searchTerm}" e navegará por todas as páginas. Deseja continuar?`)) {
            sessionStorage.setItem(IS_SCRAPING_KEY, 'true');
            sessionStorage.setItem(RESULTS_KEY, JSON.stringify([]));
            sessionStorage.setItem(SEARCH_TERM_KEY, searchTerm);
            window.location.href = `https://nyaa.si/?f=0&c=0_0&q=${encodeURIComponent(searchTerm)}`;
        }
    }

    function stopAndSave() {
        if (confirm('Tem certeza que deseja parar a busca e salvar os resultados coletados até agora?')) {
            console.log('Busca interrompida pelo usuário.');
            saveResultsToFile();
            cleanupStorage();
            window.location.reload(); // Recarrega para resetar o estado do botão
        }
    }

    function scrapeCurrentPageAndContinue() {
        console.log('Extraindo dados da página atual...');
        const storedResults = JSON.parse(sessionStorage.getItem(RESULTS_KEY) || '[]');
        const keywords = ['1080p'];
        const langKeywords = ['pt-br', 'pt', 'português', 'legendado', 'dual áudio'];

        document.querySelectorAll('table.torrent-list tbody tr').forEach(row => {
            const titleElement = row.querySelector('td:nth-child(2) a:not(.comments)');
            if (!titleElement) return;

            const title = titleElement.textContent.toLowerCase();
            const hasQuality = keywords.some(kw => title.includes(kw));
            const hasLang = langKeywords.some(kw => title.includes(kw));

            if (hasQuality && hasLang) {
                const magnetLink = row.querySelector('td:nth-child(3) a[href^="magnet:"]');
                if (magnetLink) {
                    storedResults.push({ title: titleElement.textContent.trim(), magnet: magnetLink.href });
                }
            }
        });
        sessionStorage.setItem(RESULTS_KEY, JSON.stringify(storedResults));

        // Lógica de navegação corrigida: procura por um link "next" que não esteja em um elemento desativado.
        const nextButton = document.querySelector('.pagination li.next:not(.disabled) a');
        if (nextButton && nextButton.href !== window.location.href) {
            console.log('Navegando para a próxima página...');
            setTimeout(() => { window.location.href = nextButton.href; }, 800);
        } else {
            console.log('Extração concluída. Não há mais páginas ou o botão "next" está desativado.');
            saveResultsToFile();
            cleanupStorage();
            // Recarrega a página para o botão voltar ao estado inicial "Buscar"
            setTimeout(() => { window.location.reload(); }, 1000);
        }
    }

    function saveResultsToFile() {
        const results = JSON.parse(sessionStorage.getItem(RESULTS_KEY) || '[]');
        if (results.length === 0) {
            alert('Nenhum resultado foi encontrado para salvar.');
            return;
        }

        let fileContent = `Resultados da Busca por "${sessionStorage.getItem(SEARCH_TERM_KEY)}" (1080p PT-BR)\n\n`;
        results.forEach(item => {
            fileContent += `Título: ${item.title}\nMagnet Link: ${item.magnet}\n\n`;
        });

        const blob = new Blob([fileContent], { type: 'text/plain;charset=utf-8' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        const searchTerm = sessionStorage.getItem(SEARCH_TERM_KEY) || 'nyaa';
        const fileName = `${searchTerm.replace(/[^a-z0-9]/gi, '_')}_1080p_ptbr.txt`;
        link.download = fileName;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

        alert(`Resultados salvos com sucesso em "${fileName}"!\n\nO arquivo deve estar na sua pasta de Downloads.`);
    }

    function cleanupStorage() {
        sessionStorage.removeItem(IS_SCRAPING_KEY);
        sessionStorage.removeItem(RESULTS_KEY);
        sessionStorage.removeItem(SEARCH_TERM_KEY);
    }

    function initialize() {
        setupButton();
        if (sessionStorage.getItem(IS_SCRAPING_KEY) === 'true') {
            scrapeCurrentPageAndContinue();
        }
    }

    // Garante que o script rode mesmo se injetado após o carregamento da página
    if (document.readyState === 'complete') {
        initialize();
    } else {
        window.addEventListener('load', initialize);
    }
})();
