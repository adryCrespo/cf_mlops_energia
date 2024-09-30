
from __future__ import annotations


from airflow.decorators import dag, task
from airflow.models.dag import DAG
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

with DAG(
    dag_id="taskflow_3a",
    catchup=False,
    schedule=None,
    tags=["tutorial"],
) as dag:
    trigger = TriggerDagRunOperator(
        task_id="test_trigger_dagrun",
        trigger_dag_id="taskflow_3b",  # Ensure this equals the dag_id of the DAG to trigger
        conf={"numero": 1},
        # execution_date='{{ ds }}',
        reset_dag_run=True,
        wait_for_completion=True,
    )

    trigger