
from airflow.models.dag import DAG


# Operators; we need this to operate!

# from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python import PythonOperator


def push_function(**kwargs):
    ti = kwargs['ti']
    ti.xcom_push(key='message', value='Hello from push_function')

def pull_function(**kwargs):
    ti = kwargs['ti']
    message = ti.xcom_pull(key='message', task_ids='push_task')
    print(type(message))
    print(f"Received message: {message}")
    get_shit(message)


def get_shit(key):
    
    print(key)


with DAG(
    "xxx_Xcom_dag",
    default_args={"retries": 2, 'owner':"adry"},
    description="DAG tutorial",
    schedule=None,  tags=["pruebas"]
) as dag:

    push_task = PythonOperator(
        task_id='push_task',
        python_callable=push_function,
        provide_context=True    )

    pull_task = PythonOperator(
        task_id='pull_task',
        python_callable=pull_function,
        provide_context=True)

    push_task >> pull_task
    
    