import pandas as pd 
import numpy as np 
import seaborn as sb
import matplotlib.pyplot as plt
from xgboost import XGBRegressor
import xgboost
from datetime import date,timedelta
import requests
from sklearn.model_selection import train_test_split, RandomizedSearchCV

def gradient_boosting(csvfile):
    df = pd.read_csv(csvfile)
    df['YIELD'] = pd.to_numeric(df['YIELD'])
    df['DATE'] = pd.to_datetime(df['DATE'])
    x = df.iloc[:,1:4].values
    y = df.iloc[:,-1].values

    x_train,x_test,y_train,y_test = train_test_split(x,y,random_state=1,test_size=0.2)

    params = {
    "learning_rate" : [0.01,0.05,0.10],
    "max_depth" : [3,4,5],
    "n_estimators": [1100,1200,1500],
    "gamma": [0.0,0.1,0.2],
    "colsample_bytree": [0.8,0.9,1.0]
    }

    xg_regressor = XGBRegressor()
    eval_set = [(x_test,y_test)]

    random_search = RandomizedSearchCV(xg_regressor,
                                   param_distributions=params,
                                   n_iter=5,
                                   scoring='roc_auc',
                                   n_jobs=-1,
                                   cv = 5,
                                   verbose=3)

    random_search.fit(x_train,y_train,eval_metric="error",eval_set=eval_set,verbose=True)

    xg_regressor= XGBRegressor(base_score=0.5, booster='gbtree', colsample_bylevel=1,
       colsample_bytree=0.9, gamma=0.1, learning_rate=1,
       max_delta_step=0, max_depth=5, min_child_weight=7, missing=1,
       n_estimators=1200, n_jobs=1, nthread=None, random_state=0, reg_alpha=0,
       reg_lambda=1, scale_pos_weight=1, seed=None,
       subsample=1,
       objective="reg:squarederror")
    
    y_pred = random_search.predict(x_test)
    y_train_pred = random_search.predict(x_train)
    xg_regressor.fit(x,y)
    y2_pred = xg_regressor.predict(x_test)
    np.set_printoptions(precision=2)
    print(np.concatenate((y2_pred.reshape(len(y_pred),1), y_test.reshape(len(y_test),1)),1))