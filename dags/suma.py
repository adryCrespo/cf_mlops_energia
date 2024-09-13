
from airflow.models.dag import DAG


# Operators; we need this to operate!

# from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python import PythonOperator


def create_list_compresion():
    lc = [i for i in range(5)]
    with open("lol.csv","w") as f:
        for n in lc:
            f.writelines(str(n)+"\n")

def suma():
    
    with open("lol.csv","r") as f:
        contents = f.readlines()
    
    c2 = sum([ int(i.replace("\n","")) for i in contents])
    print(c2)



with DAG(
    "xxx_prueba2_dag",
    default_args={"retries": 2, 'owner':"adry"},
    description="DAG tutorial",
    schedule=None,  tags=["pruebas"]
) as dag:
    
    lc = PythonOperator(task_id="create_list_compresion", python_callable=create_list_compresion)
    suma = PythonOperator(task_id="suma", python_callable=suma)

    lc >> suma 