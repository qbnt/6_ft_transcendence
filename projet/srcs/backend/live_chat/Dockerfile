# Étape de construction
FROM python:latest AS devEnv
RUN apt update && apt install -y gcc && pip install pyinstaller
COPY ./app /app
WORKDIR /app
RUN pyinstaller --onefile hello.py

# Étape intermédiaire pour débogage
FROM debian:bookworm-20240513-slim AS service
COPY --from=devEnv /app/dist/hello /app/hello
WORKDIR /app
ENTRYPOINT ["./hello"]

