# Music PPTX Creator

[Click here to see this page in English](https://github.com/VictorAp12/Music-PPTX-Creator/blob/main/readme-en.md)

Aplicativo responsivo e bem intuitivo para realizar busca de músicas digitadas pelo usuário no site Genius usando a GeniusApi e as transformar em apresentações PowerPoint.
O aplicativo possui muitos tooltips (dicas que aparecem quando você fica com o mouse em cima de um elemento por um curto período de tempo) e diversas funções como:
- Personalizar os slides da maneira que quiser mudando os estilos;
- Modificar apresentações existentes que foram feitas com este app;
- Definir imagem de background e mudar a transparência dela;
- Mudar a pasta de destino dos arquivos;
- Mudar idioma;
- Mudar a chave de api do genius caso você tenha a sua ou a disponibilizada expire.

<h3 align="center">Music PPTX Creator</h3>

<div align="center">
<img src="https://github.com/VictorAp12/Music-PPTX-Creator/assets/148372228/ab401b3f-aa54-4f2d-a613-4c15aa246065" />
</div>

### O projeto tem 3 páginas:
- A primeira busca somente uma música;
<img src="https://github.com/VictorAp12/Music-PPTX-Creator/assets/148372228/2a076d16-4034-4eec-8be5-e1680c79beb0" width="500"/>

- A segunda busca várias músicas por digitação ou por arquivo csv estruturado da seguinte maneira: [Exemplo](https://github.com/VictorAp12/Music-PPTX-Creator/assets/148372228/6cab8e9f-1557-40aa-861f-b222c625ee5e)
<img src="https://github.com/VictorAp12/Music-PPTX-Creator/assets/148372228/ec45a7c9-a748-48d9-a65b-f783ec6ba7e0" width="500"/>

- A terceira não realiza a busca da música, pois você deverá inseri-la manualmente, após isso cria a apresentação PowerPoint.
<img src="https://github.com/VictorAp12/Music-PPTX-Creator/assets/148372228/18a39ead-f7ea-4b4b-ad60-780835032883" width="500"/>

Conteúdo:
- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Motivações](#motivações)


## Requisitos
- Python 3.11 ou acima.

## Instalação

  - Baixe o projeto como zip ou usando gitclone https://github.com/VictorAp12/Music-PPTX-Creator.git

  - Crie o ambiente virtual na pasta do projeto:
    ```bash
    python -m venv venv
    ```

  - Ative o ambiente virtual na pasta do projeto:
    ```bash
    venv\Scripts\activate
    ```

  - Instale as dependencias do projeto:
    ```bash
    pip install -r requirements.txt
    ```

  - Execute o main.py:
    ```bash
    python -m main
    ```

## Motivações

O objetivo deste projeto foi aplicar meus conhecimentos de POO (programação orientada a objetos), PySide6 (biblioteca para interface gráfica do usuário), python-pptx (para criar e modificar apresentações de powerpoints) e api do Genius (para realizar a busca de músicas), por isso o projeto tem uma tipagem forte em tudo e possui classes e métodos.
E o foco principal foi na parte da interface gráfica, pois sou um desenvolvedor back-end e precisava melhorar minhas habilidades no front-end.
E também queria automatizar o processo de criação de powerpoints de maneira dinâmica, por isso o projeto busca por músicas escolhidas para o usuário que nunca tem o mesmo tamanho o que deixa o processo de automatização muito desafiante.
