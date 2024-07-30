from plant_processing import Source 
import pandas as pd 
import matplotlib.pyplot as plt 
import numpy as np 
from datetime import date
from sklearn.impute import SimpleImputer 
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

def linear_regression(csvfile):

    dataset = pd.read_csv(csvfile)
    x = dataset.iloc[:,1:4].values
    y = dataset.iloc[:,-1].values

    imputer = SimpleImputer(missing_values=np.nan,strategy='mean')   #replacing all the missing values in the dataset with the mean.
    imputer.fit(x[:,:]) #connects the imputer to the matriX of features 
    x[:,:] = imputer.transform(x[:,:])
    x_train, x_test, y_train, y_test = train_test_split(x,y, test_size = 0.2, random_state=1)

    regressor = LinearRegression()
    model = regressor.fit(x_train, y_train) 
    y_pred = regressor.predict(x_test)
    y_pred_train = regressor.predict(x_train)
    np.set_printoptions(precision=2)
    print(np.concatenate((y_pred.reshape(len(y_pred),1), y_test.reshape(len(y_test),1)),1))

    mse = mean_squared_error(y_test,y_pred)
    rmse = np.sqrt(mse)
    print(rmse)

linear_regression("/Users/aditirajesh/Desktop/program_files/python/SolSight/DATA_PLANTS/plant1/data15_1.csv")





