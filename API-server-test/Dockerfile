FROM python:3.7.10-slim-buster


WORKDIR /app

ADD requirements.txt .

RUN pip install -r requirements.txt

ADD ./ .

CMD ["python", "server.py"]