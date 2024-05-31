# Étape de construction
FROM node:14 AS devEnv

# Installer pkg
RUN npm install -g pkg

# Copier le code source
COPY ./app /app
WORKDIR /app

# Construire l'exécutable
RUN pkg hello.js --out-path /app

# Vérifier le contenu du répertoire de sortie
RUN ls -la /app

# Étape finale avec une image légère
FROM node:14-slim AS service
COPY --from=devEnv /app/hello-linux /hello
RUN chmod +x /hello
CMD ["/hello"]
