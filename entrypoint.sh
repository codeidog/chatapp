#!/bin/sh
rm -rf web/static
#. venv/bin/activate
#Use the .env file if the key exists otherwise use an environment variable
if grep -q DATABASE_URL ./secret/.env; then
    url=$(grep  DATABASE_URL ./secret/.env)
else
    url=$DATABASE_URL
fi
#Extract the server and port number from the URL
serverport=$(echo $url | cut -d '@' -f 2 | cut -d "/" -f 1)
server=$(echo $serverport | cut -d ':' -f 1)
port=$(echo $serverport | cut -d ':' -f 2)
#Wait for the database to accept connection
while ! nc -z -v -w 3 $server $port; do sleep 5; done
echo "Db is accepting connections"
flask db init
exec gunicorn -b :5000 --access-logfile - --error-logfile - chat:app