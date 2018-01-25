release: python manage.py migrate
web: gunicorn hc.wsgi
worker: ./manage.py ensuretriggers && ./manage.py sendalerts
