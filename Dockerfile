FROM python:3.12.3

WORKDIR /opt/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
COPY project .
COPY config/uwsgi uwsgi

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["sh", "/opt/app/start.sh"]