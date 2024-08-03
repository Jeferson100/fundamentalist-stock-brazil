## GitHub Actions - Push

**Mudar essa configuracao para permitir os pushs no repositório do `GITHUB Actions`	.**

![imagem](/.github/configuracao_pemitir_push_acitions.jpeg)

## Criação de um token de acesso pessoal

- Faça login na sua conta do GitHub e navegue até a seguinte [página](https://github.com/settings/tokens)

- Clique no botão gerar novo token e inicie o processo para obter um novo token

- Salve o token de acesso pessoal

![imagem](/.github/capitura_criacao_token.png)

## Salvar o token de acesso pessoal no seu repositório

- Apos isso entre no repositório e adicione o token de acesso pessoal.

- Click em settings

![imagem](/.github/setings.png)

- Clique em `Secrets` e depois em `Actions`.

![imagem](/.github/secrets.png)

- Aperte em `New repository secret` e salve o token de acesso pessoal.

![imagem](/.github/repository_secret.png)

## Usando o token de acesso pessoal

- Agora que o token de acesso pessoal foi salvo, basta adicionar secret no arquivo [workflow.yml](https://github.com/Jeferson100/Predicoes_macroeconomicas/blob/main/.github/workflows/treinando_avaliando_modelos.yml) do repositório.

![imagem](/.github/codigo_yml.png)










