#!/usr/bin/env bash
airflow db init 

airflow users create -r Admin -u admin -e admin@admin.com -f admin -l admin -p admin
