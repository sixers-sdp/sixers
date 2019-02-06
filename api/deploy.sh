#!/bin/bash

export DJANGO_SETTINGS_MODULE=api.production_settings

source ~/venv/bin/activate
~/venv/bin/pip install -r ~/sixers/api/requirements.txt
~/sixers/api/manage.py collectstatic -y
~/sixers/api/manage.py migrate
