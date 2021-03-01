#!/bin/sh
rm -rf web/static
#. venv/bin/activate
flask db init
exec gunicorn -b :5000 --access-logfile - --error-logfile - chat:app
