
import streamlit as st
import pandas as pd
import pickle
import numpy as np

# Cargar el modelo guardado
with open('../notebooks/ufc_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Cargar el dataset de peleas (asegurándonos de que la columna 'date' está en formato datetime)
df = pd.read_csv("../data/test_prueba.csv")
df['date'] = pd.to_datetime(df['date'])  # Asegurarse de que 'date' está en formato datetime

st.title('Predicción de Round en UFC')

# 1. Obtener las fechas únicas donde hay peleas
fechas_disponibles = df['date'].dt.date.unique()

# 2. Definir el rango de fechas para la selección
fecha_inicio = pd.to_datetime('2009-02-21').date()
fecha_fin = pd.to_datetime('2016-08-06').date()

# Asegurarse de que las fechas seleccionadas estén dentro del rango de peleas disponibles
fechas_disponibles = [fecha for fecha in fechas_disponibles if fecha >= fecha_inicio and fecha <= fecha_fin]

# Si hay fechas disponibles, tomar la primera fecha como la predeterminada
fecha_seleccionada = st.date_input(
    "Fecha de la pelea", 
    value=min(fechas_disponibles),  # Selección predeterminada como la primera fecha disponible
    min_value=fecha_inicio, 
    max_value=fecha_fin, 
    key="fecha_pelea",
    format="YYYY-MM-DD"
)

# Mostrar la fecha seleccionada
st.write(f"Fecha seleccionada: {fecha_seleccionada}")

# Filtrar el dataset por la fecha seleccionada
peleas_filtradas = df[df['date'].dt.date == fecha_seleccionada]

if peleas_filtradas.empty:
    st.write("No se encontraron peleas para la fecha seleccionada.")
else:
    st.write(f"Buscando peleas para la fecha: {fecha_seleccionada}")

    # Mostrar las peleas de la fecha seleccionada
    for i, pelea in peleas_filtradas.iterrows():
        st.subheader(f"Pelea {i + 1}")
        st.write(f"Peleador 1: {pelea['peleador_1']}")
        st.write(f"Peleador 2: {pelea['peleador_2']}")
        st.write(f"Ganador: {pelea['ganador']}")

        # # Mostrar las métricas del ganador
        # ganador = pelea['ganador']
        # if ganador == pelea['peleador_1']:
        #     st.write(f"Nombre del Ganador: {pelea['peleador_1']}")
        #     st.write(f"Edad: {pelea['edad_1']}")
        #     st.write(f"Alcance: {pelea['alcance_1']} cm")
        #     st.write(f"Récord de Victorias: {pelea['victorias_1']}")
        #     st.write(f"Récord de Derrotas: {pelea['derrotas_1']}")
        # else:
        #     st.write(f"Nombre del Ganador: {pelea['peleador_2']}")
        #     st.write(f"Edad: {pelea['edad_2']}")
        #     st.write(f"Alcance: {pelea['alcance_2']} cm")
        #     st.write(f"Récord de Victorias: {pelea['victorias_2']}")
        #     st.write(f"Récord de Derrotas: {pelea['derrotas_2']}")

        # # Realizar la predicción de round con el modelo
        # st.subheader("Predicción de Round de la Próxima Pelea")
        # if st.button(f"Predecir Round de Victoria para la Pelea {i + 1}"):
        #     # Características que se usarán para hacer la predicción (ajustar según las variables de tu modelo)
        #     # Aquí estamos utilizando algunas métricas de ejemplo, puedes personalizar según tu modelo
        #     if ganador == pelea['peleador_1']:
        #         # Supongamos que estas son las características del peleador ganador
        #         características = np.array([[pelea['edad_1'], pelea['alcance_1'], pelea['victorias_1'], pelea['derrotas_1']]])
        #     else:
        #         características = np.array([[pelea['edad_2'], pelea['alcance_2'], pelea['victorias_2'], pelea['derrotas_2']]])

        #     # Realizar la predicción con el modelo
        #     prediccion_round = model.predict(características)

        #     # Mostrar el resultado de la predicción
        #     st.write(f"El modelo predice que el peleador ganador ganará en el round: {prediccion_round[0]}")