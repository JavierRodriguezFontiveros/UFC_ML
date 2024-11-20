#Data:
import pandas as pd

test= pd.read_csv("../data/train/train.csv", index_col="Unnamed: 0")


#Cargar modelo:
import pickle

with open('../models/ufc_model.pkl', 'rb') as model_file:
    rf_tuned = pickle.load(model_file)


#Dividir el Test:
X_real = test.drop(columns=["time"])
y_real= test["time"]


#Probamos como generaliza:
from sklearn.metrics import mean_squared_error, mean_absolute_error

mae_rf = mean_absolute_error(y_real, rf_tuned.predict(X_real))
mse_rf = mean_squared_error(y_real, rf_tuned.predict(X_real))

print(f'Mean Absolute Error (MAE): {mae_rf}')
print(f"Mean Squared Error (MSE): {mse_rf}")

