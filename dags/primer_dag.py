
from airflow.models.dag import DAG


# Operators; we need this to operate!

from airflow.operators.dummy_operator import DummyOperator

with DAG(
    "xxx_prueba1_dag",
    default_args={"retries": 2, 'owner':"adry"},
    description="DAG tutorial",
    schedule=None,  tags=["pruebas"]
) as dag:
    get_api_bash = DummyOperator( task_id="get_api_bash"  )
    get_api_python = DummyOperator( task_id="get_api_python"  )
    join_trans = DummyOperator( task_id="join_trans"  )
    load_postgresSQL = DummyOperator( task_id="load_postgresSQL"  )

    [get_api_bash,get_api_python] >> join_trans >> load_postgresSQL