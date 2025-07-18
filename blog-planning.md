# Planejamento do Blog Jekyll para GitHub Pages

## Estrutura de Arquivos

```
blog/
├── _config.yml
├── _layouts/
│   ├── default.html
│   └── post.html
├── _includes/
│   ├── header.html
│   └── sidebar.html
├── _posts/
│   ├── 2025-07-18-primeiro-post.md
│   └── 2025-07-18-segundo-post.md
├── _guias/
│   ├── guia-git.md
│   └── guia-javascript.md
├── _sass/
│   └── main.scss
├── assets/
│   └── css/
│       └── style.scss
├── index.html
└── README.md
```

## Especificações Técnicas

### Design
- **Cor de fundo**: #121212 (fundo escuro)
- **Layout**: Cabeçalho fino com botão de menu à esquerda
- **Navegação**: Menu lateral deslizante
- **Sem rodapé**: Layout limpo e minimalista

### Funcionalidades
- **Página principal**: Lista todas as postagens do blog
- **Menu lateral**: Acesso rápido aos guias
- **Postagens**: Organizadas na pasta `_posts`
- **Guias**: Organizadas na pasta `_guias`
- **Responsivo**: Funciona em dispositivos móveis

## Configuração do Jekyll

### _config.yml
```yaml
title: "Meu Blog Tech"
description: "Blog sobre desenvolvimento e tecnologia"
url: "https://hungria21.github.io"
baseurl: "/blog"

markdown: kramdown
highlighter: rouge
permalink: /:year/:month/:day/:title/

collections:
  guias:
    output: true
    permalink: /guias/:name/

plugins:
  - jekyll-feed
  - jekyll-sitemap

sass:
  style: compressed
```

## Estrutura das Páginas

### Layout Principal (default.html)
- Cabeçalho com botão de menu
- Área de conteúdo principal
- Menu lateral oculto por padrão
- JavaScript para toggle do menu

### Layout de Post (post.html)
- Herda do layout default
- Área específica para conteúdo do post
- Metadados (data, autor, tags)

## Conteúdo Inicial

### Postagens (_posts/)
1. **2025-07-18-primeiro-post.md**: Post de boas-vindas
2. **2025-07-18-segundo-post.md**: Post sobre desenvolvimento

### Guias (_guias/)
1. **guia-git.md**: Guia rápido do Git
2. **guia-javascript.md**: Guia rápido do JavaScript

## Estilos CSS

### Cores Principais
- Fundo: #121212
- Texto: #ffffff
- Accent: #00d4aa
- Cinza: #8e8e93

### Componentes
- Menu lateral com animação slide
- Cards para postagens
- Botão de menu hambúrguer
- Tipografia limpa e legível

## Responsividade

### Breakpoints
- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

### Adaptações
- Menu lateral em overlay no mobile
- Stack de cards no mobile
- Ajustes de tipografia

## Recursos Técnicos

### JavaScript
- Toggle do menu lateral
- Animações suaves
- Navegação sem recarregamento da página

### SEO
- Meta tags otimizadas
- Sitemap automático
- Feed RSS
- URLs amigáveis

## Deployment

### GitHub Pages
- Push para repositório `hungria21/blog`
- Configuração automática do Jekyll
- Deploy automático via GitHub Actions
- HTTPS habilitado

### Configuração do Repositório
1. Criar repositório público `blog`
2. Habilitar GitHub Pages
3. Configurar branch `main` como fonte
4. Configurar domínio customizado (opcional)

## Próximos Passos

1. **Criar estrutura de arquivos**
2. **Desenvolver layouts HTML**
3. **Implementar estilos CSS**
4. **Adicionar JavaScript**
5. **Criar conteúdo inicial**
6. **Testar localmente**
7. **Deploy no GitHub Pages**
8. **Configurar domínio**

## Comandos Úteis

### Desenvolvimento Local
```bash
# Instalar Jekyll
gem install jekyll bundler

# Criar novo site
jekyll new blog

# Servir localmente
bundle exec jekyll serve

# Build para produção
bundle exec jekyll build
```

### Git Commands
```bash
# Inicializar repositório
git init
git add .
git commit -m "Initial commit"

# Conectar com GitHub
git remote add origin https://github.com/hungria21/blog.git
git push -u origin main
```

## Manutenção

### Adicionando Conteúdo
- Novos posts: criar arquivos em `_posts/`
- Novos guias: criar arquivos em `_guias/`
- Formato: YYYY-MM-DD-titulo.md

### Atualizações
- Themes e plugins via Gemfile
- Configurações via _config.yml
- Estilos via arquivos SASS

### Monitoramento
- Google Analytics (opcional)
- GitHub Insights
- Feedback dos usuários