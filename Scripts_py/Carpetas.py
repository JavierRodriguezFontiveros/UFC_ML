#--------------Bibliotecas----------------#

import os

#-------------------------------------------Diccionario-----------------------------------#
estructura = {"data/raw/dataset.csv",    
              "data/processed",          
              "data/train",              
              "data/test",               
              "notebooks/01_Fuentes.ipynb",
              "notebooks/02_LimpiezaEDA.ipynb",
              "notebooks/03_Entrenamiento_Evaluacion.ipynb",
              "src/data_processing.py",
              "src/training.py",
              "src/evaluation.py",
              "models/trained_model.pkl",
              "models/model_config.yaml",
              "app_streamlit/app.py",
              "app_streamlit/requirements.txt",
              "docs/negocio.ppt",
              "docs/ds.ppt",
              "docs/memoria.md"}


#-----------------------Funcion-----------------------------#

def crear_estructura(estructura):
    for elemento in estructura:
        ruta_completa = os.path.join(elemento)

        if "." in os.path.basename(ruta_completa):
            os.makedirs(os.path.dirname(ruta_completa), exist_ok=True)
            with open(ruta_completa, 'w') as f:
                f.write("")
        else:
            os.makedirs(ruta_completa, exist_ok=True)  



#----------------------Uso----------------------------#
crear_estructura(estructura)
print("Estructura de carpetas y archivos creada correctamente.")
