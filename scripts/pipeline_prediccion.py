
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression
import pickle

# como pasar argunmentos en airflow
DATA_PATH = "/opt/airflow/data/"
nombre_archivo_procesamiento = "procesamiento.csv"

def import_processed_data():
    path_data = DATA_PATH + nombre_archivo_procesamiento 
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


def separacion():
    df_model = import_processed_data()
    X_train, X_test, Y_train, Y_test = separacion_train_test(df_model) 
    serie_indices = X_train.reset_index()[["index"]]


    path_data = DATA_PATH +"index.csv"
    serie_indices.to_csv(path_data)
    print(serie_indices.shape)


################################################

def import_indices():

    path_data = DATA_PATH + "index.csv" 
    data = pd.read_csv(path_data)
    print(data.head())
    return data

def get_training_data():
    
   df_model = import_processed_data()
   indices_entrenamiento = import_indices()["index"]
   df_train = df_model.iloc[indices_entrenamiento.tolist(),:]

   X, Y = df_train.loc[:,~df_train.columns.isin(["demand"])], df_train["demand"] 
   return X.set_index("date_time"), Y

def get_test_data():  
   
   df_model = import_processed_data()
   indices_entrenamiento = import_indices()["index"]
   total_indices = pd.Series([i for i in range(df_model.shape[0])])
   train_indices_bool = total_indices.isin(indices_entrenamiento)
   test_indices_bool = ~train_indices_bool

   df_test = df_model.loc[test_indices_bool,:]
    
   X, Y = df_test.loc[:,~df_test.columns.isin(["demand"])], df_test["demand"]    
   return X.set_index("date_time"), Y

def entrenamiento():
   X_train, Y_train = get_training_data() 
   print(X_train.columns.tolist())
   
   model = LinearRegression(n_jobs=-1)
   model.fit(X_train,Y_train)
   with open(DATA_PATH+'model.pkl', 'wb') as f:
    pickle.dump(model, f)
   
######################
# EVALUACION

def evaluacion():
    with open(DATA_PATH+'model.pkl', 'rb') as f:
        model = pickle.load(f)   
    
    X_test, Y_test = get_test_data()
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