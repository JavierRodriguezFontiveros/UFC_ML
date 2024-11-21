import streamlit as st
import pandas as pd
import pickle
import time
import base64

# Cargar el dataset y el modelo
data_1 = pd.read_csv("../data/processed/metrics_media.csv", index_col="Unnamed: 0")

with open('../models/ufc_model.pkl', 'rb') as model_file:
    modelo = pickle.load(model_file)

# Funciones

def predecir_ganador(peleador_1, peleador_2):
    puntos_peleador_1 = 0
    puntos_peleador_2 = 0

    # Knockdowns
    if peleador_1['kd'] > peleador_2['kd']:
        puntos_peleador_1 += 1
    elif peleador_1['kd'] < peleador_2['kd']:
        puntos_peleador_2 += 1

    # Takedowns
    if peleador_1['td'] > peleador_2['td']:
        puntos_peleador_1 += 1
    elif peleador_1['td'] < peleador_2['td']:
        puntos_peleador_2 += 1

    # Strikes
    if peleador_1['str'] > peleador_2['str']:
        puntos_peleador_1 += 1
    elif peleador_1['str'] < peleador_2['str']:
        puntos_peleador_2 += 1

    # Submissions
    if peleador_1['sub'] > peleador_2['sub']:
        puntos_peleador_1 += 1
    elif peleador_1['sub'] < peleador_2['sub']:
        puntos_peleador_2 += 1

    # Determinar el ganador basado en los puntos
    if puntos_peleador_1 > puntos_peleador_2:
        return peleador_1['fighter']
    elif puntos_peleador_2 > puntos_peleador_1:
        return peleador_2['fighter']
    else:
        # Desempate basado en strikes
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
# Pestañas
tab1, tab2 = st.tabs(["Aplicación", "Documentación del Modelo"])

# **Tab 1: Predicción Individual**
with tab1:

    # Crear una columna para centrar la imagen
    col1, col2, col3 = st.columns([1, 3, 1])

    imagen_bienvenida = "../data/images/logo.png"  # Reemplaza con la ruta correcta de tu imagen

    with col2:
        st.image(imagen_bienvenida)
        st.write("¡Simula peleas de UFC, predice ganadores y mucho más!")

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




    # Crear una pestaña para el combate específico
    with st.sidebar:
        selected_option = st.radio("Selecciona una opción", ["Inicio", "EXTRA: Combate Ilia vs Max Holloway"])

    if selected_option == "EXTRA: Combate Ilia vs Max Holloway":
        # Sección de combate EXTRA
        st.subheader("EXTRA: Combate Ilia Topuria vs Max Holloway")

        # Mostrar imagen solo si es necesario
        if "mostrar_imagen" not in st.session_state:
            st.session_state["mostrar_imagen"] = False

        # Botón para mostrar/ocultar la imagen
        if st.button("Mostrar imagen"):
            st.session_state["mostrar_imagen"] = not st.session_state["mostrar_imagen"]

        # Mostrar la imagen si el estado lo permite
        if st.session_state["mostrar_imagen"]:
            imagen_path = "../data/images/combate_pred.png"
            st.image(imagen_path, caption="Esta es la imagen que pediste.")


        if st.button("Simular combate EXTRA"):
            peleador_1 = {'fighter': 'Ilia Topuria', 'kd': 1, 'td': 2, 'str': 75, 'sub': 0}
            peleador_2 = {'fighter': 'Max Holloway', 'kd': 0, 'td': 0, 'str': 79, 'sub': 0}

            # Crear las métricas para el DataFrame
            row = {
                'r_kd': peleador_1['kd'],
                'b_kd': peleador_2['kd'],
                'r_str': peleador_1['str'],
                'b_str': peleador_2['str'],
                'r_td': peleador_1['td'],
                'b_td': peleador_2['td'],
                'r_sub': peleador_1['sub'],
                'b_sub': peleador_2['sub'],
                'weight_class': 2  # Asumiendo que ambos están en Peso Ligero
            }

            df = pd.DataFrame([row])

            # Predicción con el modelo cargado
            resultado = modelo.predict(df)
            round = int(resultado // 5)
            minuto = int(resultado - (round * 5))

            peleador_2 = {'fighter': 'Ilia Topuria', 'kd': 1, 'td': 2, 'str': 75, 'sub': 0,"weight_class":2}
            peleador_1 = {'fighter': 'Max Holloway', 'kd': 0, 'td': 0, 'str': 79, 'sub': 0,"weight_class":2}
            
            # Mostrar resultados en la interfaz
            st.write(f"**Ganador del combate:** {predecir_ganador(peleador_1,peleador_2)}")
            st.write(f"**Round:** {round}")
            st.write(f"**Minuto:** {minuto}")



with tab2:

    st.title("Modelo utilizado: RandomForest Regressor")
    st.write("El modelo utilizado para predecir los resultados de las peleas es un **RandomForest Regressor**. "
        "Este modelo tiene un error medio de predicción de **2 minutos** en el tiempo estimado del combate en un rango de **0 a 25 minutos**")
    st.write("Las variables con más peso dentro del modelo son:")

    imagen_modelo = "../data/images/feature_importance.png" 
    st.image(imagen_modelo, caption="Gráfico representativo del modelo")

    # También puedes agregar más detalles si lo necesitas:
    st.write(
        "Este modelo ha sido entrenado con datos de peleas previas y utiliza características como el número de golpes, "
        "takedowns, y sumisiones para hacer sus predicciones."
    )
