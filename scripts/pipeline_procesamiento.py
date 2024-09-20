
#Transformaciones de datos
import pandas as pd
import numpy as np
from get_env_vars import pull_env
# como pasar argunmentos en airflow
# DATA_PATH = "/opt/airflow/data/"


def import_full_data(input_data_path:str):
    # print(DATA_PATH)
    # path_data = DATA_PATH+"vic_electricity.csv"
    data = pd.read_csv(input_data_path, parse_dates = ['Time'])
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



def procesamiento(**kwargs):
    
    ti = kwargs['ti']
    DATA_PATH = ti.xcom_pull(key='data_path', task_ids='task_env')
    nombre_archivo_input = ti.xcom_pull(key='nombre_archivo_input', task_ids='task_env')
    
    print(f"tipo: {type(DATA_PATH)},{DATA_PATH}") 
    data = import_full_data(DATA_PATH+nombre_archivo_input)
    df = limpieza_datos(data)
    df = creacion_variables(df)
    df = pre_model_processing(df)
    df = df.loc["2012-01-01":]
    
    nombre_archivo_procesamiento = ti.xcom_pull(key='nombre_archivo_procesamiento', task_ids='task_env')
    path_data = DATA_PATH + nombre_archivo_procesamiento
    df.to_csv(path_data)
