#!/usr/bin/env bash
airflow db init 
# airflow db init
# airflow db migrate
# airflow upgradedb
# airflow db upgrade
# airflow db reset
airflow users create -r Admin -u admin -e admin@admin.com -f admin -l admin -p admin
# airflow scheduler &
# airflow webserver