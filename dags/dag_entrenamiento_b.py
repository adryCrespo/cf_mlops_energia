

from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression
from mlflow.exceptions import RestException
from mlflow.models import infer_signature
from mlflow.tracking import MlflowClient
import pickle
# from dags.pipeline_2

import sys
list_path = ["scripts", "data"]
for path_element in list_path:
    sys.path.append("/opt/airflow/"+path_element)


from  pipeline_prediccion import import_processed_data, separacion_train_test, import_indices, get_training_data, get_test_data

from get_env_vars import  init_env
from mlflow_functions import mlflow_experiment_init
from airflow.decorators import dag, task

@dag(
    "predicciones_parametrizo_year",
    default_args={"retries": 1, 'owner':"adry"},
    description="DAG tutorial",
    schedule=None,  tags=["v_3","programa"])
def pipeline_ML():

    @task()
    def task_init_env(dag_run = None):
        env_vars = init_env()

        year = dag_run.conf.get("year")
        env_vars["year"] = str(year)

        return env_vars

    @task()
    def task_init_mlflow():
        parametros_mlflow = mlflow_experiment_init()
        return parametros_mlflow

    @task()
    def task_separacion_datos(env_vars):
           
        DATA_PATH = env_vars["data_path"] 
        nombre_archivo_procesamiento = env_vars["arhivo_procesamiento_"+env_vars["year"]] 
        path_data_procesamiento = DATA_PATH + nombre_archivo_procesamiento

        df_model = import_processed_data(path_data_procesamiento )
        X_train, _ , i_ , _ = separacion_train_test(df_model) 
        serie_indices = X_train.reset_index()[["index"]]

    
        nombre_archivo_index = env_vars["nombre_archivo_index"] 
    
        path_data_indices = DATA_PATH + nombre_archivo_index 
        serie_indices.to_csv(path_data_indices )
        return path_data_indices

    @task()
    def task_entrenamiento(env_vars, path_data_indices, parametros_mlflow):
        import mlflow
        DATA_PATH = env_vars["data_path"] 
        # nombre_archivo_procesamiento = env_vars["nombre_archivo_procesamiento"]
        nombre_archivo_procesamiento = env_vars["arhivo_procesamiento_"+env_vars["year"]] 
        path_data_procesamiento = DATA_PATH + nombre_archivo_procesamiento
   
        X_train, Y_train = get_training_data(path_data_indices, path_data_procesamiento) 
        
        # entrenamiento
        model = LinearRegression(n_jobs=-1)
        model.fit(X_train,Y_train)
        y_train_pred = model.predict(X_train)
        rmse_train = mean_squared_error(Y_train,y_train_pred, squared=False)
        
        #serializar modelo 
        nombre_archivo_modelo = "modelo_lineal.pkl" 
        path_archivo_modelo = DATA_PATH + nombre_archivo_modelo
        with open(path_archivo_modelo, 'wb') as f:
            pickle.dump(model, f)

        # evaluacion modelo 
        X_test, Y_test = get_test_data(path_data_indices, path_data_procesamiento)
        y_pred = model.predict(X_test)
        rmse_test = mean_squared_error(Y_test, y_pred,squared=False)
        
        # mlflow.log_metric("rmse_train", rmse_train)
        # mlflow.log_metric("rmse_test",rmse_test ) 


        #subir  modelo
        mlflow.set_tracking_uri(parametros_mlflow["tracking_uri"])

        mlflow_run_id = parametros_mlflow["mlflow_run_id"]

        with mlflow.start_run(run_id=mlflow_run_id):

            print("subir pickle modelo linear ----------------")
            # mlflow.log_artifact(path_archivo_modelo)
            # mlflow.log_metric("a")
            signature = infer_signature(X_train, model.predict(X_train))
            mlflow.sklearn.log_model(model, artifact_path="model_lineal", signature=signature)

            model_name = "modelo_lineal_energia"
            cc = f"runs:/{mlflow_run_id}/model_lineal"
            model_version = mlflow.register_model(model_uri=cc, name=model_name)
                                # mlflow.register_model(model_uri=f"runs:/{parametros_mlflow['mlflow_run_id']}/model_lineal", name=model_name)

            client = MlflowClient()

            model_alias = "challenger"
            try:
                client.get_model_version_by_alias(model_name, "champion")
            except RestException as e:
                print("Champion model not found, tagging the current model as champion")
                model_alias = "champion"

            client.set_registered_model_alias(model_version.name, model_alias, model_version.version)



        return "Task existosa"
    
    @task()
    def task_comparacion(env_vars, path_data_indices, parametros_mlflow, resultado_task  ):
        
        DATA_PATH = env_vars["data_path"] 
        # nombre_archivo_procesamiento = env_vars["nombre_archivo_procesamiento"] 
        nombre_archivo_procesamiento = env_vars["arhivo_procesamiento_"+env_vars["year"]] 
        path_data_procesamiento = DATA_PATH + nombre_archivo_procesamiento

   
        # with open(path_archivo_modelo, 'rb') as f:
        #     model = pickle.load(f)   
    
        # X_test, Y_test = get_test_data(path_data_indices, path_data_procesamiento)
    
        # y_pred = model.predict(X_test)
        # rmse = mean_squared_error(Y_test, y_pred,squared=False)
        # print(f"rmse {rmse}")



        import mlflow
        from pathlib import Path



        mlflow.set_tracking_uri(parametros_mlflow["tracking_uri"])
        mlflow_run_id = parametros_mlflow["mlflow_run_id"]

        with mlflow.start_run(run_id=mlflow_run_id):

            destination = Path("scripts/artifacts", mlflow_run_id)
            destination.mkdir(parents=True, exist_ok=True)
            client = MlflowClient()

            challenger_model_version = None
            champion_model_version = None
            model_name = "modelo_lineal_energia"



            try:
                challenger_model_version = client.get_model_version_by_alias( model_name, "challenger" )

            except mlflow.exceptions.RestException as e:
                print(f"RestException: {e}")
                # print(f"Status Code: {e.status_code}")
                print(f"Message:  No hay challenger")
                return " No challenger"



            challenger_run_id = challenger_model_version.run_id

            model_challenger = mlflow.sklearn.load_model(
                                                f"runs:/{challenger_run_id}/model_lineal",
                                                dst_path=destination    )


            champion_model_version = client.get_model_version_by_alias( model_name, "champion")
            champion_run_id = champion_model_version.run_id
            model_champion = mlflow.sklearn.load_model(
                                                f"runs:/{champion_run_id}/model_lineal",
                                                dst_path=destination    )

            
            X_test, Y_test = get_test_data(path_data_indices, path_data_procesamiento)
            y_pred_champion = model_champion.predict(X_test)
            y_pred_challenger = model_challenger.predict(X_test)
            
            rmse_test_champion = mean_squared_error(Y_test, y_pred_champion,squared=False)
            rmse_test_challenger = mean_squared_error(Y_test, y_pred_challenger,squared=False)
            print(f"year : {env_vars['year']}")

            print(f"rmse_champion dataset test : {rmse_test_champion:.2f}")
            print(f"rmse_challenger dataset test : {rmse_test_challenger:.2f}")

            mlflow.log_metrics({"year": int(env_vars['year']), 
                                f"rmse_champion dataset test ": round(rmse_test_champion,2), 
                                f"rmse_challenger dataset test ": round(rmse_test_challenger,2)})


                
            if rmse_test_challenger < rmse_test_champion:
                print("El modelo challenger es mejor")

                print("Marcando el modelo champion como archived")
                client.set_model_version_tag(
                    champion_model_version.name,
                    champion_model_version.version,
                    "archived",
                        "true")

                client.delete_registered_model_alias(
                    champion_model_version.name,
                    "champion",)
                client.delete_registered_model_alias(
                    challenger_model_version.name,
                    "challenger",)

                print("Promoviendo el modelo challenger a champion")
                client.set_registered_model_alias(
                    challenger_model_version.name,
                    "champion",
                    challenger_model_version.version,
                )
    
        return "comparacion exitosa"

    @task()
    def task_evalaucion(env_vars, path_data_indices, parametros_mlflow, resultado_comparacion):
        DATA_PATH = env_vars["data_path"] 
        # nombre_archivo_procesamiento = env_vars["nombre_archivo_procesamiento"] 
        nombre_archivo_procesamiento = env_vars["arhivo_procesamiento_"+env_vars["year"]] 
        path_data_procesamiento = DATA_PATH + nombre_archivo_procesamiento


        import mlflow
        from pathlib import Path



        mlflow.set_tracking_uri(parametros_mlflow["tracking_uri"])
        mlflow_run_id = parametros_mlflow["mlflow_run_id"]

        with mlflow.start_run(run_id=mlflow_run_id):

            destination = Path("scripts/artifacts", mlflow_run_id)
            destination.mkdir(parents=True, exist_ok=True)
            client = MlflowClient()

            champion_model_version = None
            model_name = "modelo_lineal_energia"

            champion_model_version = client.get_model_version_by_alias( model_name, "champion")
            champion_run_id = champion_model_version.run_id
            model_champion = mlflow.sklearn.load_model(
                                                f"runs:/{champion_run_id}/model_lineal",
                                                dst_path=destination    )

            
            X_test, Y_test = get_test_data(path_data_indices, path_data_procesamiento)
            y_pred_champion = model_champion.predict(X_test)
            
            rmse_test_champion = mean_squared_error(Y_test, y_pred_champion,squared=False)
            mlflow.log_metric(f"rmse_champion dataset test {env_vars['year']}",rmse_test_champion)

    env_vars = task_init_env()
    parametros_mlflow = task_init_mlflow()
    path_data_indices = task_separacion_datos(env_vars)
    resultado_task = task_entrenamiento(env_vars,path_data_indices, parametros_mlflow)

    res_comparcion = task_comparacion(env_vars,path_data_indices,parametros_mlflow , resultado_task )

    task_evalaucion(env_vars,path_data_indices,parametros_mlflow , res_comparcion )
pipeline_ML()





