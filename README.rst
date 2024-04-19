Project "Checker"
====

Getting started
----

1. Install requirements::

    pip install -r ./requirements/production.txt

2. Apply environment settings in file `.env`.

   e.g. `Webhook <https://en.wikipedia.org/wiki/Webhook>`_ you can take with `serveo.net <https://serveo.net>`_: ::

    ssh -R 80:127.0.0.1:8000 serveo.net

3. Migrate Database::

    manage.py makemigrations
    python manage.py migrate

4. Run Django server and Celery::

    python manage.py runserver
    celery -A apps worker --loglevel=INFO -P solo
    celery -A apps beat -l info

   or::

    docker-compose up --build

Description
----

For demonstration purposes, a test database with sample data is included.
If needed, you can always delete the test database file `db.sqlite3`, perform migrations as per step 3, and use your own database.

