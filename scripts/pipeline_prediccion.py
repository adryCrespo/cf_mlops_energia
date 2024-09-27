
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression
import pickle

# como pasar argunmentos en airflow
# DATA_PATH = "/opt/airflow/data/"
# nombre_archivo_procesamiento = "procesamiento.csv"

def import_processed_data(path_data):
    # path_data = DATA_PATH + nombre_archivo_procesamiento 
    data = pd.read_csv(path_data, parse_dates = ['date_time'])
    # data.set_index("date_time", inplace=True)
    return data




# ## Entrenamiento
def separacion_train_test(df_model):
    test_data = df_model.loc["2014-07-01":]
    train_data = df_model.loc[:"2014-06-30"]
    Y_train = train_data["demand"]
    X_train = train_data.loc[:,~train_data.columns.isin(['demand'])]
    Y_test = test_data["demand"]
    X_test = test_data.loc[:,~test_data.columns.isin(['demand'])]
    return X_train, X_test, Y_train, Y_test 


def separacion(**kwargs):
    
    
    ti = kwargs['ti']
    DATA_PATH = ti.xcom_pull(key='data_path', task_ids='task_env')
    nombre_archivo_procesamiento = ti.xcom_pull(key='nombre_archivo_procesamiento', task_ids='task_env')
    
    print(f"DATA_PATH: {DATA_PATH},{type(DATA_PATH)}")
    print(f"nombre_archivo_procesamiento: {nombre_archivo_procesamiento},{type(nombre_archivo_procesamiento)}")
    
    path_data_procesamiento = DATA_PATH + nombre_archivo_procesamiento
    
    df_model = import_processed_data(path_data_procesamiento )
    X_train, _ , i_ , _ = separacion_train_test(df_model) 
    serie_indices = X_train.reset_index()[["index"]]

    
    nombre_archivo_index = ti.xcom_pull(key='nombre_archivo_index', task_ids='task_env')
    
    print(f"nombre_archivo_index: {nombre_archivo_index},{type(nombre_archivo_index)}")
    path_data_indieces = DATA_PATH + nombre_archivo_index 
    serie_indices.to_csv(path_data_indieces )


################################################

def import_indices(path_data_indices):

    # path_data = DATA_PATH + "index.csv" 
    data = pd.read_csv(path_data_indices)
    # print(data.head())
    return data

def get_training_data(path_data_indices, path_data_procesamiento):
    
    
    df_model = import_processed_data(path_data_procesamiento )

    indices_entrenamiento = import_indices(path_data_indices)["index"]
    df_train = df_model.iloc[indices_entrenamiento.tolist(),:]

    X, Y = df_train.loc[:,~df_train.columns.isin(["demand"])], df_train["demand"] 
    return X.set_index("date_time"), Y


def entrenamiento(**kwargs):

   ti = kwargs['ti']
   DATA_PATH = ti.xcom_pull(key='data_path', task_ids='task_env')
   nombre_archivo_index = ti.xcom_pull(key='nombre_archivo_index', task_ids='task_env')
   nombre_archivo_procesamiento = ti.xcom_pull(key='nombre_archivo_procesamiento', task_ids='task_env')
   print(f"DATA_PATH: {DATA_PATH},{type(DATA_PATH)}")
   print(f"nombre_archivo_procesamiento: {nombre_archivo_procesamiento},{type(nombre_archivo_procesamiento)}")
    
   print(f"nombre_archivo_index: {nombre_archivo_index},{type(nombre_archivo_index)}")
   
   path_data_procesamiento = DATA_PATH + nombre_archivo_procesamiento
   path_data_indices = DATA_PATH + nombre_archivo_index 
   
   X_train, Y_train = get_training_data(path_data_indices, path_data_procesamiento) 
   print(X_train.columns.tolist())
   
   model = LinearRegression(n_jobs=-1)
   model.fit(X_train,Y_train)

   nombre_archivo_modelo = ti.xcom_pull(key='nombre_archivo_modelo' , task_ids='task_env')
   with open(DATA_PATH+nombre_archivo_modelo, 'wb') as f:
    pickle.dump(model, f)
   
######################
# EVALUACION

def get_test_data(path_data_indices, path_data_procesamiento):
   
   df_model = import_processed_data(path_data_procesamiento )
   indices_entrenamiento = import_indices(path_data_indices)["index"]

   total_indices = pd.Series([i for i in range(df_model.shape[0])])
   train_indices_bool = total_indices.isin(indices_entrenamiento)
   test_indices_bool = ~train_indices_bool

   df_test = df_model.loc[test_indices_bool,:]
    
   X, Y = df_test.loc[:,~df_test.columns.isin(["demand"])], df_test["demand"]    
   return X.set_index("date_time"), Y

def evaluacion(**kwargs):

    ti = kwargs['ti']
    DATA_PATH = ti.xcom_pull(key='data_path', task_ids='task_env')

    nombre_archivo_modelo = ti.xcom_pull(key='nombre_archivo_modelo' , task_ids='task_env')
    nombre_archivo_index = ti.xcom_pull(key='nombre_archivo_index', task_ids='task_env')

    path_data_procesamiento = DATA_PATH + nombre_archivo_procesamiento
    path_data_indices = DATA_PATH + nombre_archivo_index 
   
    with open(DATA_PATH+nombre_archivo_modelo, 'rb') as f:
        model = pickle.load(f)   
    
    X_test, Y_test = get_test_data(path_data_indices, path_data_procesamiento)
    # X_test, Y_test = get_test_data()
    y_pred = model.predict(X_test)
    rmse = mean_squared_error(Y_test, y_pred,squared=False)
    print(f"rmse {rmse}")



if __name__ == "__main__":
   
   DATA_PATH = "data/"
   entrenamiento()










## Procesamiento

# print(df.columns.tolist())

# print(df.shape)
# print(df.index)