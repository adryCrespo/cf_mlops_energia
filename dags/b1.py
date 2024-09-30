
from __future__ import annotations


from airflow.models.dag import DAG
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

with DAG(
    dag_id="example_trigger_controller_dag",
    catchup=False,
    schedule=None,
    tags=["example"],
) as dag:
    trigger = TriggerDagRunOperator(
        task_id="test_trigger_dagrun",
        trigger_dag_id="example_trigger_target_dag",  # Ensure this equals the dag_id of the DAG to trigger
        conf={"message": "Hello World"},
        # execution_date='{{ ds }}',
        reset_dag_run=True,
        wait_for_completion=True,
    )

    trigger