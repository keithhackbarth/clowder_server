#!/bin/bash

cd /var/
mkdir data

. bin/activate

WSGI_PATH=`find /var/app | egrep '/var/app/[^/]+/wsgi.py'`
[ -n "$WSGI_MODULE" ] && UWSGI_MODULE="--module $WSGI_MODULE"

# defaulting to application.py if not explicitly set
[ -z "$WSGI_PATH" ] && WSGI_PATH=application.py

echo $WSGI_PATH
echo $UWSGI_MODULE

python3 /var/app/manage.py collectstatic --noinput
uwsgi --ini /var/app/uwsgi.ini --wsgi-file $WSGI_PATH $UWSGI_MODULE
