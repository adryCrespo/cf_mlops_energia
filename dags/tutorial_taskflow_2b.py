from airflow.decorators import dag, task

from airflow.models.dag import DAG

@task()
def suma1(dag_run = None):
    numero = dag_run.conf.get("numero")
    return numero +1

@task()
def suma2(numero):
        return numero +1
    
@task()
def suma3(numero):
        return numero +1

with DAG(
    "taskflow_api2b",
    schedule=None,
    default_args={"retries": 1, 'owner':"adry"},
    description="DAG tutorial",
    catchup=False,
    tags=["tutorial"]
) as dag:

    n1 = suma1() 
    n2 = suma2(n1)
    n3 = suma3(n2)
    print(f"***** {n3}")
    
    n1 >> n2 >> n3


