import streamlit as st
import pandas as pd
import pickle
import time

# Cargar el dataset y el modelo
data_1 = pd.read_csv("../data/processed/metrics_media.csv", index_col="Unnamed: 0")

with open('../models/ufc_model.pkl', 'rb') as model_file:
    modelo = pickle.load(model_file)

# Funciones

def predecir_ganador(peleador_1, peleador_2):
    peso_influencia = {4: 1.5, 3: 1.25, 2: 1.3}
    puntos_peleador_1 = 0
    puntos_peleador_2 = 0

    peso_1 = peso_influencia.get(peleador_1['weight_class'], 1.0)
    peso_2 = peso_influencia.get(peleador_2['weight_class'], 1.0)
        
    if peleador_1['kd'] * peso_1 > peleador_2['kd'] * peso_2:
        puntos_peleador_1 += 1
    else:
        puntos_peleador_2 += 1

    # Takedowns
    if peleador_1['td'] > peleador_2['td']:
        puntos_peleador_1 += 1
    else:
        puntos_peleador_2 += 1

    # Strikes 
    if peleador_1['str'] * peso_1 > peleador_2['str'] * peso_2:
        puntos_peleador_1 += 1
    else:
        puntos_peleador_2 += 1

    # Submissions
    if peleador_1['sub'] > peleador_2['sub']:
        puntos_peleador_1 += 1
    else:
        puntos_peleador_2 += 1

    # Sistema de puntuaciones final
    if puntos_peleador_1 > puntos_peleador_2:
        return peleador_1['fighter']
    elif puntos_peleador_2 > puntos_peleador_1:
        return peleador_2['fighter']
    else:
        if peleador_1['str'] > peleador_2['str']:
            return peleador_1['fighter']
        elif peleador_2['str'] > peleador_1['str']:
            return peleador_2['fighter']
        else:
            return "Empate"


def generar_enfrentamiento(df, peleador_1_id, peleador_2_id):
    peleador_1 = df[df['fighter'] == peleador_1_id].iloc[0]
    peleador_2 = df[df['fighter'] == peleador_2_id].iloc[0]
    
    if peleador_1['weight_class'] != peleador_2['weight_class']:
        raise ValueError("Los peleadores no están en la misma categoría de peso.")
    
    metrics = {'r_fighter': peleador_1['fighter'],
               'b_fighter': peleador_2['fighter'],
               'r_kd': peleador_1['kd'],
               'b_kd': peleador_2['kd'],
               'r_str': peleador_1['str'],
               'b_str': peleador_2['str'],
               'r_td': peleador_1['td'],
               'b_td': peleador_2['td'],
               'r_sub': peleador_1['sub'],
               'b_sub': peleador_2['sub'],
               'weight_class': peleador_1['weight_class']}
    
    df_versus = pd.DataFrame([metrics])
    return df_versus



def apuesta(peleador_1, peleador_2, modelo, metrics_media):
    peleador_1_data = metrics_media[metrics_media['fighter'] == peleador_1].iloc[0]
    peleador_2_data = metrics_media[metrics_media['fighter'] == peleador_2].iloc[0]

    # Generar las métricas para el enfrentamiento
    versus = generar_enfrentamiento(metrics_media, peleador_1, peleador_2)
    versus = versus.drop(columns=["r_fighter", "b_fighter"])

    # Predicción del ganador
    ganador = predecir_ganador(peleador_1_data, peleador_2_data)

    # Predicción del round y minuto
    resultado = float(modelo.predict(versus)[0])
    round = resultado // 5
    minuto = resultado / 5
    resto = int(minuto)
    parte_decimal = minuto - resto
    
    # Redondear al alza si es necesario
    if parte_decimal >= 0.5:
        resto += 1

    return ganador, int(round), resto



# Interfaz de Streamlit
# Título
st.title("Predicción de Peleas UFC")

# Selección de categoría
category_mapping = {"Peso Ligero": 2, "Peso Medio": 3, "Peso Pesado": 4}
category = st.selectbox("Elige la categoría de pelea", ["Selecciona una categoría", "Peso Ligero", "Peso Medio", "Peso Pesado"])

if category != "Selecciona una categoría":
    st.write(f"Has seleccionado: **{category}**")
    category_value = category_mapping[category]
    filtered_fighters = data_1[data_1["weight_class"] == category_value]["fighter"].tolist()

    # Selección de peleadores
    fighter1 = st.selectbox("Selecciona el peleador 1", ["Selecciona un peleador"] + filtered_fighters)
    fighter2 = st.selectbox("Selecciona el peleador 2", ["Selecciona un peleador"] + filtered_fighters)

    if fighter1 and fighter2 and fighter1 != fighter2:
        if 'resultado' not in st.session_state:
            st.session_state['resultado'] = None
            st.session_state['round'] = None
            st.session_state['minuto'] = None

        # Botón para predecir el ganador
        if st.button("Predecir quién ganará"):
            ganador, round, minuto = apuesta(fighter1, fighter2, modelo, data_1)
            st.session_state['resultado'] = ganador
            st.session_state['round'] = round
            st.session_state['minuto'] = minuto
            st.write(f"El ganador es: **{ganador}**")
        
        # Botón para predecir el round
        if st.session_state['resultado'] is not None and st.button("Predecir en qué round"):
            st.write(f"El round será: **{st.session_state['round']}**")

        # Botón para predecir el minuto
        if st.session_state['round'] is not None and st.button("Predecir en qué minuto"):
            st.write(f"El minuto será: **{st.session_state['minuto']}**")
