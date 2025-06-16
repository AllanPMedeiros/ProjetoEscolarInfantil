FROM bitnami/postgres-exporter:latest

# Define a variável de ambiente para o PostgreSQL
ENV DATA_SOURCE_NAME="postgresql://admin:admin123@db:5432/escola?sslmode=disable"

# Exponha a porta padrão do exporter
EXPOSE 9187