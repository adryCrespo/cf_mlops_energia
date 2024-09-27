

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
from  pipeline_procesamiento import import_full_data,limpieza_datos,creacion_variables,pre_model_processing
from get_env_vars import  init_env

from airflow.decorators import dag, task


@dag(
    "procesamiento_v2",
    default_args={"retries": 1, 'owner':"adry"},
    description="DAG tutorial",
    schedule=None,  tags=["v_2"])
def procesamiento_datos():
    
    @task()
    def task_init_env():
        env_vars = init_env()
        return env_vars

    @task()
    def task_procesamiento(env_vars):
    
        DATA_PATH = env_vars["data_path"] 
        nombre_archivo_input = env_vars["nombre_archivo_input"]
        
        print(f"tipo: {type(DATA_PATH)},{DATA_PATH}") 
        data = import_full_data(DATA_PATH+nombre_archivo_input)
        df = limpieza_datos(data)
        df = creacion_variables(df)
        df = pre_model_processing(df)
        df = df.loc["2012-01-01":]
        
        nombre_archivo_procesamiento = env_vars["nombre_archivo_procesamiento"]
        path_data = DATA_PATH + nombre_archivo_procesamiento
        df.to_csv(path_data) 

    env_vars = task_init_env()    
    task_procesamiento(env_vars)   
procesamiento_datos() 