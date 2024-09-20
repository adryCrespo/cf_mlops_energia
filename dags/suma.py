
from airflow.models.dag import DAG


# Operators; we need this to operate!

# from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python import PythonOperator


def secret_number(ti):
    secret_number = 2
    ti.xcom_push(key="secret_number", value=secret_number)

def get_secret_number(ti):
    mensaje = ti.xcom_pull(key="secret_number", task_ids="generate_random_number_task")
    print(f"mensaje: {mensaje}") 


with DAG(
    "xxx_XCOM_dag",
    default_args={"retries": 1, 'owner':"adry"},
    description="DAG tutorial",
    schedule=None,  tags=["pruebas"]
) as dag:
    
    sn = PythonOperator(task_id="generate_random_number_task", python_callable=secret_number)
    gsn = PythonOperator(task_id="get", python_callable=get_secret_number)

    sn >> gsn 