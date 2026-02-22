// State Management
const state = {
    files: [],
    currentTab: 'files',
    blocks: [
        {
            category: 'Evento',
            color: '#ff4d4d',
            icon: 'fa-bolt',
            description: 'Gatilhos que iniciam a execução da lógica.',
            items: [
                { name: 'Ao Iniciar Jogo', desc: 'Acionado quando a partida começa.' },
                { name: 'Ao Entrar Jogador', desc: 'Acionado quando um jogador entra no mapa.' },
                { name: 'Ao Eliminar', desc: 'Acionado quando um jogador elimina outro.' },
                { name: 'Temporizador', desc: 'Acionado após um intervalo de tempo.' }
            ]
        },
        {
            category: 'Ação',
            color: '#4dff4d',
            icon: 'fa-play',
            description: 'Instruções que alteram o estado do jogo ou entidades.',
            items: [
                { name: 'Teletransportar', desc: 'Move uma entidade para uma posição.' },
                { name: 'Dar Item', desc: 'Adiciona um item ao inventário do jogador.' },
                { name: 'Definir PV', desc: 'Altera os pontos de vida de um jogador.' },
                { name: 'Exibir Mensagem', desc: 'Mostra um texto na tela para o jogador.' }
            ]
        },
        {
            category: 'Dados',
            color: '#4da6ff',
            icon: 'fa-database',
            description: 'Blocos que retornam informações específicas.',
            items: [
                { name: 'Posição do Jogador', desc: 'Coordenadas X, Y, Z do jogador.' },
                { name: 'Nome do Jogador', desc: 'Retorna o apelido do jogador.' },
                { name: 'Contagem de Jogadores', desc: 'Número total de jogadores vivos.' }
            ]
        },
        {
            category: 'Lógica',
            color: '#ffcc00',
            icon: 'fa-code-branch',
            description: 'Controle de fluxo e comparações.',
            items: [
                { name: 'Se / Então', desc: 'Executa blocos se uma condição for verdadeira.' },
                { name: 'Comparar', desc: 'Verifica se dois valores são iguais, maiores ou menores.' },
                { name: 'E / Ou', desc: 'Combina múltiplas condições lógicas.' }
            ]
        },
        {
            category: 'Variável',
            color: '#bc13fe',
            icon: 'fa-box',
            description: 'Armazenamento de dados personalizados.',
            items: [
                { name: 'Definir Variável', desc: 'Atribui um valor a um nome.' },
                { name: 'Obter Variável', desc: 'Recupera o valor armazenado.' },
                { name: 'Modificar Variável', desc: 'Soma ou subtrai valores de uma variável numérica.' }
            ]
        },
        {
            category: 'Jogo',
            color: '#ff4da6',
            icon: 'fa-gamepad',
            description: 'Configurações e estados globais da partida.',
            items: [
                { name: 'Encerrar Partida', desc: 'Finaliza o jogo imediatamente.' },
                { name: 'Definir Tempo', desc: 'Altera o cronômetro da rodada.' },
                { name: 'Alterar Equipe', desc: 'Muda a equipe de um jogador.' }
            ]
        },
        {
            category: 'Função',
            color: '#00ffcc',
            icon: 'fa-vial',
            description: 'Blocos para criar lógica reutilizável.',
            items: [
                { name: 'Definir Função', desc: 'Cria um novo bloco de função.' },
                { name: 'Chamar Função', desc: 'Executa uma função definida anteriormente.' },
                { name: 'Retornar', desc: 'Envia um valor de volta para quem chamou.' }
            ]
        }
    ]
};

// DOM Elements
const dropzone = document.getElementById('dropzone');
const fileInput = document.getElementById('fileInput');
const fileGrid = document.getElementById('file-grid');
const fileCount = document.getElementById('file-count');
const statusContainer = document.getElementById('status-container');
const tabFiles = document.getElementById('tab-files');
const tabBlocks = document.getElementById('tab-blocks');
const viewFiles = document.getElementById('view-files');
const viewBlocks = document.getElementById('view-blocks');
const modal = document.getElementById('modal');
const closeModal = document.getElementById('close-modal');
const modalContent = document.getElementById('modal-content');
const modalTitle = document.getElementById('modal-title');

// Initialization
function init() {
    setupEventListeners();
    renderBlocks();
}

function setupEventListeners() {
    // Tab Switching
    tabFiles.addEventListener('click', () => switchTab('files'));
    tabBlocks.addEventListener('click', () => switchTab('blocks'));

    // Drag and Drop
    dropzone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropzone.classList.add('border-cyan-500', 'bg-cyan-500/10');
    });

    dropzone.addEventListener('dragleave', () => {
        dropzone.classList.remove('border-cyan-500', 'bg-cyan-500/10');
    });

    dropzone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropzone.classList.remove('border-cyan-500', 'bg-cyan-500/10');
        handleFiles(e.dataTransfer.files);
    });

    fileInput.addEventListener('change', (e) => {
        handleFiles(e.target.files);
    });

    // Mobile Sidebar Toggle
    const toggleBtn = document.getElementById('toggle-sidebar');
    const uploadControls = document.getElementById('upload-controls');
    if (toggleBtn) {
        toggleBtn.addEventListener('click', () => {
            uploadControls.classList.toggle('hidden');
            toggleBtn.querySelector('i').classList.toggle('fa-chevron-down');
            toggleBtn.querySelector('i').classList.toggle('fa-chevron-up');
        });
    }

    // Modal
    closeModal.addEventListener('click', () => {
        modal.classList.add('hidden');
    });

    window.addEventListener('click', (e) => {
        if (e.target === modal) modal.classList.add('hidden');
    });
}

function switchTab(tab) {
    state.currentTab = tab;
    if (tab === 'files') {
        tabFiles.classList.add('tab-active');
        tabFiles.classList.remove('text-gray-400');
        tabBlocks.classList.remove('tab-active');
        tabBlocks.classList.add('text-gray-400');
        viewFiles.classList.remove('hidden');
        viewBlocks.classList.add('hidden');
    } else {
        tabBlocks.classList.add('tab-active');
        tabBlocks.classList.remove('text-gray-400');
        tabFiles.classList.remove('tab-active');
        tabFiles.classList.add('text-gray-400');
        viewBlocks.classList.remove('hidden');
        viewFiles.classList.add('hidden');
    }
}

function renderBlocks() {
    const container = document.getElementById('blocks-container');
    container.innerHTML = '';

    state.blocks.forEach(cat => {
        const catEl = document.createElement('div');
        catEl.className = 'space-y-4';
        catEl.innerHTML = `
            <div class="flex items-center space-x-3">
                <div class="p-2 rounded bg-opacity-20" style="background-color: ${cat.color}">
                    <i class="fas ${cat.icon} text-lg" style="color: ${cat.color}"></i>
                </div>
                <div>
                    <h3 class="text-xl font-bold">${cat.category}</h3>
                    <p class="text-xs text-gray-500">${cat.description}</p>
                </div>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                ${cat.items.map(item => `
                    <div class="p-4 bg-card-bg border border-gray-800 rounded-lg hover:border-gray-600 transition group cursor-help">
                        <h4 class="font-bold text-sm mb-1 group-hover:text-white transition" style="color: ${cat.color}">${item.name}</h4>
                        <p class="text-xs text-gray-400">${item.desc}</p>
                    </div>
                `).join('')}
            </div>
        `;
        container.appendChild(catEl);
    });
}

// Logic for handling files
async function handleFiles(fileList) {
    if (typeof JSZip === 'undefined' || typeof pako === 'undefined') {
        addStatus("Erro: Bibliotecas externas (JSZip/Pako) não carregadas. Verifique sua conexão.", "error");
        return;
    }

    const files = Array.from(fileList);
    if (files.length === 0) return;

    addStatus(`Iniciando análise de ${files.length} itens...`);
    showProgress(0);

    try {
        for (let i = 0; i < files.length; i++) {
            const file = files[i];
            if (file.name.endsWith('.zip')) {
                await processZip(file);
            } else {
                await processFile(file);
            }
            showProgress(((i + 1) / files.length) * 100);
        }
        addStatus(`Análise concluída. Total de arquivos: ${state.files.length}`, 'success');
    } catch (error) {
        console.error("Erro no processamento:", error);
        addStatus(`Erro fatal: ${error.message}`, 'error');
    } finally {
        renderFileList();
        setTimeout(() => hideProgress(), 1000);
    }
}

async function processZip(zipFile) {
    addStatus(`Extraindo ZIP: ${zipFile.name}...`);
    try {
        const zip = await JSZip.loadAsync(zipFile);
        const entries = Object.keys(zip.files);

        for (let name of entries) {
            const entry = zip.files[name];
            if (!entry.dir) {
                const content = await entry.async('uint8array');
                await processFile({
                    name: name,
                    size: content.length,
                    content: content,
                    fromZip: true
                });
            }
        }
    } catch (e) {
        addStatus(`Erro ao processar ZIP ${zipFile.name}: ${e.message}`, 'error');
    }
}

async function processFile(fileOrData) {
    let name, size, data;

    if (fileOrData instanceof File) {
        name = fileOrData.name;
        size = fileOrData.size;
        data = new Uint8Array(await fileOrData.arrayBuffer());
    } else {
        name = fileOrData.name;
        size = fileOrData.size;
        data = fileOrData.content;
    }

    addStatus(`Processando: ${name}...`);

    const fileObj = {
        id: Math.random().toString(36).substr(2, 9),
        name: name,
        size: size,
        raw: data,
        type: getFileType(name),
        decoded: null,
        preview: null
    };

    // Decode logic
    try {
        if (fileObj.type === 'bytes') {
            await decodeBytesFile(fileObj);
        } else if (fileObj.type === 'text') {
            fileObj.decoded = new TextDecoder().decode(fileObj.raw);
        }
    } catch (e) {
        addStatus(`Aviso: Falha ao decodificar ${name}: ${e.message}`, 'warning');
    }

    state.files.push(fileObj);
}

async function decodeBytesFile(file) {
    const data = file.raw;

    // Check if it's a ProjectData (GZIP at offset 6)
    if (data.length > 6 && data[6] === 0x1F && data[7] === 0x8B) {
        addStatus(`Detectado GZIP em ${file.name} (offset 6). Descomprimindo...`);
        try {
            const compressed = data.slice(6);
            const decompressed = pako.inflate(compressed);
            file.decoded = new TextDecoder().decode(decompressed);
            addStatus(`Sucesso: ${file.name} descomprimido.`);
        } catch (e) {
            addStatus(`Erro GZIP em ${file.name}: ${e.message}`);
        }
    }
    // Check for SceneReview (Embedded PNGs)
    else if (file.name.includes('SceneReview')) {
        addStatus(`Buscando imagens em ${file.name}...`);
        extractPNGs(file);
    }
}

function extractPNGs(file) {
    const data = file.raw;
    const pngSignature = [0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A];
    let found = 0;

    for (let i = 0; i < data.length - 8; i++) {
        let match = true;
        for (let j = 0; j < 8; j++) {
            if (data[i + j] !== pngSignature[j]) {
                match = false;
                break;
            }
        }

        if (match) {
            // Find IEND chunk to determine end of PNG
            const endSign = [0x49, 0x45, 0x4E, 0x44, 0xAE, 0x42, 0x60, 0x82];
            let endIdx = -1;
            for (let k = i; k < data.length - 8; k++) {
                let endMatch = true;
                for (let l = 0; l < 8; l++) {
                    if (data[k + l] !== endSign[l]) {
                        endMatch = false;
                        break;
                    }
                }
                if (endMatch) {
                    endIdx = k + 8;
                    break;
                }
            }

            if (endIdx !== -1) {
                const pngData = data.slice(i, endIdx);
                const blob = new Blob([pngData], { type: 'image/png' });
                const url = URL.createObjectURL(blob);

                // For now, let's add it as a new "extracted" file
                state.files.push({
                    id: Math.random().toString(36).substr(2, 9),
                    name: `${file.name}_image_${found + 1}.png`,
                    size: pngData.length,
                    raw: pngData,
                    type: 'image',
                    preview: url,
                    decoded: 'Imagem extraída de ' + file.name
                });
                found++;
                i = endIdx; // Skip to end of this PNG
            }
        }
    }
    addStatus(`${found} imagens extraídas de ${file.name}.`);
}

function getFileType(name) {
    const ext = name.split('.').pop().toLowerCase();
    if (ext === 'bytes') return 'bytes';
    if (['png', 'jpg', 'jpeg', 'webp'].includes(ext)) return 'image';
    if (['json', 'txt', 'xml'].includes(ext)) return 'text';
    return 'unknown';
}

function renderFileList() {
    try {
    fileGrid.innerHTML = '';
    fileCount.innerText = `${state.files.length} arquivos`;

    state.files.forEach(file => {
        const card = document.createElement('div');
        card.className = 'bg-card-bg border border-gray-800 rounded-lg p-4 hover:border-cyan-500/50 transition cursor-pointer group relative overflow-hidden';
        card.onclick = () => viewFile(file.id);

        let icon = 'fa-file';
        let colorClass = 'text-gray-400';

        if (file.type === 'bytes') { icon = 'fa-microchip'; colorClass = 'text-purple-400'; }
        if (file.type === 'image') { icon = 'fa-image'; colorClass = 'text-blue-400'; }
        if (file.type === 'text') { icon = 'fa-file-alt'; colorClass = 'text-green-400'; }

        const isDecoded = file.decoded !== null || file.preview !== null;

        card.innerHTML = `
            ${file.preview ? `<div class="h-24 -mx-4 -mt-4 mb-3 bg-black flex items-center justify-center overflow-hidden"><img src="${file.preview}" class="w-full h-full object-cover opacity-60 group-hover:opacity-100 transition"></div>` : ''}
            <div class="flex items-center space-x-3">
                <div class="w-10 h-10 rounded bg-gray-900 flex items-center justify-center ${colorClass} shrink-0">
                    <i class="fas ${icon} text-lg"></i>
                </div>
                <div class="flex-1 min-w-0">
                    <p class="file-name text-sm font-bold truncate group-hover:text-cyan-400 transition"></p>
                    <div class="flex items-center space-x-2 mt-1">
                        <span class="text-[10px] text-gray-500 bg-black/50 px-1 rounded border border-gray-800 uppercase">${file.type}</span>
                        <span class="text-[10px] text-gray-500">${formatSize(file.size)}</span>
                        ${isDecoded ? '<span class="text-[10px] text-cyan-500 font-bold"><i class="fas fa-check-circle"></i> DEC</span>' : ''}
                    </div>
                </div>
            </div>
            <div class="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition">
                <button onclick="event.stopPropagation(); deleteFile('${file.id}')" class="text-gray-500 hover:text-red-500 p-1"><i class="fas fa-trash text-[10px]"></i></button>
            </div>
        `;
        card.querySelector('.file-name').textContent = file.name;
        fileGrid.appendChild(card);
    });
    } catch (e) {
        console.error("Error in renderFileList:", e);
    }
}

function deleteFile(id) {
    const file = state.files.find(f => f.id === id);
    if (file && file.preview) {
        URL.revokeObjectURL(file.preview);
    }
    state.files = state.files.filter(f => f.id !== id);
    renderFileList();
}

function formatSize(bytes) {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function viewFile(id) {
    const file = state.files.find(f => f.id === id);
    if (!file) return;

    modalTitle.textContent = `Visualizando: ${file.name}`;
    modalContent.innerHTML = '';
    modal.classList.remove('hidden');

    if (file.type === 'image') {
        const img = document.createElement('img');
        img.src = file.preview || URL.createObjectURL(new Blob([file.raw]));
        img.className = 'max-w-full h-auto mx-auto';
        modalContent.appendChild(img);
    } else {
        const pre = document.createElement('pre');
        pre.className = 'text-cyan-400 bg-black p-4 rounded overflow-x-auto h-full';

        let content = file.decoded || `Conteúdo Binário (${file.size} bytes)\n\nDados brutos (HEX):\n${toHex(file.raw.slice(0, 512))}...`;

        try {
            // Tenta formatar se for JSON
            if (content.trim().startsWith('{') || content.trim().startsWith('[')) {
                const obj = JSON.parse(content);
                content = JSON.stringify(obj, null, 4);
            }
        } catch (e) {}

        pre.innerText = content;
        modalContent.appendChild(pre);
    }
}

function toHex(buffer) {
    return Array.from(new Uint8Array(buffer))
        .map(b => b.toString(16).padStart(2, '0'))
        .join(' ');
}

function showProgress(percent) {
    const bar = document.getElementById('progress-bar');
    const fill = document.getElementById('progress-fill');
    if (bar) bar.classList.remove('hidden');
    if (fill) fill.style.width = `${percent}%`;
}

function hideProgress() {
    const bar = document.getElementById('progress-bar');
    if (bar) bar.classList.add('hidden');
}

function addStatus(msg, type = 'info') {
    const el = document.createElement('div');
    el.className = `p-2 rounded border border-gray-800 bg-black/30 mb-2 flex items-center`;
    const time = new Date().toLocaleTimeString();

    const timeSpan = document.createElement('span');
    timeSpan.className = 'text-gray-600 mr-2';
    timeSpan.textContent = `[${time}]`;

    const msgSpan = document.createElement('span');
    msgSpan.textContent = msg;

    el.appendChild(timeSpan);
    el.appendChild(msgSpan);
    statusContainer.prepend(el);
}

init();
