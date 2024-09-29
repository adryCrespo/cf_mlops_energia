
import mlflow


def mlflow_experiment_init():
    tracking_uri = "http://tracking_server:5000"
    # tracking_uri = "tracking_server"
    mlflow.set_tracking_uri(tracking_uri)
    print("Setting tracking uri -------------") 
    

    # experiment_id = mlflow.create_experiment("Prediccion demanda energia3")
    mlflow.set_experiment("Prediccion demanda energia2")
    mlflow.set_experiment_tags(
        {
            "project": "CF_MLOPS_Energia",
            "task": "Classification",
        }
    )
    run = mlflow.start_run()
    mlflow_run_id = run.info.run_id
    parametros_mlflow = {"mlflow_run_id":mlflow_run_id, "tracking_uri":tracking_uri}
    mlflow.end_run()
    return parametros_mlflow

    

