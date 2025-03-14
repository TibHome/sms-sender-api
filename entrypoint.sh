#!/bin/bash
# entrypoint.sh

cd /app

# Exécute la commande gunicorn pour démarrer l'application
exec gunicorn -w 4 -b 0.0.0.0:5000 app:app --log-level warning