<h1 align="center">
<br>
  <img src="https://github.com/luddias/readmefiles/blob/main/icon.png" alt="susc_logo" width="120">
<br>
<br>
SUSC
</h1>

<p align="center">Aplicativo para controle de unidade de saúde, construído utilizando Python, Kivy e Firebase.</p>


<div align="center">
  <img src="https://github.com/luddias/readmefiles/blob/main/lv-0-20220715124253.gif" alt="demo" height="425">
  <img src="https://github.com/luddias/readmefiles/blob/main/lv-0-20220715123910.gif" alt="demo" height="425">
</div>

<hr />

## Funcionalidades

- Login, cadastro e redefinição de senha do usuário.
- Fazer agendamento de retiradas de medicamentos e de consultas médicas.
- Visualizar próximos agendamentos .
- Visualizar tabela com dados dos pacientes.
- Visualizar tabela com dados dos medicamentos, e fazer alteração em quantidades de estoque (entrada e saída).


## Recursos

- 🐍 **Python** — Linguagem utilizada para desenvolvimento da parte lógica do sistema.
- 🔰 **Kivy e KivyMD** —  Bibliotecas Open Source escrita em Python para o desenvolvimento de aplicações multiplataforma.
- 🔥 **Firebase** — Plataforma desenvolvida pelo Google para criar aplicativos móveis e web. Foi se utilizado o "Realtime Database" da plataforma como Banco de dados para armazenar dados do sistema.
- 🌀 **Json e Request** — Bibliotecas utilizadas para fazer a comunicação entre o aplicativo e o banco de dados.

## Instruções Iniciais

**Python**: Para a instalação em um sistema Windows, recomendo que siga o passo-a-passo desse <a href="https://python.org.br/instalacao-windows/">**link**</a>.
<br> Para a instalação em um sistema Linux, recomendo que siga as instruções desse <a href="https://python.org.br/instalacao-linux/">**link**</a>.
<br> E caso seu sistema seja Mac, sugiro que siga as instruções desse <a href="https://python.org.br/instalacao-mac/">**link**</a>.

**Kivy e KivyMD**: Para a instalação em um sistema Windows ou Linux, recomendo que siga o passo-a-passo desse
<a href="https://acervolima.com/introducao-ao-kivy-uma-estrutura-python-de-plataforma-cruzada/">**link**</a>.
<br>Para a instalação em outros sistemas, recomendo a leitura da <a href= "https://kivy.org/doc/stable/gettingstarted/installation.html#installation-canonical">**documentação da biblioteca**</a>.
<br>Após instalar o Kivy, utilize o pip para instalar o KivyMD. Para mais informações ou dúvidas, confira as <a href="https://kivymd.readthedocs.io/en/latest/getting-started/">**instruções da documentação**</a>.

**Firebase**: Crie uma conta no <a href="https://firebase.google.com">site</a> e crie um projeto. Após isso, a ferramenta do Firebase que será utilizada para o aplicativo é o **"Realtime Database"**, que pode ser encontrado no menu do lado esquerdo da página. Crie um Realtime Database e copie o link que será fornecido e substitua o que está no arquivo "database.py" disponibilizado nesse repositório. 



