# SistemaEscolar
Projeto do 5ºSemestre de ADS como parte das aulas de Integração de Software e Implementação de Software do professor Alexandre Tavares 


## Propósito

Este Repositorio foi criado para ensinar os alunos da UniFAAT a trabalharem com microserviço em Python.

## Estrutura do Projeto

├── InfraBD/ # Contem a os arquivos docker para subir o Banco de Dados<br>
│ ├── northwind.sql # SQL utilizado para criar o Banco e as tabelas utilizadas no projeto<br> 
│ ├── dockerFile # arquivo docker para inicializar o postgre<br>
│ └── [Readme.md](InfraBD/Readme.md) # Instruções para inicializar o banco no docker
├── app/ # Pasta com o projeto python<br>
│ ├── Util/ # Utilitários e modulos Python<br>
│ │ ├── bd.py # Arquivo python com função para conectar no Banco de Dados<br>
│ │ └── paramsBD.yml # Arquico com as configurações para conexão com o Banco de Dados<br>
│ ├── crudCateg.py # MicroServiso de CRUD de Categorias<br>
│ └── [Readme.md](app/Readme.md) # Instruções para inicializar o APP
└── Readme.md # Arquivo com instruções gerais