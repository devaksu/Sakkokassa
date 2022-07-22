#!/bin/bash
sudo docker-compose up -d && \
#sudo docker-compose exec web python manage.py makemigrations --noinput && \
#sudo docker-compose exec web python manage.py migrate --noinput && \
#sudo docker-compose exec web python manage.py collectstatic --no-input --clear && \
sudo docker ps -a

#sudo docker-compose exec web python manage.py createsuperuser
