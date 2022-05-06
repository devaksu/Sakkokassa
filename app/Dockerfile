FROM  python:3.9.6-bullseye

ENV PYTHONDONTWRITEBYTECODE=1  
ENV PYTHONUNBUFFERED=1

ENV APP_HOME=/home/app/web

RUN mkdir -p $APP_HOME
RUN mkdir $APP_HOME/staticfiles
WORKDIR $APP_HOME

COPY . .

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt