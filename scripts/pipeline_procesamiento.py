
#Transformaciones de datos
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression

# como pasar argunmentos en airflow
DATA_PATH = "/opt/airflow/data/"


def import_full_data():
    path_data = DATA_PATH+"vic_electricity.csv"
    data = pd.read_csv(path_data, parse_dates = ['Time'])
    return data

## Procesamiento

def limpieza_datos(data):
    data.columns = [c.lower() for c in data.columns.tolist()]

    data.rename(columns={"time":"date_time"},inplace=True)
    data = data.loc[:,['date_time', 'demand', 'temperature', 'holiday']]
    data["date"] = data.date_time.dt.date
    data["hour"] = data.date_time.dt.hour
    data["year"] = data.date_time.dt.year
    data["mes"] = data.date_time.dt.month

    df = data.set_index("date_time")
    df = df.resample("1h").first()
    return df


def creacion_variables(df):
    df = shift_demand(df, horas_anteriores=11)
    df = moving_avg(df, horas_mv_avg_list=5)
    return df


def shift_demand(df,horas_anteriores):
  for horas in range(1,horas_anteriores):
    df[f'demand_lag_{horas}h'] = df.demand.shift(horas, fill_value=0)
  return df


def moving_avg(df, horas_mv_avg_list):
    for hora in range(1,horas_mv_avg_list):
        df[f"mv_avg_{hora}"] = df.demand.shift(1, fill_value=0).rolling(hora).agg(['mean'])
    return df


def pre_model_processing(df):
    df2 = df.copy()
    holiday = np.where(df2["holiday"]== True,1,0)
    df2["holiday_num"] = holiday
    
    new_columns = [c for c in df.columns.tolist() if c not in ["date", "holiday"]]
    return df2[new_columns]



def procesamiento():
    data = import_full_data()
    df = limpieza_datos(data)
    df = creacion_variables(df)
    df = pre_model_processing(df)
    df = df.loc["2012-01-01":]
    print(f"version pandas: {pd.__version__}")
    path_data = DATA_PATH +"procesamiento.csv"
    df.to_csv(path_data)


# df_model = pre_model_processing(df)




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



