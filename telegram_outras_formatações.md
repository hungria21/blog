# Recursos Adicionais e Formatação Avançada (Telegram 2026)

Este documento lista funcionalidades complementares ao Markdown que foram introduzidas ou expandidas na atualização de 2026 do Telegram.

---

### 1. Novas Entidades de Mensagem
*   **date_time**: Permite formatar datas que se ajustam automaticamente ao fuso horário de quem lê.
*   **member_tag**: Permite marcar usuários em grupos/canais sem necessidade de username público.

---

### 2. Citações Expansíveis
Desde a atualização recente, citações enviadas com a sintaxe `>` podem ser configuradas como expansíveis através do menu de formatação do aplicativo ou via HTML:
*   `<details><summary>Resumo</summary>Conteúdo oculto</details>`

---

### 3. IA Editor e Ferramentas de Texto
O Telegram agora integra ferramentas de Inteligência Artificial que auxiliam na formatação e conteúdo:
*   **AI Summary**: Gera automaticamente resumos de posts longos em canais.
*   **AI Translation**: Tradução instantânea de mensagens mantendo a formatação.
*   **AI Rewrite**: Sugestões para mudar o tom da sua mensagem antes de enviar.

---

### 4. Formatação via HTML (Alternativa)
Se preferir enviar via API ou se o Markdown estiver causando conflitos, use o `parse_mode="HTML"`:
*   `<b>Negrito</b>`
*   `<i>Itálico</i>`
*   `<u>Sublinhado</u>`
*   `<s>Taxado</s>`
*   `<tg-spoiler>Spoiler</tg-spoiler>`
*   `<a href="tg://user?id=123456789">Link por ID</a>`
*   `<blockquote>Citação</blockquote>`
*   `<pre>Código em bloco</pre>`

---

### 5. Liquid Glass Design
A interface agora suporta elementos visuais de "Liquid Glass" no iOS e Android, o que afeta como os balões de chat interagem com fundos transparentes e reflexos, embora não mude a sintaxe do texto em si.

---
*Este arquivo serve como referência técnica para usuários avançados e desenvolvedores de bots.*
