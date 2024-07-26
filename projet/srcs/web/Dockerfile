FROM python:3.12

RUN apt-get update

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install -r requirements.txt

EXPOSE 8000
CMD python ft_transcendence/manage.py makemigrations \
	&& python ft_transcendence/manage.py migrate \
	&& python ft_transcendence/manage.py runserver 0.0.0.0:8000