FROM apache/airflow:latest-python3.8
USER root

ARG AIRFLOW_HOME=/opt/airflow
ADD dags /opt/airflow/dags
COPY ./requirements.txt  ./requirements.txt
USER airflow
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

USER ${AIRFLOW_UID}