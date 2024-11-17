

# ¿ Que quiero que salga en la aplicacion (de momento)?

# 1. Slogan de la página: escoge tus peleadores favoritos
# 2. Boton de categorias
# 3. Escoger dos peleadores
# 4. Se genere el enfrentamiento
# 5. Haya un contador regresivo
# 6. Boton Para Predecir Ganador
# 7. Estas seguro de querer saber en que round?
# 8. Predecir round
# 9. No me hago responsable de tus actos
# 10. Predecir minutos

# Extra: Tener preparado el combate de topuria vs Holloway
# Mostrar: - documentacion en una pestaña aparte
#          - gráfica de como predice el modelo etc..



import streamlit as st
import time

# 1. Slogan de la página
st.title("¡Escoge tus peleadores favoritos!")

# 2. Botón para seleccionar categorías
category = st.selectbox("Elige la categoría de pelea", ["Selecciona una categoría", "Peso Ligero", "Peso Pesado", "Peso Welter", "Peso Pluma"])

# Usamos session_state para mantener las selecciones entre interacciones
if 'category' not in st.session_state:
    st.session_state.category = category

if category != "Selecciona una categoría":
    st.session_state.category = category
    # 3. Escoger dos peleadores
    st.subheader("Escoge los dos peleadores")
    fighter1 = st.selectbox("Peleador 1", ["Selecciona un peleador", "Conor McGregor", "Khabib Nurmagomedov", "Max Holloway", "Islam Makhachev", "Jiri Prochazka"])
    fighter2 = st.selectbox("Peleador 2", ["Selecciona un peleador", "Charles Oliveira", "Alexander Volkanovski", "Michael Chandler", "Dustin Poirier", "Yair Rodríguez"])

    # 4. Generar el enfrentamiento (solo si ambos peleadores han sido seleccionados)
    if fighter1 != "Selecciona un peleador" and fighter2 != "Selecciona un peleador":
        st.session_state.fighter1 = fighter1
        st.session_state.fighter2 = fighter2
        st.write(f"¡Se ha generado el enfrentamiento entre {fighter1} y {fighter2}!")
        
        # 5. Contador regresivo
        countdown = st.empty()  # Espacio vacío para el contador
        for i in range(10, 0, -1):  # Contador regresivo de 10 segundos
            countdown.markdown(f"Contador regresivo: {i} segundos")
            time.sleep(1)
        countdown.markdown("¡La pelea está por comenzar!")

        # 6. Botón Para Predecir Ganador
        predict_button = st.button("¿Quién ganará? Predecir ganador")
        if predict_button:
            st.write("Predicción en progreso...") 
            # Aquí iría la lógica para predecir el ganador (modelo de ML)
        
            # 7. ¿Estás seguro de querer saber en qué round?
            confirmation = st.radio("¿Estás seguro de querer saber en qué round?", ["Selecciona una opción", "Sí", "No"])
            if confirmation == "Sí":
                st.write("Vamos a predecir en qué round terminará la pelea.")
                
                # 8. Predecir Round
                round_prediction_button = st.button("Predecir Round")
                if round_prediction_button:
                    st.write("Predicción del round en progreso...")
                    # Aquí iría la lógica para predecir el round (modelo de ML)

                # 9. No me hago responsable de tus actos
                st.write("**No me hago responsable de tus actos.**")

                # 10. Predecir minutos
                minute_prediction_button = st.button("Predecir minutos")
                if minute_prediction_button:
                    st.write("Predicción de minutos en progreso...")
                    # Aquí iría la lógica para predecir los minutos (modelo de ML)
            elif confirmation == "No":
                st.write("La predicción de round ha sido cancelada.")
            
# Extra: Combate de Topuria vs Holloway
st.subheader("Combate entre Topuria y Holloway")
st.write("¡El combate entre Topuria y Holloway está preparado! Estás a punto de ver su predicción.")

# Pestaña adicional para la documentación
if st.sidebar.button("Documentación"):
    st.sidebar.write("Aquí va la documentación sobre cómo funciona el modelo de predicción...")

# Pestaña para la gráfica
if st.sidebar.button("Gráfica de predicción"):
    st.sidebar.write("Aquí va la gráfica de cómo el modelo predice los resultados, mostrando las probabilidades de victoria.")
    # Aquí iría el código para generar y mostrar la gráfica (por ejemplo, con Matplotlib, Plotly, etc.)
    # Ejemplo de gráfico de barras
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    ax.bar(["Peleador 1", "Peleador 2"], [0.6, 0.4])  # Solo un ejemplo simple
    ax.set_title("Probabilidades de victoria")
    st.sidebar.pyplot(fig)

