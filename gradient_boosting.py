import pandas as pd 
import numpy as np 
from xgboost import XGBRegressor
import datetime
from sklearn.model_selection import train_test_split,RandomizedSearchCV
from extract_data import request_data
import time 
import pytz

def realtime_data(user,key):
    path =f'./datasets/{user}/{key}.csv'
    df = pd.read_csv(path)
    df['YIELD'] = pd.to_numeric(df['YIELD'])
    df['DATE'] = pd.to_datetime(df['DATE'])

    x = df.iloc[:,1:4].values
    y = df.iloc[:,-1].values

    #x_train,x_test,y_train,y_test = train_test_split(x,y,random_state=1)

    xg_regressor_yield= XGBRegressor(base_score=0.5, booster='gbtree', colsample_bylevel=1,
       colsample_bytree=0.9, gamma=0.1, learning_rate=1,
       max_delta_step=0, max_depth=5, min_child_weight=7, missing=1,
       n_estimators=1200, n_jobs=1, nthread=None, random_state=0, reg_alpha=0,
       reg_lambda=1, scale_pos_weight=1, seed=None,
       subsample=1,
       objective="reg:squarederror")
    
    xg_regressor_yield.fit(x,y)
    print('regression complete')

    df_module = pd.read_csv(path,usecols=['AMBIENT_TEMP','SUN_HOURS','MODULE_TEMP'])
    order = ['AMBIENT_TEMP','SUN_HOURS','MODULE_TEMP']
    df_module = df_module[order]
    
    x = df_module.iloc[:,:2].values
    y = df_module.iloc[:,-1].values

    xg_regressor_module = XGBRegressor(base_score=0.5, booster='gbtree', colsample_bylevel=1,
       colsample_bytree=0.7, gamma=0.1, learning_rate=0.1,
       max_delta_step=0, max_depth=4, min_child_weight=10, missing=1,
       n_estimators=1500, n_jobs=1, nthread=None, random_state=0, reg_alpha=0.1,
       reg_lambda=1.5, scale_pos_weight=1, seed=None,
       subsample=0.6,
       objective="reg:squarederror")
    
    xg_regressor_module.fit(x,y)

    data = request_data()

    input_data = pd.DataFrame({
        'AMBIENT_TEMP':[data[0]],
        'SUN_HOURS':[data[1]]
    })

    module_temperature = xg_regressor_module.predict(input_data)


 
    global ambient_temp,modular_temp,irradiance,yield_obtained
    ambient_temp = []
    modular_temp = []
    irradiance = []
    yield_obtained = None

    data = [data[0],module_temperature[0],data[1]]
    ambient_temp.append(data[0])
    modular_temp.append(data[1])
    irradiance.append(data[2])

    ambient_mean = sum(ambient_temp)/len(ambient_temp)
    modular_mean = sum(modular_temp)/len(modular_temp)
    sunhours = sum(irradiance)/4

    print('ambient temps: ',ambient_temp)
    print('modular temps: ',modular_temp)
    print('irradiances: ',irradiance)

    input_data = pd.DataFrame({
        'AMBIENT_TEMP': [ambient_mean],
        'MODULE_TEMP':[modular_mean],
        'SUNHOURS':[sunhours]
    })

    yield_obtained = xg_regressor_yield.predict(input_data)[0]
    tz = pytz.timezone('Asia/Kolkata')
    current_time = datetime.datetime.now(tz) 
    str_time = current_time.strftime("%H:%M:%S")

    print('Yield Obtained at',str_time,'is: ',yield_obtained)
    return yield_obtained,irradiance,ambient_temp,modular_temp
if __name__ == "__main__":
    realtime_data('user1','panel2')




    






