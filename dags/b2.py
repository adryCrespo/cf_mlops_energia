from __future__ import annotations


from airflow.decorators import task
from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator


@task(task_id="run_this")
def run_this_func(dag_run=None):
    """
    Print the payload "message" passed to the DagRun conf attribute.

    :param dag_run: The DagRun object
    """
    print(f"Remotely received value of {dag_run.conf.get('message')} for key=message")


with DAG(
    dag_id="example_trigger_target_dag",
    catchup=False,
    schedule=None,
    tags=["example"],
) as dag:
    run_this = run_this_func()

    bash_task = BashOperator(
        task_id="bash_task",
        bash_command='echo "Here is the message: $message"',
        env={"message": '{{ dag_run.conf.get("message") }}'},
    )

    run_this >> bash_task