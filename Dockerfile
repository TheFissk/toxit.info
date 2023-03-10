FROM node:19.5.0-alpine
WORKDIR /app
COPY . /app

# install npm dependancies
RUN npm install

FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1

# set the working directory inside the container
WORKDIR /app
COPY . /app

# install wget and nodejs
RUN apt-get update && apt-get install --no-install-recommends -y wget nodejs

# install python dependancies
RUN pip install -r requirements.txt

# run the main application loop
CMD python3 manage.py runserver