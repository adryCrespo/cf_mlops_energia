
from airflow.models.dag import DAG


# Operators; we need this to operate!

from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python import PythonOperator

def pyversion(): 
    import sysconfig
    print(f"py version: {sysconfig.get_python_version()}")
    import sklearn
    print(f"sklearn version: {sklearn.__version__}")
 



with DAG(
    "xxx_pyversion_dag",
    default_args={"retries": 2, 'owner':"adry"},
    description="DAG tutorial",
    schedule=None,  tags=["pruebas"]
) as dag:
    
    lc = PythonOperator(task_id="pyversion", python_callable=pyversion)
    suma = DummyOperator(task_id="suma")

    lc >> suma 