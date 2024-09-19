
#Transformaciones de datos
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression

# como pasar argunmentos en airflow
DATA_PATH = "/opt/airflow/data/"
nombre_archivo_procesamiento = "procesamiento.csv"

def import_processed_data():
    path_data = DATA_PATH + nombre_archivo_procesamiento 
    data = pd.read_csv(path_data, parse_dates = ['Time'])
    return data

## Procesamiento


# df_model = pre_model_processing(df)


import_processed_data()


# ## Entrenamiento
# def separacion_train_test(df_model):
#     test_data = df_model.loc["2014-07-01":]
#     train_data = df_model.loc[:"2014-06-30"]
#     Y_train = train_data["demand"]
#     X_train = train_data.loc[:,~train_data.columns.isin(['demand'])]
#     Y_test = test_data["demand"]
#     X_test = test_data.loc[:,~test_data.columns.isin(['demand'])]
#     return X_train, X_test, Y_train, Y_test 

# X_train, X_test, Y_train, Y_test = separacion_train_test(df_model) 

# model = LinearRegression(n_jobs=-1)
# model.fit(X_train,Y_train)


# # Predict and Evaluation
# y_pred = model.predict(X_test)
# rmse = root_mean_squared_error(Y_test, y_pred)



