FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update -y

WORKDIR /app

COPY requirements.txt /app/

RUN pip3 install -r /app/requirements.txt

COPY . /app

COPY ./compose/django/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start

ENTRYPOINT ["/start"]
