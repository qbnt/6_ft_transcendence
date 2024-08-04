# Utiliser l'image officielle Python comme image de base
FROM python:3.12

# Mise à jour des packages et installation des dépendances
RUN apt-get update && apt-get install -y zsh curl

# Définir le répertoire de travail dans le conteneur
WORKDIR /usr/src/app

# Copier le fichier requirements.txt et installer les dépendances Python
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Installer oh-my-zsh
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# Copier le reste du code de l'application
COPY . .

# Exposer le port utilisé par l'application
EXPOSE 8000

# Commande pour lancer l'application
CMD ["sh", "-c", "python ft_transcendence/manage.py makemigrations && python ft_transcendence/manage.py migrate && python ft_transcendence/manage.py runserver 0.0.0.0:8000"]
