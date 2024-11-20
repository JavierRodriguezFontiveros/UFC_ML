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


#Guardar .yaml:
import yaml


configuracion_modelo = {"modelo": {
        "nombre": "RandomForestRegressor",
        "descripcion": "Modelo Random Forest optimizado para predecir el tiempo de combate."
    },
    "parametros": {
        "n_estimators": rf_tuned.n_estimators,
        "max_depth": rf_tuned.max_depth,
        "min_samples_split": rf_tuned.min_samples_split,
        "random_state": rf_tuned.random_state
    },
    "entrenamiento": {
        "datos": {
            "ruta_train": "../data/train/train.csv",
            "columnas_predictoras": [
                "r_kd", "b_kd", "r_str", "b_str", "r_td", 
                "b_td", "r_sub", "b_sub", "weight_class"
            ],
            "columna_objetivo": "time"
        },
        "validacion": {
            "test_size": 0.2,
            "random_state": 42
        }
    },
    "evaluacion": {
        "metricas": {
            "mean_absolute_error": mae_rf,
            "mean_squared_error": mse_rf
        }
    },
    "modelo_guardado": {
        "ruta": "../models/ufc_model.pkl",
        "formato": "pickle"
    }
}

# Guardar el diccionario como un archivo YAML
with open('../models/model_config.yaml', 'w') as yaml_file:
    yaml.dump(configuracion_modelo, yaml_file, default_flow_style=False)

print("Archivo 'model_config.yaml' generado exitosamente.")

