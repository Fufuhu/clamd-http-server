FROM python:3.8-slim-buster

EXPOSE 5000
COPY clamd_http_server.py clamd_http_server.py
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
CMD python clamd_http_server.py
