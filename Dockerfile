FROM python:3.9.21-alpine3.21

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY src /app

COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh

EXPOSE 5000

ENV ENDPOINT="http://192.168.0.1"
ENV ADMINPASS="password"

ENTRYPOINT ["sh", "/entrypoint.sh"]