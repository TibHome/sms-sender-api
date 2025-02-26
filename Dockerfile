FROM python:3.9.21-alpine3.21

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY src /app

COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh

# Exposer le port 5000
EXPOSE 5000

# Définir le script d'entrée
ENTRYPOINT ["sh", "/entrypoint.sh"]