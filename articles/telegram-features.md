---

title: "Showcase de Expandir/Encolher (HTML no Markdown)"
description: "Demonstra diferentes formas de criar seções expansíveis usando HTML dentro do Markdown."
image: "https://picsum.photos/seed/expand/800/450"
date: "2024-05-20"

🔽 Expandir / Encolher no Markdown (HTML)

Este arquivo mostra várias formas de criar conteúdo colapsável usando HTML dentro do ".md".

---

🔹 1. Básico (padrão)

<details>
  <summary>📂 Clique para abrir</summary>Conteúdo simples escondido.

</details>---

🔹 2. Aberto por padrão

<details open>
  <summary>📂 Já começa aberto</summary>Esse conteúdo já aparece expandido.

</details>---

🔹 3. Com Markdown dentro

<details>
  <summary>🧠 Conteúdo com Markdown</summary>Título interno

- Lista
- Dentro do dropdown

Negrito aqui

</details>---

🔹 4. Estilo Dark

<details style="background:#111; padding:12px; border-radius:10px; margin-bottom:10px;">
  <summary style="cursor:pointer; font-weight:bold;">
    🌙 Dark Mode
  </summary>  <div style="margin-top:10px;">
    Conteúdo com estilo escuro.
  </div></details>---

🔹 5. Estilo Card

<details style="border:1px solid #333; padding:12px; border-radius:12px;">
  <summary style="font-size:16px; font-weight:bold;">
    📦 Card expansível
  </summary>  <div style="margin-top:10px;">
    Parece um card moderno.
  </div></details>---

🔹 6. Ícone animado (simulado)

<details>
  <summary>▶️ Clique para expandir</summary>▼ Agora está aberto

</details>---

🔹 7. FAQ (perguntas e respostas)

<details>
  <summary>❓ O que é isso?</summary>É uma seção expansível.

</details><details>
  <summary>❓ Funciona no GitHub?</summary>Sim, funciona perfeitamente.

</details>---

🔹 8. Nested (dentro de outro)

<details>
  <summary>📁 Categoria</summary>  <details>
    <summary>📄 Subitem</summary>Conteúdo dentro de outro dropdown.

  </details></details>---

🔹 9. Com código

<details>
  <summary>💻 Mostrar código</summary><details>
  <summary>Título</summary>
  Conteúdo
</details>

</details>---

🔹 10. Com imagem

<details>
  <summary>🖼️ Ver imagem</summary>"Imagem" (https://picsum.photos/300/200)

</details>---

🔹 11. Bloco destacado

<details style="background:#1a1a1a; border-left:4px solid #00ffcc; padding:10px;">
  <summary>✨ Destaque</summary>Conteúdo importante destacado.

</details>---

🔹 12. Grande (tipo seção de artigo)

<details>
  <summary>📚 Ler mais</summary>Lorem ipsum dolor sit amet, consectetur adipiscing elit.
Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.

</details>---

🎯 Conclusão

Você pode criar:

- Dropdown simples
- FAQ
- Cards
- Nested
- Estilizados

Tudo usando apenas:

<details>
  <summary>Título</summary>
  Conteúdo
</details>

---

<details>
  <summary>Clique aqui</summary>
  Conteúdo escondido
</details>