#!/bin/bash

export DJANGO_SETTINGS_MODULE=api.production_settings

source ~/venv/bin/activate
~/venv/bin/pip install -r ~/sixers/api/requirements.txt
python3 ~/sixers/api/manage.py collectstatic --noinput
python3 ~/sixers/api/manage.py migrate
