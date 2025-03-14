FROM python:3.9.21-alpine3.21

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY src /app

COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh

EXPOSE 5000

ENV ENDPOINT="http://192.168.0.1"
ENV ADMINPASS="password"

HEALTHCHECK --interval=30s --timeout=3s --start-period=30s \
  CMD wget --quiet --tries=1 --spider http://127.0.0.1:5000/api/health || exit 1

ENTRYPOINT ["sh", "/entrypoint.sh"]