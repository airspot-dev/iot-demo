# Use an official Python runtime as a parent image
FROM python:3.7

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

RUN pip install flask json-logging requests cloudevents pytz gunicorn


ENV FLASK_APP /app/main.py
ENV FLASK_ENV production

CMD exec gunicorn --bind :8080 --workers 1 --threads 8 main:app