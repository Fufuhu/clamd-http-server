FROM python:3.8-slim-buster

EXPOSE 5000
COPY clamd_http_server.py clamd_http_server.py
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
ENV CLAMD_HTTP_SERVER_LISTENING_PORT=5000
ENV CLAMD_LISTENING_PORT=3310
ENV CLAMD_SERVER='localhost'
CMD python clamd_http_server.py
