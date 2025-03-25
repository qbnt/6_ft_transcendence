# ft_transcendence Project

This project consists of building a web application that lets users play Pong locally — either solo against a bot or in 2-player mode on a shared keyboard. It includes a frontend, backend, database, Django server, security and monitoring services, all deployed with Docker Compose.

## 🛠️ Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## ⚙️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/qbnt/6_ft_transcendence.git
   cd 6_ft_transcendence
   ```

2. Set up environment variables:
   ```bash
   touch .env
   ```

   Add the necessary values:
   ```env
   POSTGRES_USER=user
   POSTGRES_PASSWORD=password
   POSTGRES_DB=pongdb
   DJANGO_ADMIN_USER=admin
   DJANGO_ADMIN_MAIL=admin@test.test
   DJANGO_ADMIN_PASS=admin
   UID_42=***************
   SECRET_42=*****************
   ```

3. Start the services with Docker Compose:
   ```bash
   docker-compose up --build
   ```

## 💡 Usage

1. Open the user interface in your browser:  
   [http://localhost](http://localhost)

2. Play Pong and explore available features.

3. View monitoring metrics on Grafana:  
   [http://localhost:3000](http://localhost:3000)

4. Check logs and summaries on Kibana:  
   [http://localhost:5601](http://localhost:5601)

## 🧩 Configured Services

- **backend**: Backend server (Django)
- **db**: PostgreSQL database
- **nginx**: Reverse proxy (Nginx)
- **blockchain**: Ethereum blockchain node
- **prometheus**: Monitoring (Prometheus)
- **grafana**: Metrics visualization (Grafana)
- **vault**: Secret management (HashiCorp Vault)
- **ELK**: Log management (Elasticsearch/Logstash/Kibana)

## 🤝 Contributions

1. Create a new branch:  
   `git checkout -b feature/my-feature`

2. Commit your changes:  
   `git commit -m 'Add my feature'`

3. Push the branch:  
   `git push origin feature/my-feature`

4. Open a Pull Request.
