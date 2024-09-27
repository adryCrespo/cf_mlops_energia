

from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression
import pickle
# from dags.pipeline_2

import sys
list_path = ["scripts", "data"]
for path_element in list_path:
    sys.path.append("/opt/airflow/"+path_element)

# sys.path.append("/opt/airflow/scripts")
# sys.path.append("/opt/airflow/data")

from  pipeline_prediccion import import_processed_data, separacion_train_test, import_indices, get_training_data, get_test_data

from get_env_vars import  init_env

from airflow.decorators import dag, task
@dag(
    "predicciones_v2",
    default_args={"retries": 1, 'owner':"adry"},
    description="DAG tutorial",
    schedule=None,  tags=["v_2"])
def pipeline_ML():

    @task()
    def task_init_env():
        env_vars = init_env()
        return env_vars

    @task()
    def task_separacion_datos(env_vars):
           
        DATA_PATH = env_vars["data_path"] 
        nombre_archivo_procesamiento = env_vars["nombre_archivo_procesamiento"] 
        path_data_procesamiento = DATA_PATH + nombre_archivo_procesamiento
    
        df_model = import_processed_data(path_data_procesamiento )
        X_train, _ , i_ , _ = separacion_train_test(df_model) 
        serie_indices = X_train.reset_index()[["index"]]

    
        nombre_archivo_index = env_vars["nombre_archivo_index"] 
    
        path_data_indices = DATA_PATH + nombre_archivo_index 
        serie_indices.to_csv(path_data_indices )
        return path_data_indices

    @task()
    def task_entrenamiento(env_vars,path_data_indices):
        DATA_PATH = env_vars["data_path"] 
        nombre_archivo_procesamiento = env_vars["nombre_archivo_procesamiento"] 
        path_data_procesamiento = DATA_PATH + nombre_archivo_procesamiento
   
        X_train, Y_train = get_training_data(path_data_indices, path_data_procesamiento) 
   
        model = LinearRegression(n_jobs=-1)
        model.fit(X_train,Y_train)

        nombre_archivo_modelo = "modelo_lineal.pkl" 
        path_archivo_modelo = DATA_PATH+nombre_archivo_modelo
        with open(path_archivo_modelo, 'wb') as f:
            pickle.dump(model, f)
        return path_archivo_modelo
    
    @task()
    def task_evaluacion(env_vars,path_data_indices,path_archivo_modelo  ):
        
        DATA_PATH = env_vars["data_path"] 
        nombre_archivo_procesamiento = env_vars["nombre_archivo_procesamiento"] 
        path_data_procesamiento = DATA_PATH + nombre_archivo_procesamiento

   
        with open(path_archivo_modelo, 'rb') as f:
            model = pickle.load(f)   
    
        X_test, Y_test = get_test_data(path_data_indices, path_data_procesamiento)
    
        y_pred = model.predict(X_test)
        rmse = mean_squared_error(Y_test, y_pred,squared=False)
        print(f"rmse {rmse}")


    env_vars = task_init_env()
    path_data_indices = task_separacion_datos(env_vars)
    path_archivo_modelo = task_entrenamiento(env_vars,path_data_indices )
    task_evaluacion(env_vars,path_data_indices,path_archivo_modelo  )

pipeline_ML()





