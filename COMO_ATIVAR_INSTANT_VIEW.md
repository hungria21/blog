# Como Ativar o Instant View no seu Blog

O Telegram Instant View não é ativado automaticamente apenas colocando o arquivo `iv-template.txt` no repositório. Você precisa seguir os passos oficiais do Telegram para "reivindicar" o seu domínio.

## Passo a Passo

1. **Acesse o Portal do Instant View:**
   Vá para [https://instantview.telegram.org/](https://instantview.telegram.org/) e faça login com sua conta do Telegram.

2. **Adicione seu Site:**
   - Na aba **"My Templates"**, insira a URL de um dos seus artigos (ex: `https://seu-usuario.github.io/seu-repo/posts/exemplo.html`).

3. **Configure o Template:**
   - No editor que abrir, cole o conteúdo do arquivo `iv-template.txt` que está na raiz deste repositório na coluna da esquerda.
   - Verifique se a visualização aparece corretamente na coluna da direita.

4. **Publicação e RHASH:**
   - Clique em **"Mark as Checked"** e depois em **"Submit and Get Link"**.
   - O Telegram fornecerá um link que contém um parâmetro `rhash=...`.
   - **Importante:** Para que o botão "Instant View" apareça para todos os usuários no Telegram, você precisa enviar links que incluam esse `rhash`.

## Por que não aparece o botão automaticamente?
O Telegram só habilita o botão automaticamente para domínios globais conhecidos (como Medium, WordPress, etc). Para sites no GitHub Pages, você deve:
- Usar o link gerado com `rhash`.
- Ou aguardar que o Telegram aprove seu template globalmente (o que raramente acontece para blogs pessoais).

## Dica para Testes
Você pode usar o bot `@chotamreaderbot` no Telegram enviando o link do seu artigo para testar como ele ficaria, mas o método oficial acima é o recomendado para produção.