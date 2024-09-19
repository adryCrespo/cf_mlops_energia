

from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy_operator import DummyOperator

# from dags.pipeline_2

import sys
list_path = ["scripts", "data"]
for path_element in list_path:
    sys.path.append("/opt/airflow/"+path_element)

# sys.path.append("/opt/airflow/scripts")
# sys.path.append("/opt/airflow/data")
from  pipeline_procesamiento import procesamiento


with DAG(
    "procesamiento_v1",
    default_args={"retries": 1, 'owner':"adry"},
    description="DAG tutorial",
    schedule=None,  tags=["v_1"]
) as dag:
    
    task_procesamiento = PythonOperator(task_id="procesamiento_datos", python_callable=procesamiento)
    task_dummy = DummyOperator(task_id="dummy")

    task_procesamiento >> task_dummy 