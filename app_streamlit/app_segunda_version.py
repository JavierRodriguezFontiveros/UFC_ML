import streamlit as st
import pandas as pd
import pickle
import numpy as np
from datetime import datetime


with open('../models/ufc_model.pkl', 'rb') as f:
    model = pickle.load(f)



df = pd.read_csv("../data/test_prueba.csv")

df['date'] = pd.to_datetime(df['date'])

st.title('Predicción de Round en UFC')
st.subheader('Selecciona una fecha para la pelea')

fecha_seleccionada = st.date_input("Fecha de la pelea", min_value=df['date'].min().date(), max_value=df['date'].max().date())

fecha_seleccionada_dt = pd.to_datetime(fecha_seleccionada)

peleas_filtradas = df[df['date'] == fecha_seleccionada_dt]

# Si hay peleas para la fecha seleccionada
if not peleas_filtradas.empty:
    st.write(f"Se encontraron {len(peleas_filtradas)} peleas para la fecha {fecha_seleccionada_dt.date()}:")
    
    # Crear una lista de nombres para las peleas como "Pelea 1", "Pelea 2", etc.
    pelea_nombres = [f"Pelea {i+1}" for i in range(len(peleas_filtradas))]

    # Mostrar las peleas y permitir seleccionar una
    pelea_seleccionada_index = st.selectbox(
        "Selecciona una pelea:",
        pelea_nombres
    )

    # Obtener el índice de la pelea seleccionada
    pelea_seleccionada = peleas_filtradas.iloc[pelea_nombres.index(pelea_seleccionada_index)]
    
    # Mostrar las métricas de la pelea seleccionada
    st.write(f"Métricas para la {pelea_seleccionada_index} del {fecha_seleccionada_dt.date()}:")
    st.write(f"Método de victoria: {pelea_seleccionada['method']}")

    st.write(f"Tiempo: {pelea_seleccionada['time']}")
    st.write(f"Knockdowns: {pelea_seleccionada['kd']}")
    st.write(f"Golpes significativos: {pelea_seleccionada['str']}")
    st.write(f"Derribos: {pelea_seleccionada['td']}")
    st.write(f"Sumisiones: {pelea_seleccionada['sub']}")
    
    # Botón para predecir el round
    if st.button(f"Predecir Round para la {pelea_seleccionada_index} del {fecha_seleccionada_dt.date()}", key=f"prediccion_{fecha_seleccionada_dt.date()}"):
        características = np.array([[pelea_seleccionada['kd'], pelea_seleccionada['str'], pelea_seleccionada['td'], pelea_seleccionada['sub'],pelea_seleccionada['method']]])

        # Realizar la predicción con el modelo
        predicción = model.predict(características)

        # Mostrar la predicción
        st.write(f"La predicción para el round es: {predicción[0]}")
else:
    st.write("No se encontraron peleas para esta fecha.")



