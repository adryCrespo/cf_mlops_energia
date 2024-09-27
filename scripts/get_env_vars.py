


def init_env():
    DATA_PATH = "/opt/airflow/data/"
    nombre_archivo_input = "vic_electricity.csv"
    nombre_archivo_procesamiento = "procesamiento.csv"
    nombre_archivo_index = "index.csv"
    nombre_archivo_modelo = "modelo.pkl"
    env_vars = {"data_path":DATA_PATH,
           "nombre_archivo_input": nombre_archivo_input,
           "nombre_archivo_procesamiento":nombre_archivo_procesamiento,
            "nombre_archivo_index":nombre_archivo_index,
            "nombre_archivo_modelo" : nombre_archivo_modelo        }
    return env_vars
def push_env(**kwargs):
     
    DATA_PATH = "/opt/airflow/data/"
    nombre_archivo_input = "vic_electricity.csv"
    nombre_archivo_procesamiento = "procesamiento.csv"
    nombre_archivo_index = "index.csv"
    nombre_archivo_modelo = "modelo.pkl"
    print(DATA_PATH)
    print(type(DATA_PATH))

    ti = kwargs['ti']
    ti.xcom_push(key='data_path', value=DATA_PATH)
    ti.xcom_push(key='nombre_archivo_procesamiento' , value = nombre_archivo_procesamiento )
    ti.xcom_push(key='nombre_archivo_input' , value = nombre_archivo_input )
    ############################ 
    ti.xcom_push(key = "nombre_archivo_index", value= nombre_archivo_index)
    ti.xcom_push(key = "nombre_archivo_modelo" , value = nombre_archivo_modelo )
    # ti.xcom_push(key='nombre_archivo_input' , value = nombre_archivo_input )



def pull_env(key,**kwargs):
    ti = kwargs['ti']
    message = ti.xcom_pull(key=key, task_ids='task_env')