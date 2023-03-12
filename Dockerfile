FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1

# set the working directory inside the container
WORKDIR /app
COPY . /app

# install wget and nodejs
RUN apt-get update && apt-get install --no-install-recommends -y wget

# install python dependancies
RUN pip install -r requirements.txt

# run the main application loop
EXPOSE $PORT
CMD ["gunicorn", "--bind", ":${PORT}", "--workers", "3", "toxit_main.wsgi:application"]