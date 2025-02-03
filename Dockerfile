FROM python:3.11

RUN apt update && apt upgrade -y
RUN pip3 install --upgrade pip

RUN apt install -y libdbus-1-dev libdbus-glib-1-dev

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/var/www/topaz/

WORKDIR /var/www/topaz
COPY . .
RUN pip3 install -r requirements.txt

EXPOSE 5000
