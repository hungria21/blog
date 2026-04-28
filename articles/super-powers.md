---
title: Super Poderes do Blog Moonshot
date: 2024-05-23
---

# Turbocharge seu conteúdo

Este guia demonstra como utilizar os componentes avançados que criamos para superar as limitações do Markdown padrão.

## 1. Menus Expansíveis Personalizados
Agora os menus de detalhes possuem ícones animados e um design minimalista.

<details>
<summary>O que há de novo no motor de renderização?</summary>
<div class="details-content">
Implementamos uma camada de CSS personalizada que intercepta as tags HTML padrão e aplica o estilo Moonshot AI, garantindo que o conteúdo seja legível e elegante em qualquer dispositivo.
</div>
</details>

<details>
<summary>Como usar classes personalizadas?</summary>
<div class="details-content">
Você pode envolver blocos de conteúdo em tags `div` com classes específicas definidas em nosso arquivo `blog.css`.
</div>
</details>

## 2. Caixas de Destaque (Callouts)
Use estas caixas para chamar a atenção do leitor para informações importantes.

<div class="callout callout-info">
    <span class="callout-icon">ℹ️</span>
    <div>
        <strong>Dica de Produtividade:</strong> Use o modo escuro para reduzir a fadiga ocular durante longas sessões de leitura.
    </div>
</div>

<div class="callout callout-warning">
    <span class="callout-icon">⚠️</span>
    <div>
        <strong>Atenção:</strong> Sempre verifique se o arquivo `manifest.json` está atualizado ao subir novos artigos.
    </div>
</div>

<div class="callout callout-success">
    <span class="callout-icon">✅</span>
    <div>
        <strong>Sucesso:</strong> Seu blog agora suporta componentes avançados e renderização ultra-rápida.
    </div>
</div>

## 3. Grids de Imagens Responsivas
Perfeito para criar galerias ou mostrar capturas de tela lado a lado.

<div class="image-grid">
    <img src="https://picsum.photos/seed/a/800/600" alt="Exemplo 1">
    <img src="https://picsum.photos/seed/b/800/600" alt="Exemplo 2">
</div>

## 4. Estilos de Texto Avançados
Você pode usar HTML diretamente para criar layouts mais complexos:

<div style="background: rgba(255,255,255,0.05); padding: 2rem; border-radius: 16px; border: 1px dashed rgba(255,255,255,0.1);">
    <h3 style="margin-top: 0;">Bloco de Conteúdo Isolado</h3>
    <p>Este parágrafo está dentro de um container HTML estilizado diretamente no Markdown.</p>
</div>

---
*Fim do guia de Super Poderes.*
