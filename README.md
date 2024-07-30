
# Projet ft_transcendence

Ce projet consiste à créer un site web permettant de jouer à Pong en local seul contre un bot ou a deux sur clavier partagé. Ce projet inclu un frontend, un backend, une base de données, un serveur Django, et des services de sécurité et de surveillance, le tout déployé avec Docker Compose.

## Prérequis

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Installation

1. Clonez le dépôt :
    bash
      git clone https://github.com/qbnt/6_ft_transcendence.git
      cd 6_ft_transcendence

2. Configurez les variables d'environnement :
    bash
      touch .env
    
    Ajoutez-y les variables nécessaires :
       # .env
       POSTGRES_USER=user  
       POSTGRES_PASSWORD=password  
       POSTGRES_DB=pongdb  
       DJANGO_ADMIN_USER: admin  
       DJANGO_ADMIN_MAIL: admin@test.test  
       DJANGO_ADMIN_PASS: admin  

4. Démarrez les services avec Docker Compose :
    bash
      docker-compose up --build

## Utilisation

1. Accédez à l'interface utilisateur à l'adresse :
    http://localhost

2. Jouez à Pong et expérimentez les fonctionnalités

3. Visualisez les métriques de surveillance sur Grafana :
    http://localhost:3001

## Services Configurés

- **frontend** : Serveur frontend (Node.js)
- **backend** : Serveur backend (Django)
- **db** : Base de données (PostgreSQL)
- **nginx** : Reverse proxy (Nginx)
- **blockchain** : Nœud blockchain (Ethereum)
- **prometheus** : Surveillance (Prometheus)
- **grafana** : Visualisation (Grafana)
- **vault** : Gestion des secrets (HashiCorp Vault)

## Contributions

1. Créez une branche (`git checkout -b feature/ma-fonctionnalite`).
2. Committez vos changements (`git commit -m 'Ajout de ma fonctionnalité'`).
3. Pushez la branche (`git push origin feature/ma-fonctionnalite`).
4. Ouvrez une Pull Request.

