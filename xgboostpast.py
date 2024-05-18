import pandas as pd 
import numpy as np 
from xgboost import XGBRegressor
import xgboost
from datetime import date,timedelta
from sklearn.model_selection import train_test_split
import warnings 
xgboost.set_config(verbosity=0)
warnings.filterwarnings('ignore')


def xg_boost_past(user,key):
    path =f'./datasets/{user}/{key}'
    df = pd.read_csv(path)

    df['YIELD'] = pd.to_numeric(df['YIELD'])
    df['DATE'] = pd.to_datetime(df['DATE'])

    x = df.iloc[:,1:4].values
    y = df.iloc[:,-1].values

    x_train,x_test,y_train,y_test = train_test_split(x,y,random_state=1,test_size=0.2, shuffle=False)
    xg_regressor = XGBRegressor()

    xg_regressor= XGBRegressor(base_score=0.5, booster='gbtree', colsample_bylevel=1,
        colsample_bytree=0.9, gamma=0.1, learning_rate=1,
        max_delta_step=0, max_depth=5, min_child_weight=7, missing=1,
        n_estimators=1200, n_jobs=1, nthread=None, random_state=0, reg_alpha=0,
        reg_lambda=1, scale_pos_weight=1, seed=None,
        subsample=1,
        objective="reg:squarederror")

    xg_regressor.fit(x,y)
    y2_pred = xg_regressor.predict(x_test)
    np.set_printoptions(precision=2)
    return (np.concatenate((y2_pred.reshape(len(y2_pred),1), y_test.reshape(len(y_test),1)),1))

if __name__=='__main__':
    print(xg_boost_past('adharsh_18','data16_1.csv'))