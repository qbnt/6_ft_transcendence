# Étape de construction
FROM python:latest AS devEnv
RUN apt update && apt install -y gcc
RUN pip install pyinstaller
COPY ./app /app
WORKDIR /app
RUN pyinstaller --onefile hello.py

# Vérifier le contenu du répertoire de sortie
RUN ls -la /app/dist/

# Étape intermédiaire pour débogage
FROM ubuntu:latest AS service
COPY --from=devEnv /app/dist/hello /hello
RUN chmod +x /hello
CMD ["/hello"]
