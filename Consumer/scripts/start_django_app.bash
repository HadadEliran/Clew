#!/bin/bash

# This script is response to start a django app.

# First, it tries to connect to the django's database. 
# Beacuse there are cases where the db isn't up, we tries to establish the connection up to 20 times.
# If the connection succeeded we will migrate the django's tables into it and run the server on port 8000.
# If the connection failed we will exit the script with return code of 1.

wait_for_db()
{
  attempt=1
  #while ! python manage.py sqlflush > /dev/null 2>&1 ;do
  while ! python manage.py sqlflush > connecting_db.log 2>&1 ;do
    if [ $attempt -gt 20 ]; then
        return 1
    fi

    echo "Waiting for the db to be ready. Attempt: $attempt"
    sleep 1
    attempt=$((attempt + 1))
  done
  
  return 0
}

wait_for_db
connected=$?

if [ $connected -eq 0 ]; then
    python /consumer/manage.py makemigrations
    python /consumer/manage.py migrate

    # Create the superuser. 
    # The script assumes the credetials has been configured as environments variables.
    python /consumer/manage.py createsuperuser --noinput
    python /consumer/manage.py runserver 0.0.0.0:8000
    exit 0
else
    echo "Failed to start the application. Last command output: "
    cat "connecting_db.log"
    exit 1
fi

