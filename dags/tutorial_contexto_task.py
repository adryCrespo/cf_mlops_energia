from airflow.models.taskinstance import TaskInstance
from airflow.models.dagrun import DagRun
from typing import Optional
from airflow.decorators import dag, task



@task
def print_ti_info(task_instance: Optional[TaskInstance] = None, dag_run: Optional[DagRun]= None):
    print(f"Run ID: {task_instance.run_id}")  # Run ID: scheduled__2023-08-09T00:00:00+00:00
    print(f"Duration: {task_instance.duration}")  # Duration: 0.972019
    print(f"DAG Run queued at: {dag_run.queued_at}")  # 2023-08-10 00:00:01+02:20


@dag(
    "tutorial_contexto2",
    schedule=None,
    default_args={"retries": 1, 'owner':"adry"},
    description="DAG tutorial",
    tags=["tutorial"]
)
def dag():
    print_ti_info()


dag()