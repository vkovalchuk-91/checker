# Uncomment this `release` process if you are using a database, so that Django's model
# migrations are run as part of app deployment, using Heroku's Release Phase feature:
# https://docs.djangoproject.com/en/5.0/topics/migrations/
# https://devcenter.heroku.com/articles/release-phase

release: ./manage.py migrate
web: gunicorn apps.wsgi
celery: celery -A apps worker --loglevel=INFO -P solo