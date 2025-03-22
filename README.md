# Bot de Música para Discord

Um bot de Discord rico em recursos que pode reproduzir música do YouTube e Spotify.

## Funcionalidades

- Reprodução de música a partir de URLs do YouTube ou consultas de pesquisa
- Suporte para faixas, playlists e álbuns do Spotify
- Sistema de gerenciamento de fila
- Suporte a múltiplos servidores
- Controles básicos de música (reproduzir, pausar, retomar, parar)
- Documentação OpenAPI/Swagger para comandos

## Requisitos

- Python 3.8 ou superior
- FFmpeg instalado no seu sistema
- Token de Bot do Discord
- (Opcional) Credenciais da API do Spotify para funcionalidade do Spotify

## Instalação

1. Clone este repositório:
   ```
   git clone <url-do-repositório>
   cd disc-bot
   ```

2. Instale os pacotes Python necessários:
   ```
   pip install -r requirements.txt
   ```

3. Instale o FFmpeg:
   - **Windows**: Baixe do [ffmpeg.org](https://ffmpeg.org/download.html) e adicione-o ao seu PATH
   - **Linux (Debian/Ubuntu)**: `sudo apt install ffmpeg`
   - **macOS**: `brew install ffmpeg`

4. Configure seu bot:
   - Crie um arquivo `.env` na raiz do projeto (veja `.env.example`)
   - Adicione seu Token de Bot do Discord e credenciais do Spotify ao arquivo `.env`
   - Obtenha seu Token de Bot do Discord no [Portal de Desenvolvedor do Discord](https://discord.com/developers/applications)
   - (Opcional) Obtenha credenciais da API do Spotify no [Painel de Desenvolvedor do Spotify](https://developer.spotify.com/dashboard/)

## Configuração

No seu arquivo `.env`, adicione o seguinte:
```
DISCORD_TOKEN=seu_token_do_discord_aqui
SPOTIFY_CLIENT_ID=seu_client_id_do_spotify_aqui
SPOTIFY_CLIENT_SECRET=seu_client_secret_do_spotify_aqui
```

Você também pode personalizar outras configurações no arquivo `config.py`, como o prefixo de comando.

## Uso

1. Inicie o bot:
   ```
   python main.py
   ```

2. Convide o bot para seu servidor usando a URL OAuth2 do Portal de Desenvolvedor do Discord

3. Use os seguintes comandos:
   - `!join` - Conectar ao seu canal de voz
   - `!leave` - Desconectar do canal de voz
   - `!play <url ou termo de pesquisa>` - Reproduzir a partir de URL do YouTube ou pesquisa
   - `!play <url do spotify>` - Reproduzir a partir de URL do Spotify (faixa, playlist, álbum)
   - `!pause` - Pausar reprodução atual
   - `!resume` - Retomar reprodução pausada
   - `!stop` - Parar reprodução e limpar fila
   - `!skip` - Pular para a próxima música
   - `!queue` - Mostrar fila atual
   - `!clear` - Limpar a fila
   - `!ping` - Verificar latência do bot

## Documentação da API (Swagger/OpenAPI)

O bot vem com um arquivo de documentação Swagger/OpenAPI que descreve todos os comandos como se fossem endpoints de API. Isso fornece uma representação clara e visual dos comandos disponíveis.

Para visualizar a documentação:

1. Copie o conteúdo do arquivo `commands_api.yaml`
2. Cole-o em um editor online de Swagger UI como o [Swagger Editor](https://editor.swagger.io/)
3. A documentação será renderizada em uma interface amigável, mostrando todos os comandos, parâmetros e respostas

Alternativamente, você pode usar ferramentas como [Redocly](https://redocly.github.io/redoc/) ou [SwaggerHub](https://app.swaggerhub.com/) para renderizar a documentação.

Esta documentação da API serve como uma referência útil para entender:
- Todos os comandos disponíveis
- Parâmetros necessários
- Possíveis respostas
- Categorização de comandos

## Permissões do Discord

O bot requer estas permissões:
- Ver Canais
- Enviar Mensagens
- Ler Histórico de Mensagens
- Conectar a Canais de Voz
- Falar em Canais de Voz

## Solução de Problemas

- **Bot não entra no canal de voz**: Certifique-se de que ele tem permissão para entrar em canais de voz
- **Sem som**: Verifique se o FFmpeg está instalado corretamente
- **Spotify não funciona**: Verifique suas credenciais da API do Spotify no arquivo `.env`
- **Bot desconecta**: Isso pode ser devido a problemas de conexão com a internet ou limitações da API do Discord
- **Erros de token**: Certifique-se de que seu arquivo `.env` está configurado corretamente e o token é válido

## Segurança

- O arquivo `.env` contém informações sensíveis e está incluído no `.gitignore`
- Nunca envie seus tokens ou chaves de API para o controle de versão
- Se você expor acidentalmente seu token do Discord, regenere-o imediatamente no Portal de Desenvolvedor do Discord

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para enviar um Pull Request.

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para detalhes. 