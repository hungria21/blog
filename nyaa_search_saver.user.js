// ==UserScript==
// @name         Nyaa Search and Save (PT-BR)
// @namespace    http://tampermonkey.net/
// @version      0.5
// @description  Inicia uma nova busca no nyaa.si e salva os resultados 1080p em português em um .txt.
// @match        https://nyaa.si/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    const IS_SCRAPING_KEY = 'nyaa_is_scraping';
    const RESULTS_KEY = 'nyaa_results';
    const SEARCH_TERM_KEY = 'nyaa_search_term';

    function addButton() {
        const formContainer = document.querySelector('form.search-form');
        const saveButton = document.createElement('button');
        saveButton.innerHTML = 'Buscar e Salvar 1080p (PT-BR)';
        saveButton.className = 'btn btn-primary';
        saveButton.style.marginLeft = '10px';
        saveButton.addEventListener('click', startSearchAndSave);

        if (formContainer) {
            const buttonGroup = formContainer.querySelector('.input-group');
            if (buttonGroup) buttonGroup.appendChild(saveButton);
            else formContainer.appendChild(saveButton);
        } else {
            Object.assign(saveButton.style, {
                position: 'fixed', top: '15px', right: '15px', zIndex: '9999'
            });
            document.body.appendChild(saveButton);
        }
    }

    function startSearchAndSave() {
        const searchTerm = prompt('Digite o termo para buscar e salvar:', '');
        if (searchTerm === null || searchTerm.trim() === '') {
            return; // Sai se o usuário cancelar ou não digitar nada
        }

        if (confirm(`Isso iniciará uma nova busca por "${searchTerm}" e irá navegar por todas as páginas de resultados para coletar os dados. Deseja continuar?`)) {
            sessionStorage.setItem(IS_SCRAPING_KEY, 'true');
            sessionStorage.setItem(RESULTS_KEY, JSON.stringify([]));
            sessionStorage.setItem(SEARCH_TERM_KEY, searchTerm);

            // Navega para a primeira página dos resultados da nova busca
            const searchUrl = `https://nyaa.si/?f=0&c=0_0&q=${encodeURIComponent(searchTerm)}`;
            window.location.href = searchUrl;
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
                    storedResults.push({
                        title: titleElement.textContent.trim(),
                        magnet: magnetLink.href
                    });
                }
            }
        });

        sessionStorage.setItem(RESULTS_KEY, JSON.stringify(storedResults));

        const nextButton = document.querySelector('.pagination li.next a');
        if (nextButton) {
            console.log('Navegando para a próxima página...');
            setTimeout(() => {
                window.location.href = nextButton.href;
            }, 500); // Atraso de 500ms para tornar a navegação visível
        } else {
            console.log('Extração concluída.');
            saveResultsToFile();
            sessionStorage.removeItem(IS_SCRAPING_KEY);
            sessionStorage.removeItem(RESULTS_KEY);
            sessionStorage.removeItem(SEARCH_TERM_KEY);
        }
    }

    function saveResultsToFile() {
        const results = JSON.parse(sessionStorage.getItem(RESULTS_KEY) || '[]');
        if (results.length === 0) {
            alert('Nenhum resultado encontrado para salvar.');
            return;
        }

        let fileContent = 'Resultados da Busca Nyaa.si (1080p PT-BR)\n\n';
        results.forEach(item => {
            fileContent += `Título: ${item.title}\n`;
            fileContent += `Magnet Link: ${item.magnet}\n\n`;
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

        alert(`Resultados salvos com sucesso em "${fileName}"!`);
    }

    function initialize() {
        addButton();
        if (sessionStorage.getItem(IS_SCRAPING_KEY) === 'true') {
            scrapeCurrentPageAndContinue();
        }
    }

    if (document.readyState === 'complete') {
        initialize();
    } else {
        window.addEventListener('load', initialize);
    }

})();
