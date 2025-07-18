# Blog Jekyll - hungria21.github.io/blog

Este é um blog minimalista construído com Jekyll e hospedado no GitHub Pages.

## 🚀 Características

- **Design Dark**: Fundo #121212 com tema escuro moderno
- **Menu Lateral**: Navegação deslizante com guias rápidos
- **Responsivo**: Funciona perfeitamente em dispositivos móveis
- **Sem Rodapé**: Layout limpo e minimalista
- **GitHub Pages**: Deploy automático

## 📁 Estrutura do Projeto

```
blog/
├── _config.yml              # Configuração do Jekyll
├── _layouts/
│   ├── default.html         # Layout principal
│   └── post.html           # Layout para posts
├── _includes/               # Componentes reutilizáveis
├── _posts/                 # Posts do blog
│   ├── 2025-07-18-bem-vindo-ao-meu-blog.md
│   └── 2025-07-18-introducao-ao-git-e-github.md
├── _guias/                 # Guias rápidos
│   ├── guia-git-basico.md
│   └── guia-javascript-essencial.md
├── assets/
│   └── css/
│       └── style.scss      # Estilos CSS
├── index.html              # Página principal
└── README.md               # Este arquivo
```

## 🛠️ Instalação e Configuração

### 1. Clonar o Repositório

```bash
git clone https://github.com/hungria21/blog.git
cd blog
```

### 2. Instalar Dependências

```bash
# Instalar Jekyll e Bundler
gem install jekyll bundler

# Criar Gemfile (se não existir)
bundle init
bundle add jekyll
bundle add jekyll-feed
bundle add jekyll-sitemap
```

### 3. Servir Localmente

```bash
# Executar servidor local
bundle exec jekyll serve

# Ou com live reload
bundle exec jekyll serve --livereload
```

Acesse: `http://localhost:4000/blog`

## 📝 Adicionando Conteúdo

### Novo Post

Crie um arquivo em `_posts/` com o formato: `YYYY-MM-DD-titulo.md`

```markdown
---
layout: post
title: "Título do Post"
date: 2025-07-18 10:00:00 -0300
author: "Seu Nome"
description: "Descrição do post"
---

# Conteúdo do Post

Seu conteúdo aqui...
```

### Novo Guia

Crie um arquivo em `_guias/` com o formato: `nome-do-guia.md`

```markdown
---
layout: post
title: "Guia Rápido: Título"
description: "Descrição do guia"
---

# Conteúdo do Guia

Seu conteúdo aqui...
```

## 🎨 Personalização

### Cores

Edite `assets/css/style.scss` para alterar as cores:

```scss
// Cores principais
$background: #121212;
$text: #ffffff;
$accent: #00d4aa;
$card-bg: #1a1a1a;
$border: #2a2a2a;
```

### Configurações do Site

Edite `_config.yml`:

```yaml
title: "Seu Blog"
description: "Sua descrição"
url: "https://seuusuario.github.io"
baseurl: "/blog"
```

## 🚀 Deploy no GitHub Pages

### 1. Criar Repositório

- Acesse GitHub.com
- Crie um repositório público chamado `blog`
- **Não** adicione README, .gitignore ou license

### 2. Configurar Pages

1. Vá para Settings → Pages
2. Source: Deploy from a branch
3. Branch: `main` / `/ (root)`
4. Salve as configurações

### 3. Push do Código

```bash
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/hungria21/blog.git
git push -u origin main
```

### 4. Aguardar Deploy

- O GitHub Pages irá fazer o build automaticamente
- Acesse: `https://hungria21.github.io/blog/`

## 🔧 Comandos Úteis

```bash
# Build para produção
bundle exec jekyll build

# Limpar cache
bundle exec jekyll clean

# Verificar configuração
bundle exec jekyll doctor

# Atualizar gems
bundle update
```

## 📱 Recursos do Blog

### Menu Lateral

- **Desktop**: Clique no botão ☰ para abrir/fechar
- **Mobile**: Menu em overlay com fundo escuro
- **Guias**: Acesso rápido aos guias organizados

### Posts

- **Grid responsivo**: Adapta-se ao tamanho da tela
- **Cards interativos**: Hover effects e animações
- **Metadata**: Data de publicação e autor
- **Excerpts**: Prévia do conteúdo

### Guias Rápidos

- **Coleção separada**: Organizados em `_guias/`
- **Acesso rápido**: Disponível no menu lateral
- **Formato otimizado**: Para consulta rápida

## 🎯 Próximos Passos

1. **Personalizar**: Altere cores, fontes e layout
2. **Adicionar**: Mais posts e guias
3. **Otimizar**: SEO e performance
4. **Integrar**: Google Analytics, comentários
5. **Expandir**: Categorias, tags, pesquisa

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🆘 Suporte

Se você encontrar algum problema ou tiver dúvidas:

1. Verifique a [documentação do Jekyll](https://jekyllrb.com/docs/)
2. Consulte a [documentação do GitHub Pages](https://pages.github.com/)
3. Abra uma issue no repositório

---

**Desenvolvido com ❤️ usando Jekyll e GitHub Pages**