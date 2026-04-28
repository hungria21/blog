---
title: "Bem-vindo ao Blog Moonshot"
description: "Uma introdução ao nosso novo espaço para compartilhar conhecimento e ideias sobre IA e tecnologia."
image: "https://picsum.photos/seed/intro/800/450"
date: "2024-05-21"
---


<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,400&family=DM+Sans:wght@300;400;500&family=JetBrains+Mono:wght@400;600&display=swap');

  :root {
    --bg: #0d0d0f;
    --surface: #16161a;
    --surface2: #1e1e24;
    --border: #2a2a32;
    --accent: #e8c547;
    --accent2: #ff6b4a;
    --text: #e8e6e0;
    --muted: #7a7880;
    --code-bg: #111115;
  }

  * { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    background: var(--bg);
    color: var(--text);
    font-family: 'DM Sans', sans-serif;
    font-weight: 300;
    line-height: 1.8;
    padding: 0;
  }

  /* ── HERO ── */
  .hero {
    position: relative;
    padding: 72px 40px 56px;
    border-bottom: 1px solid var(--border);
    overflow: hidden;
  }
  .hero::before {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse 80% 60% at 70% 40%, #e8c54714, transparent 70%),
                radial-gradient(ellipse 50% 80% at 10% 80%, #ff6b4a0a, transparent 60%);
    pointer-events: none;
  }
  .hero-meta {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 24px;
    font-size: 0.75rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--muted);
  }
  .hero-meta .dot { width: 4px; height: 4px; border-radius: 50%; background: var(--border); }
  .tag {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 2px;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }
  .tag-yellow { background: #e8c5471a; color: var(--accent); border: 1px solid #e8c54730; }
  .tag-red    { background: #ff6b4a14; color: var(--accent2); border: 1px solid #ff6b4a30; }
  .tag-blue   { background: #4a90ff14; color: #7ab3ff; border: 1px solid #4a90ff30; }

  .hero h1 {
    font-family: 'Playfair Display', serif;
    font-weight: 700;
    font-size: clamp(2rem, 5vw, 3.5rem);
    line-height: 1.15;
    max-width: 720px;
    margin-bottom: 20px;
  }
  .hero h1 em { font-style: italic; color: var(--accent); }
  .hero-sub {
    max-width: 580px;
    color: var(--muted);
    font-size: 1.05rem;
    margin-bottom: 32px;
  }
  .hero-stats {
    display: flex;
    gap: 32px;
    flex-wrap: wrap;
  }
  .stat { display: flex; flex-direction: column; gap: 2px; }
  .stat-val { font-size: 1.3rem; font-weight: 500; color: var(--text); }
  .stat-label { font-size: 0.7rem; letter-spacing: 0.1em; text-transform: uppercase; color: var(--muted); }

  /* ── MAIN LAYOUT ── */
  .container { max-width: 820px; margin: 0 auto; padding: 48px 40px; }

  /* ── HEADINGS ── */
  h2 {
    font-family: 'Playfair Display', serif;
    font-size: 1.6rem;
    font-weight: 700;
    margin: 48px 0 16px;
    color: var(--text);
  }
  h3 {
    font-size: 1rem;
    font-weight: 500;
    letter-spacing: 0.05em;
    margin: 28px 0 12px;
    color: var(--text);
  }
  p { margin-bottom: 16px; color: #c8c6c0; }

  /* ── DIVIDER ── */
  .divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border) 20%, var(--border) 80%, transparent);
    margin: 40px 0;
  }

  /* ══════════════════════════════════
     COMPONENTE 1 — ACCORDION
  ══════════════════════════════════ */
  .accordion-group { display: flex; flex-direction: column; gap: 2px; margin: 24px 0; }

  .accordion-item {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 6px;
    overflow: hidden;
    transition: border-color 0.2s;
  }
  .accordion-item.open { border-color: #e8c54740; }

  .accordion-trigger {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px 20px;
    cursor: pointer;
    user-select: none;
    gap: 16px;
    background: none;
    border: none;
    width: 100%;
    text-align: left;
    color: var(--text);
    font-family: 'DM Sans', sans-serif;
    font-size: 0.95rem;
    font-weight: 500;
  }
  .accordion-trigger:hover { background: #ffffff06; }

  .accordion-left { display: flex; align-items: center; gap: 14px; }
  .accordion-icon {
    width: 30px; height: 30px; flex-shrink: 0;
    background: #e8c5471a;
    border: 1px solid #e8c54728;
    border-radius: 6px;
    display: grid; place-items: center;
    font-size: 0.9rem;
  }

  /* SETA PERSONALIZADA SVG */
  .accordion-arrow {
    width: 28px; height: 28px; flex-shrink: 0;
    position: relative;
    transition: transform 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);
  }
  .accordion-arrow svg {
    width: 100%; height: 100%;
  }
  .accordion-arrow .arrow-shaft {
    stroke: var(--accent);
    stroke-width: 2;
    stroke-linecap: round;
    transition: stroke-dashoffset 0.3s ease;
  }
  .accordion-arrow .arrow-head {
    fill: var(--accent);
    transition: transform 0.3s ease;
    transform-origin: center;
  }
  .accordion-item.open .accordion-arrow { transform: rotate(180deg); }

  .accordion-body {
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  }
  .accordion-item.open .accordion-body { max-height: 600px; }

  .accordion-content {
    padding: 0 20px 20px 64px;
    color: #a8a6a0;
    font-size: 0.9rem;
    line-height: 1.75;
    border-top: 1px solid var(--border);
    padding-top: 16px;
  }
  .accordion-content ul { padding-left: 18px; }
  .accordion-content li { margin-bottom: 6px; }
  .accordion-content li::marker { color: var(--accent); }

  /* ══════════════════════════════════
     COMPONENTE 2 — TABS
  ══════════════════════════════════ */
  .tabs { margin: 24px 0; }
  .tab-list {
    display: flex;
    gap: 0;
    border-bottom: 1px solid var(--border);
    overflow-x: auto;
    scrollbar-width: none;
  }
  .tab-list::-webkit-scrollbar { display: none; }
  .tab-btn {
    padding: 10px 20px;
    background: none;
    border: none;
    border-bottom: 2px solid transparent;
    color: var(--muted);
    font-family: 'DM Sans', sans-serif;
    font-size: 0.82rem;
    font-weight: 500;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    cursor: pointer;
    white-space: nowrap;
    transition: color 0.2s, border-color 0.2s;
    margin-bottom: -1px;
  }
  .tab-btn:hover { color: var(--text); }
  .tab-btn.active { color: var(--accent); border-bottom-color: var(--accent); }

  .tab-panel { display: none; padding: 24px 0; }
  .tab-panel.active { display: block; }

  /* ══════════════════════════════════
     COMPONENTE 3 — CODE BLOCK
  ══════════════════════════════════ */
  .code-block {
    background: var(--code-bg);
    border: 1px solid var(--border);
    border-radius: 8px;
    overflow: hidden;
    margin: 20px 0;
    position: relative;
  }
  .code-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 16px;
    background: #ffffff05;
    border-bottom: 1px solid var(--border);
  }
  .code-lang {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--muted);
  }
  .copy-btn {
    background: none;
    border: 1px solid var(--border);
    border-radius: 4px;
    color: var(--muted);
    font-size: 0.72rem;
    padding: 3px 10px;
    cursor: pointer;
    font-family: 'DM Sans', sans-serif;
    letter-spacing: 0.05em;
    transition: all 0.2s;
  }
  .copy-btn:hover { border-color: var(--accent); color: var(--accent); }
  .copy-btn.copied { border-color: #4ade80; color: #4ade80; }
  pre {
    padding: 20px;
    overflow-x: auto;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    line-height: 1.7;
    color: #d0cec8;
  }
  .kw { color: #ff6b4a; }
  .fn { color: #e8c547; }
  .str { color: #7dd3a8; }
  .cm { color: #555560; font-style: italic; }
  .num { color: #9b8fff; }

  /* ══════════════════════════════════
     COMPONENTE 4 — PROGRESS / SKILLS
  ══════════════════════════════════ */
  .skill-list { display: flex; flex-direction: column; gap: 14px; margin: 24px 0; }
  .skill-row { display: flex; flex-direction: column; gap: 6px; }
  .skill-meta {
    display: flex;
    justify-content: space-between;
    font-size: 0.8rem;
    font-weight: 500;
    letter-spacing: 0.04em;
  }
  .skill-pct { color: var(--muted); font-family: 'JetBrains Mono', monospace; }
  .progress-track {
    height: 4px;
    background: var(--surface2);
    border-radius: 99px;
    overflow: hidden;
  }
  .progress-fill {
    height: 100%;
    border-radius: 99px;
    width: 0%;
    transition: width 1s cubic-bezier(0.4, 0, 0.2, 1);
  }
  .fill-yellow { background: linear-gradient(90deg, #c8a520, var(--accent)); }
  .fill-red    { background: linear-gradient(90deg, #cc4422, var(--accent2)); }
  .fill-blue   { background: linear-gradient(90deg, #2255cc, #7ab3ff); }
  .fill-green  { background: linear-gradient(90deg, #228844, #4ade80); }

  /* ══════════════════════════════════
     COMPONENTE 5 — CALLOUT
  ══════════════════════════════════ */
  .callout {
    display: flex;
    gap: 14px;
    padding: 16px 18px;
    border-radius: 6px;
    margin: 24px 0;
    font-size: 0.9rem;
    line-height: 1.65;
  }
  .callout-info { background: #4a90ff10; border-left: 3px solid #4a90ff; color: #a8c8ff; }
  .callout-warn { background: #e8c54710; border-left: 3px solid var(--accent); color: #d4b240; }
  .callout-danger { background: #ff6b4a10; border-left: 3px solid var(--accent2); color: #ff9f88; }
  .callout-icon { font-size: 1.1rem; flex-shrink: 0; margin-top: 1px; }

  /* ══════════════════════════════════
     COMPONENTE 6 — TOOLTIP
  ══════════════════════════════════ */
  .tooltip-wrap { position: relative; display: inline-block; }
  .tooltip-word {
    color: var(--accent);
    text-decoration: underline dotted var(--accent);
    cursor: help;
    font-weight: 500;
  }
  .tooltip-box {
    position: absolute;
    bottom: 130%; left: 50%;
    transform: translateX(-50%) translateY(4px);
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 0.78rem;
    color: var(--text);
    white-space: nowrap;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.2s, transform 0.2s;
    z-index: 10;
    box-shadow: 0 8px 24px #00000060;
  }
  .tooltip-box::after {
    content: '';
    position: absolute;
    top: 100%; left: 50%;
    transform: translateX(-50%);
    border: 5px solid transparent;
    border-top-color: var(--border);
  }
  .tooltip-wrap:hover .tooltip-box {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
  }

  /* ══════════════════════════════════
     COMPONENTE 7 — READING PROGRESS
  ══════════════════════════════════ */
  #reading-progress {
    position: fixed;
    top: 0; left: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    width: 0%;
    z-index: 100;
    transition: width 0.1s linear;
  }

  /* ══════════════════════════════════
     COMPONENTE 8 — TIMELINE
  ══════════════════════════════════ */
  .timeline { position: relative; padding-left: 24px; margin: 24px 0; }
  .timeline::before {
    content: '';
    position: absolute;
    left: 6px; top: 8px; bottom: 8px;
    width: 1px;
    background: linear-gradient(180deg, var(--accent), var(--accent2), transparent);
  }
  .timeline-item { position: relative; margin-bottom: 24px; }
  .timeline-dot {
    position: absolute;
    left: -21px; top: 6px;
    width: 10px; height: 10px;
    border-radius: 50%;
    background: var(--accent);
    border: 2px solid var(--bg);
    box-shadow: 0 0 0 1px var(--accent);
  }
  .timeline-item:nth-child(even) .timeline-dot { background: var(--accent2); box-shadow: 0 0 0 1px var(--accent2); }
  .timeline-date { font-size: 0.72rem; letter-spacing: 0.1em; text-transform: uppercase; color: var(--muted); margin-bottom: 4px; }
  .timeline-title { font-weight: 500; font-size: 0.95rem; margin-bottom: 4px; }
  .timeline-desc { font-size: 0.85rem; color: #909098; line-height: 1.6; }

  /* ── FOOTER ── */
  .post-footer {
    margin-top: 64px;
    padding-top: 32px;
    border-top: 1px solid var(--border);
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: gap;
    gap: 16px;
  }
  .author { display: flex; align-items: center; gap: 12px; }
  .avatar {
    width: 40px; height: 40px; border-radius: 50%;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    display: grid; place-items: center;
    font-size: 0.85rem; font-weight: 700; color: var(--bg);
  }
  .author-name { font-size: 0.85rem; font-weight: 500; }
  .author-role { font-size: 0.75rem; color: var(--muted); }
  .share-btn {
    padding: 8px 18px;
    background: none;
    border: 1px solid var(--border);
    border-radius: 4px;
    color: var(--muted);
    font-family: 'DM Sans', sans-serif;
    font-size: 0.8rem;
    font-weight: 500;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    cursor: pointer;
    transition: all 0.2s;
  }
  .share-btn:hover { border-color: var(--accent); color: var(--accent); }
</style>

<div id="reading-progress"></div>

<div class="hero">
  <div class="hero-meta">
    <span class="tag tag-yellow">Tutorial</span>
    <span class="tag tag-red">Frontend</span>
    <span class="tag tag-blue">HTML</span>
    <span class="dot"></span>
    <span>28 abr 2025</span>
    <span class="dot"></span>
    <span>8 min de leitura</span>
  </div>

  <h1>Componentes <em>interativos</em> para o seu blog moderno</h1>

  <p class="hero-sub">
    Um guia completo com acordeões, abas, blocos de código copiáveis, 
    barras de progresso, tooltips e muito mais — tudo em HTML puro.
  </p>

  <div class="hero-stats">
    <div class="stat"><span class="stat-val">8</span><span class="stat-label">Componentes</span></div>
    <div class="stat"><span class="stat-val">0</span><span class="stat-label">Dependências</span></div>
    <div class="stat"><span class="stat-val">CSS</span><span class="stat-label">Animações</span></div>
    <div class="stat"><span class="stat-val">100%</span><span class="stat-label">Responsivo</span></div>
  </div>
</div>

<div class="container">

  <!-- ────────────────────────────────────── -->
  <h2>1 · Acordeão com seta personalizada</h2>
  <p>
    Clique em cada item para expandir o conteúdo. A seta é um 
    <span class="tooltip-wrap">
      <span class="tooltip-word">SVG inline</span>
      <span class="tooltip-box">Scalable Vector Graphics — gráfico vetorial embutido direto no HTML</span>
    </span>
    animado com CSS puro, sem JavaScript para o controle visual.
  </p>

  <div class="accordion-group" id="accordion">

    <div class="accordion-item">
      <button class="accordion-trigger" onclick="toggleAccordion(this)">
        <span class="accordion-left">
          <span class="accordion-icon">🧩</span>
          <span>O que é um componente acordeão?</span>
        </span>
        <span class="accordion-arrow">
          <svg viewBox="0 0 28 28" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="14" cy="14" r="13" stroke="#e8c54730" stroke-width="1"/>
            <path class="arrow-shaft" d="M9 12 L14 17 L19 12"/>
          </svg>
        </span>
      </button>
      <div class="accordion-body">
        <div class="accordion-content">
          Um acordeão é um padrão de interface que mostra e oculta seções de conteúdo. 
          É ideal para <strong>FAQs</strong>, tutoriais e documentação onde o espaço é limitado.
          <ul>
            <li>Reduz o scroll desnecessário</li>
            <li>Organiza informação hierárquica</li>
            <li>Melhora a experiência em mobile</li>
          </ul>
        </div>
      </div>
    </div>

    <div class="accordion-item">
      <button class="accordion-trigger" onclick="toggleAccordion(this)">
        <span class="accordion-left">
          <span class="accordion-icon">🎨</span>
          <span>Como personalizar as cores e a seta?</span>
        </span>
        <span class="accordion-arrow">
          <svg viewBox="0 0 28 28" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="14" cy="14" r="13" stroke="#ff6b4a30" stroke-width="1"/>
            <path class="arrow-shaft" d="M9 12 L14 17 L19 12" stroke="#ff6b4a"/>
          </svg>
        </span>
      </button>
      <div class="accordion-body">
        <div class="accordion-content">
          Basta editar as variáveis CSS em <code>:root</code>. A seta SVG aceita qualquer 
          cor via atributo <code>stroke</code>. A animação de rotação é controlada pela 
          classe <code>.open</code> adicionada via JavaScript:
          <br><br>
          <code>.accordion-item.open .accordion-arrow { transform: rotate(180deg); }</code>
        </div>
      </div>
    </div>

    <div class="accordion-item">
      <button class="accordion-trigger" onclick="toggleAccordion(this)">
        <span class="accordion-left">
          <span class="accordion-icon">⚡</span>
          <span>Posso usar sem JavaScript?</span>
        </span>
        <span class="accordion-arrow">
          <svg viewBox="0 0 28 28" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="14" cy="14" r="13" stroke="#4a90ff30" stroke-width="1"/>
            <path class="arrow-shaft" d="M9 12 L14 17 L19 12" stroke="#7ab3ff"/>
          </svg>
        </span>
      </button>
      <div class="accordion-body">
        <div class="accordion-content">
          Sim! Usando o padrão <code>&lt;details&gt;</code> e <code>&lt;summary&gt;</code> 
          do HTML5 você obtém comportamento nativo de accordion sem nenhum JS. 
          Porém, para transições suaves de altura, um mínimo de JavaScript é necessário.
        </div>
      </div>
    </div>

  </div>

  <div class="divider"></div>

  <!-- ────────────────────────────────────── -->
  <h2>2 · Sistema de Abas</h2>
  <p>Organize conteúdo relacionado em abas — perfeito para comparações e exemplos em múltiplas linguagens.</p>

  <div class="tabs">
    <div class="tab-list" role="tablist">
      <button class="tab-btn active" onclick="switchTab(this, 'tab-html')">HTML</button>
      <button class="tab-btn" onclick="switchTab(this, 'tab-css')">CSS</button>
      <button class="tab-btn" onclick="switchTab(this, 'tab-js')">JavaScript</button>
    </div>

    <div id="tab-html" class="tab-panel active">
      <p>O HTML define a estrutura semântica com atributos <code>role</code> para acessibilidade. Use <code>&lt;button&gt;</code> para os gatilhos das abas.</p>
      <div class="callout callout-info">
        <span class="callout-icon">ℹ</span>
        <span>Adicione <code>aria-selected</code> e <code>tabindex</code> para melhorar a acessibilidade por teclado.</span>
      </div>
    </div>

    <div id="tab-css" class="tab-panel">
      <p>O CSS gerencia a visibilidade com <code>display: none</code> e <code>display: block</code>. A aba ativa recebe uma borda inferior colorida como indicador visual.</p>
      <div class="callout callout-warn">
        <span class="callout-icon">⚠</span>
        <span>Evite usar <code>visibility: hidden</code> — o elemento ainda ocupa espaço no layout.</span>
      </div>
    </div>

    <div id="tab-js" class="tab-panel">
      <p>O JavaScript apenas troca classes <code>active</code> nos botões e painéis. Toda a lógica cabe em menos de 10 linhas.</p>
      <div class="callout callout-danger">
        <span class="callout-icon">✕</span>
        <span>Não use <code>innerHTML</code> para mudar conteúdo de abas — prefira mostrar/ocultar painéis já existentes no DOM.</span>
      </div>
    </div>
  </div>

  <div class="divider"></div>

  <!-- ────────────────────────────────────── -->
  <h2>3 · Bloco de Código com Copiar</h2>

  <div class="code-block">
    <div class="code-header">
      <span class="code-lang">JavaScript</span>
      <button class="copy-btn" onclick="copyCode(this)">Copiar</button>
    </div>
    <pre id="code-sample"><span class="cm">// Função de toggle para o acordeão</span>
<span class="kw">function</span> <span class="fn">toggleAccordion</span>(trigger) {
  <span class="kw">const</span> item = trigger.<span class="fn">closest</span>(<span class="str">'.accordion-item'</span>);
  <span class="kw">const</span> isOpen = item.<span class="fn">classList</span>.<span class="fn">contains</span>(<span class="str">'open'</span>);

  <span class="cm">// Fecha todos os itens abertos</span>
  document.<span class="fn">querySelectorAll</span>(<span class="str">'.accordion-item.open'</span>)
    .<span class="fn">forEach</span>(el => el.<span class="fn">classList</span>.<span class="fn">remove</span>(<span class="str">'open'</span>));

  <span class="cm">// Abre o item clicado (se estava fechado)</span>
  <span class="kw">if</span> (!isOpen) item.<span class="fn">classList</span>.<span class="fn">add</span>(<span class="str">'open'</span>);
}</pre>
  </div>

  <div class="divider"></div>

  <!-- ────────────────────────────────────── -->
  <h2>4 · Barras de Progresso Animadas</h2>
  <p>Útil para mostrar habilidades, progresso de leitura ou métricas de projeto.</p>

  <div class="skill-list" id="skills">
    <div class="skill-row">
      <div class="skill-meta"><span>HTML & CSS</span><span class="skill-pct">95%</span></div>
      <div class="progress-track"><div class="progress-fill fill-yellow" data-pct="95"></div></div>
    </div>
    <div class="skill-row">
      <div class="skill-meta"><span>JavaScript</span><span class="skill-pct">82%</span></div>
      <div class="progress-track"><div class="progress-fill fill-red" data-pct="82"></div></div>
    </div>
    <div class="skill-row">
      <div class="skill-meta"><span>Design de Interface</span><span class="skill-pct">78%</span></div>
      <div class="progress-track"><div class="progress-fill fill-blue" data-pct="78"></div></div>
    </div>
    <div class="skill-row">
      <div class="skill-meta"><span>Acessibilidade Web</span><span class="skill-pct">67%</span></div>
      <div class="progress-track"><div class="progress-fill fill-green" data-pct="67"></div></div>
    </div>
  </div>

  <div class="divider"></div>

  <!-- ────────────────────────────────────── -->
  <h2>5 · Timeline de Conteúdo</h2>

  <div class="timeline">
    <div class="timeline-item">
      <div class="timeline-dot"></div>
      <div class="timeline-date">Janeiro 2025</div>
      <div class="timeline-title">Estrutura base do projeto</div>
      <div class="timeline-desc">Definição da arquitetura de componentes e sistema de design tokens com variáveis CSS.</div>
    </div>
    <div class="timeline-item">
      <div class="timeline-dot"></div>
      <div class="timeline-date">Fevereiro 2025</div>
      <div class="timeline-title">Componentes interativos</div>
      <div class="timeline-desc">Implementação do acordeão, abas e blocos de código com suporte a syntax highlight.</div>
    </div>
    <div class="timeline-item">
      <div class="timeline-dot"></div>
      <div class="timeline-date">Março 2025</div>
      <div class="timeline-title">Animações e micro-interações</div>
      <div class="timeline-desc">Adição de transições suaves, barra de leitura e animações de entrada por scroll.</div>
    </div>
    <div class="timeline-item">
      <div class="timeline-dot"></div>
      <div class="timeline-date">Abril 2025</div>
      <div class="timeline-title">Publicação e documentação</div>
      <div class="timeline-desc">Lançamento público com guia de uso e exemplos de customização para diferentes temas.</div>
    </div>
  </div>

  <!-- ── FOOTER ── -->
  <div class="post-footer">
    <div class="author">
      <div class="avatar">M</div>
      <div>
        <div class="author-name">Marcelo</div>
        <div class="author-role">Desenvolvedor & Designer</div>
      </div>
    </div>
    <button class="share-btn" onclick="sharePost()">↗ Compartilhar</button>
  </div>

</div>

<script>
/* ── Acordeão ── */
function toggleAccordion(trigger) {
  const item = trigger.closest('.accordion-item');
  const isOpen = item.classList.contains('open');
  document.querySelectorAll('.accordion-item.open')
    .forEach(el => el.classList.remove('open'));
  if (!isOpen) item.classList.add('open');
}

/* ── Abas ── */
function switchTab(btn, panelId) {
  btn.closest('.tabs').querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  btn.closest('.tabs').querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
  btn.classList.add('active');
  document.getElementById(panelId).classList.add('active');
}

/* ── Copiar código ── */
function copyCode(btn) {
  const pre = btn.closest('.code-block').querySelector('pre');
  navigator.clipboard.writeText(pre.innerText).then(() => {
    btn.textContent = '✓ Copiado';
    btn.classList.add('copied');
    setTimeout(() => { btn.textContent = 'Copiar'; btn.classList.remove('copied'); }, 2000);
  });
}

/* ── Barra de leitura ── */
window.addEventListener('scroll', () => {
  const doc = document.documentElement;
  const pct = (doc.scrollTop / (doc.scrollHeight - doc.clientHeight)) * 100;
  document.getElementById('reading-progress').style.width = pct + '%';
});

/* ── Barras de progresso ao entrar na viewport ── */
const observer = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.querySelectorAll('.progress-fill').forEach(bar => {
        bar.style.width = bar.dataset.pct + '%';
      });
      observer.unobserve(e.target);
    }
  });
}, { threshold: 0.3 });

const skillEl = document.getElementById('skills');
if (skillEl) observer.observe(skillEl);

/* ── Compartilhar ── */
function sharePost() {
  if (navigator.share) {
    navigator.share({ title: 'Componentes interativos para blog', url: location.href });
  } else {
    navigator.clipboard.writeText(location.href);
    alert('Link copiado!');
  }
}
</script>
