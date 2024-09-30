from airflow.decorators import dag, task
from airflow.models.dag import DAG
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

with DAG(
    dag_id="dag_proceso",
    catchup=False,
    schedule=None,
    tags=["programa"],
) as dag:
    trigger_procesamiento = TriggerDagRunOperator(
        task_id="trigger_procesamiento",
        trigger_dag_id="dag_procesamiento",  # Ensure this equals the dag_id of the DAG to trigger
        conf={"numero": 1},
        reset_dag_run=True,
        wait_for_completion=True,
    )
    trigger_year_2012 = TriggerDagRunOperator(
        task_id="trigger_2012",
        trigger_dag_id="predicciones_parametrizo_year",  # Ensure this equals the dag_id of the DAG to trigger
        conf={"year": "2012"},
        reset_dag_run=True,
        wait_for_completion=True,
    )

    trigger_year_2013 = TriggerDagRunOperator(
        task_id="trigger_2013",
        trigger_dag_id="predicciones_parametrizo_year",  # Ensure this equals the dag_id of the DAG to trigger
        conf={"year": "2013"},
        reset_dag_run=True,
        wait_for_completion=True,
    )

    trigger_year_2014 = TriggerDagRunOperator(
        task_id="trigger_2014",
        trigger_dag_id="predicciones_parametrizo_year",  # Ensure this equals the dag_id of the DAG to trigger
        conf={"year": "2014"},
        reset_dag_run=True,
        wait_for_completion=True,
    )
    trigger_procesamiento >> trigger_year_2012>> trigger_year_2013 >> trigger_year_2014