import sys
from pprint import pprint
pprint(sys.path)
from pathlib import Path

import joblib
import mlflow
import pandas as pd
output_dir = Path("data")
output_dir.mkdir(parents=True, exist_ok=True)

mlflow.set_tracking_uri("http://localhost:5555")

mlflow.set_experiment("Online Gaming Behavior - Engagement Level Prediction")
mlflow.set_experiment_tags(
    {
        "project": "Online Gaming Behavior",
        "task": "Classification",
    }
)
run = mlflow.start_run()

df = pd.read_csv(output_dir/"vic_electricity.csv")
split_test_size = 0.2
split_random_state = 42

mlflow.log_param("split_test_size", split_test_size)
mlflow.log_param("split_random_state", split_random_state)


dfi = df.head()
dfi.to_csv(output_dir / "X_test_prep.csv")
mlflow.log_artifact(output_dir / "X_test_prep.csv")