

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
from  pipeline_prediccion import separacion, entrenamiento, evaluacion


with DAG(
    "predicciones_v1",
    default_args={"retries": 1, 'owner':"adry"},
    description="DAG tutorial",
    schedule=None,  tags=["v_1"]
) as dag:
    
    task_separacion = PythonOperator(task_id="separacion_datos", python_callable=separacion)
    
    task_entrenamiento = PythonOperator(task_id="entrenamiento_modelo", python_callable=entrenamiento)

    task_eval = PythonOperator(task_id="evaluacion_modelos", python_callable=evaluacion)
    task_dummy = DummyOperator(task_id="dummy")

    task_separacion >> task_entrenamiento >> task_eval >> task_dummy 