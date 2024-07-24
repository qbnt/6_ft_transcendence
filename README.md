
# Projet ft_transcendence

Ce projet consiste à créer un site web permettant de jouer à Pong en temps réel, incluant un frontend, un backend, une base de données, un serveur WebSocket, et des services de sécurité et de surveillance, le tout déployé avec Docker Compose.

## Prérequis

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Installation

1. Clonez le dépôt :
    bash
      git clone https://github.com/votre-utilisateur/ft_transcendence_surprise.git
      cd ft_transcendence_surprise

2. Configurez les variables d'environnement :
    bash
      touch .env
    
    Ajoutez-y les variables nécessaires :
      env
       POSTGRES_USER=user
       POSTGRES_PASSWORD=password
       POSTGRES_DB=pongdb

3. Démarrez les services avec Docker Compose :
    bash
      docker-compose up --build

## Utilisation

1. Accédez à l'interface utilisateur à l'adresse :
    http://localhost

2. Jouez à Pong en temps réel avec d'autres utilisateurs.

3. Visualisez les métriques de surveillance sur Grafana :
    http://localhost:3001

## Services Configurés

- **frontend** : Serveur frontend (Node.js)
- **backend** : Serveur backend (Ruby)
- **db** : Base de données (PostgreSQL)
- **nginx** : Reverse proxy (Nginx)
- **websocket** : Serveur WebSocket (Node.js)
- **blockchain** : Nœud blockchain (Ethereum)
- **prometheus** : Surveillance (Prometheus)
- **grafana** : Visualisation (Grafana)
- **vault** : Gestion des secrets (HashiCorp Vault)

## Contributions

1. Fork le dépôt.
2. Créez une branche (`git checkout -b feature/ma-fonctionnalite`).
3. Committez vos changements (`git commit -m 'Ajout de ma fonctionnalité'`).
4. Pushez la branche (`git push origin feature/ma-fonctionnalite`).
5. Ouvrez une Pull Request.

