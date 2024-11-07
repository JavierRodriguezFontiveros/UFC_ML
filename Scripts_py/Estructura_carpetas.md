# UFC_ML

# Estructura de Carpetas del Proyecto

## data
Almacenará los datos utilizados en el proyecto, organizada en las siguientes subcarpetas:

- **raw**: datos en su formato original, sin procesar.
- **processed**: datos transformados y listos para su uso.
- **train**: datos de entrenamiento, derivados de `processed`.
- **test**: datos de prueba, derivados de `processed`.

---

## notebooks
Archivos Jupyter Notebook con el desarrollo del proyecto, numerados para indicar su orden:

- **01_Fuentes.ipynb**: adquisición y unificación de datos.
- **02_LimpiezaEDA.ipynb**: limpieza, transformación, análisis exploratorio y visualización.
- **03_Entrenamiento_Evaluacion.ipynb**: entrenamiento y evaluación de modelos.

---

## src
Contiene el código fuente en Python que implementa funcionalidades clave:

- **data_processing.py**: procesamiento de datos desde `data/raw` hacia `data/processed`.
- **training.py**: entrenamiento y guardado de modelos usando datos de `data/processed`.
- **evaluation.py**: evaluación de los modelos usando los datos de `data/test`.

---

## models
Archivos relacionados con el modelo entrenado:

- **trained_model_n.pkl**: modelo(s) entrenado(s), donde _n_ es el identificador.
- **final_model.pkl**: modelo final en formato pickle.
- **model_config.yaml**: configuración y parámetros del modelo final.

---

## app_streamlit
Archivos para el despliegue del modelo en Streamlit:

- **app.py**: aplicación web para ejecutar el modelo entrenado.
- **requirements.txt**: dependencias necesarias para ejecutar la app.

---

## docs
Documentación adicional:

- **negocio.ppt**: presentación de negocio.
- **ds.ppt**: presentación de datos.
- **memoria.md**: documentación detallada del proyecto.

---

## README.md
Portada del proyecto y guía general.