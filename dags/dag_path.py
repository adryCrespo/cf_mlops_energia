import sys
from airflow.models.dag import DAG


# Operators; we need this to operate!

# from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python import PythonOperator

sys.path.append("/opt/airflow/scripts")
from prueba import chorradas

def ver_path():
    
    import sys
    from pprint import pprint
    pprint(sys.path)

def suma():
    
    pass



with DAG(
    "xxx_path_dag",
    default_args={"retries": 2, 'owner':"adry"},
    description="DAG tutorial",
    schedule=None,  tags=["pruebas"]
) as dag:
    
    ver_path = PythonOperator(task_id="ver_path", python_callable=ver_path)
    suma = PythonOperator(task_id="suma", python_callable=chorradas)

    ver_path >> suma 