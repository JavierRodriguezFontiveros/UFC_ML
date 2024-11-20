#Data
import pandas as pd

train= pd.read_csv("../data/train/train.csv", index_col="Unnamed: 0")



#Train/test del train
from sklearn.model_selection import train_test_split

X = train.drop(columns=["time"])
y = train["time"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


#Mejor modelo RandomForestRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error

rf_tuned = RandomForestRegressor(n_estimators=200,
                                 max_depth=10,
                                 min_samples_split=5,
                                 random_state=42)

rf_tuned.fit(X_train, y_train)
y_pred_rf_tuned = rf_tuned.predict(X_test)


#Evaluación del modelo
mae_rf = mean_absolute_error(y_test, y_pred_rf_tuned)
mse_rf = mean_squared_error(y_test, y_pred_rf_tuned)

print(f"Mean Absolute Error (MAE): {mae_rf}")
print(f"Mean Squared Error (MSE): {mse_rf}")


#Guardar Modelo
import pickle

with open('../models/ufc_model.pkl', 'wb') as model_file:
    pickle.dump(rf_tuned, model_file)

print("Modelo RandomForestRegressor guardado exitosamente en 'ufc_model.pkl'")