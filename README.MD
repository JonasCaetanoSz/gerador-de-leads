
# gerador de leads

gerador de leads com dados publicos do instagram


## Instalação

clone o repositorio:

```bash
git clone https://github.com/JonasCaetanoSz/gerador-de-leads.git
```

inicia e instala as dependecias em um ambiente virtual:

```bash
python -m venv gerador-de-leads && cd gerador-de-leads/scripts && activate && cd.. pip install -r requirements.txt 
```

inicie o programa:

```bash
python start.py
```

## Funcionalidades

- Coleta de dados de um perfil especifico
- Log em tempo real
- Exportar em arquivo de Excel (.XLSX)


### dados:

- Nome de usuario
- Nome (se disponivel)
- Numero de telefone (se disponivel)
- Email (se disponivel)


## FAQ

#### Quantos dados posso coletar?

á quantidade que o instagram permitir.

#### Posso usar meu perfil pessoal no programa?

Não encorajo você a fazer isso, o instagram é muito rigido com a privacidade de seus usuarios, portanto se eles descofiarem que seu perfil está sendo utilizado para burlar as diretrizes da comunidade sua conta pode ser suspensa permanentemente.

#### Como fazer login via sessionID?

para fazer login por esse método, basta inserir o sessionID no campo `login` da tela inicial e não digitar a senha e claro clicar em `add+`, dessa forma o programa vai tentar fazer login no instagram com o sessionID digitado no campo `login`.
## Screenshots

janela inicial:

![Capturar](https://user-images.githubusercontent.com/86696196/211113379-8d1282bc-8a89-44e3-b79e-cf27f09f1e01.PNG)

janela de extração:

https://user-images.githubusercontent.com/86696196/211115293-50636e93-2960-4fe0-a2ad-7eab0c653a61.mp4
## Log de mudanças

## 10/01/2023

### alterados:

**[extract.py]** - criar função que salva arquivo quando o programa é fechado.  <br>
**[extract.py]** - fazer theard acionada por extract.py acabar quando o programa é encerrado.  <br>
**[insta.py]** - fazer theard que gerencia função de extração de dados acaba quando o programa é encerrado.  <br>
**[insta.py]** - extração de um perfil por vez  <br>
**[start.py]** - login via sessionID  <br>
## Licença

distribuido sobre á licença [MIT](https://choosealicense.com/licenses/mit/)

