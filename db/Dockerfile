# Dockerfile
FROM postgres:17

# Copiar scripts de inicialización
COPY init.sql /docker-entrypoint-initdb.d/

# Exponer el puerto predeterminado de PostgreSQL
EXPOSE 5432