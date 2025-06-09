# Utiliza a imagem oficial mais recente do PostgreSQL como base.
FROM postgres:latest

# Defina variáveis de ambiente para configurar o PostgreSQL
ENV POSTGRES_DB=escola
ENV POSTGRES_USER=admin
ENV POSTGRES_PASSWORD=admin123

# Copie o script de inicialização para o diretório de inicialização do PostgreSQL
COPY init.sql /docker-entrypoint-initdb.d/

# Exponha a porta padrão do PostgreSQL
EXPOSE 5432