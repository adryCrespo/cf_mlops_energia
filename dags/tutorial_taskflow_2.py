
from airflow.decorators import dag, task
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

@dag(
    "taskflow_api2",
    schedule=None,
    default_args={"retries": 1, 'owner':"adry"},
    description="DAG tutorial",
    catchup=False,
    tags=["tutorial"]
)
def tutorial_taskflow_api():
    @task()
    def task_lol():
        TriggerDagRunOperator(
            task_id="a_unique_task_id",
            #   execution_date=datetime.now().replace(tzinfo=timezone.utc),
            trigger_dag_id="taskflow_api2b", 
            conf={"numero": 10},
            # execution_date='{{ ds }}',
            reset_dag_run=True,
            wait_for_completion=True,
    )
    # @task()
    # def task_lol2():
    #     TriggerDagRunOperator(
    #         task_id="a_unique_task_id2",
    #         #   execution_date=datetime.now().replace(tzinfo=timezone.utc),
    #             trigger_dag_id="taskflow_api2b",  # dag to trigger      conf={"k": "v"}
    #         ).execute(kwargs)    

    n = task_lol()
    # m = task_lol2()
    print(f"--------------------------{n}")
tutorial_taskflow_api()