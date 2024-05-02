#!/bin/sh

flask db upgrade
# flask seed-db
exec gunicorn --bind 0.0.0.0:5500 "app:create_app()"