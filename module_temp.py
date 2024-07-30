import pandas as pd
import numpy as np 
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split,RandomizedSearchCV

def get_module_temp(csvfile):
    df = pd.read_csv(csvfile,usecols=['AMBIENT_TEMP','SUN_HOURS','MODULE_TEMP'])
    order = ['AMBIENT_TEMP','SUN_HOURS','MODULE_TEMP']
    df = df[order]
    
    x = df.iloc[:,:2].values
    y = df.iloc[:,-1].values

    params = {
    'learning_rate': [0.01, 0.05, 0.1, 0.2],
    'n_estimators': [100, 200, 500, 1000],
    'max_depth': [3, 4, 5, 6],
    'min_child_weight': [1, 5, 10],
    'gamma': [0, 0.1, 0.2, 0.3],
    'subsample': [0.6, 0.7, 0.8, 0.9, 1.0],
    'colsample_bytree': [0.6, 0.7, 0.8, 0.9, 1.0],
    'reg_alpha': [0, 0.01, 0.1, 0.5],
    'reg_lambda': [1, 1.5, 2.0, 2.5]
    }


    xg_regressor = XGBRegressor(base_score=0.5, booster='gbtree', colsample_bylevel=1,
       colsample_bytree=0.7, gamma=0.1, learning_rate=0.1,
       max_delta_step=0, max_depth=4, min_child_weight=10, missing=1,
       n_estimators=1500, n_jobs=1, nthread=None, random_state=0, reg_alpha=0.1,
       reg_lambda=1.5, scale_pos_weight=1, seed=None,
       subsample=0.6,
       objective="reg:squarederror")
    
    xg_regressor.fit(x,y)
    

get_module_temp('/Users/aditirajesh/Desktop/program_files/python/SolSight/DATA_PLANTS/plant2/data22_2.csv')
