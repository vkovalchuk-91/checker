Checker
====

1. Install requirements::

    pip install -r ./requirements/production.txt


2. Apply environment settings in file::

    .env


3. Migrate Database::

    manage.py makemigrations
    python manage.py migrate

4. Run Django server and Celery::

    python manage.py runserver
    celery -A apps worker --loglevel=INFO -P solo
    celery -A apps beat -l info

    or:

    docker-compose up --build


Description
----

Description...