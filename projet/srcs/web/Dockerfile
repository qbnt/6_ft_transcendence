# FROM python:3.12

# RUN apt-get update

# WORKDIR /usr/src/app
# COPY requirements.txt ./
# RUN pip install -r requirements.txt \
# 	&& apt install zsh -y \
# 	&& sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" -y

# EXPOSE 8000
# WORKDIR /usr/src/app/ft_transcendence
# CMD python manage.py makemigrations \
# 	&& python manage.py migrate \
# 	# && python manage.py runserver 0.0.0.0:8000
# 	&& exec daphne -b 0.0.0.0 -p 8000 ft_transcendence.asgi:application

FROM python:3.12

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    zsh curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended

EXPOSE 8000

COPY . .

WORKDIR /usr/src/app/ft_transcendence
CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
# CMD ["sleep", "infinity"]