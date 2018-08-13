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
uwsgi --http :8080 --chdir /var/app --wsgi-file $WSGI_PATH $UWSGI_MODULE --master --processes $UWSGI_NUM_PROCESSES --threads $UWSGI_NUM_THREADS --uid $UWSGI_UID --gid $UWSGI_GID --py-autoreload 6