#!/bin/bash
set -e

if [ "$1" = 'run' ]; then
     echo "Starting runner"
     python3 /idt_backend/runtime/manage.py makemigrations
     python3 /idt_backend/runtime/manage.py migrate

     echo "Starting main server"
     python3 /idt_backend/runtime/manage.py runserver 0.0.0.0:8000 --noreload
fi
exec "$@"
