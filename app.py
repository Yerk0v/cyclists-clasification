import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from model_prediction import predict_capacities
from input_data import user_input

# Configuración de la página
st.set_page_config(page_title="Predicción de Ciclistas", page_icon="🚴", layout="centered")

# Título de la aplicación
st.title("🚴 Predicción de Ciclistas con XGBoost")

# Información en la barra lateral
with st.sidebar:
    st.header("Requisitos de los datos")
    st.caption("Para predecir, sube un archivo CSV con las siguientes características:")
    with st.expander("Formato de los datos"):
        st.markdown("""
        - Codificación: UTF-8
        - Separado por comas
        - Delimitado por comillas dobles
        - La primera fila debe ser el encabezado
        - Características necesarias: 'age', 'gender', 'activities', 'weightkg', 'frecuencia_semanal', 'workout_time', 'total_distance', 'elevation_gain', 'average_speed', 'average_power', 'average_hr'
        """)
    st.divider()
    st.caption("<p style='text-align:center'>Desarrollado por Yerko Muñoz</p>", unsafe_allow_html=True)

# Estado del botón
if 'clicked' not in st.session_state:
    st.session_state.clicked = {1: False}
if 'show_data' not in st.session_state:
    st.session_state.show_data = False

def clicked(button):
    st.session_state.clicked[button] = True

def toggle_data_view():
    st.session_state.show_data = not st.session_state.show_data

st.button("Comencemos", on_click=clicked, args=[1])

# Subida de archivos y predicción
if st.session_state.clicked[1]:
    uploaded_file = st.file_uploader("Sube tu archivo CSV", type="csv")

    if uploaded_file is not None:
        # Cargar datos
        df = pd.read_csv(uploaded_file)

        # Mostrar datos subidos opcionalmente
        if st.button("Mostrar/Ocultar datos subidos"):
            toggle_data_view()

        if st.session_state.show_data:
            st.header("Muestra de datos subidos")
            st.write(df.head())

        # Procesar datos y hacer predicciones
        data = df.to_dict(orient='records')
        if data:
            predictions = []
            for record in data:
                predicted_aerobic, predicted_anaerobic = predict_capacities(record)
                # Mapear las predicciones a las categorías equivalentes
                record['predicted_aerobic'] = ['Casual', 'Principiante', 'Experimentado', 'Élite'][predicted_aerobic]
                record['predicted_anaerobic'] = ['Casual', 'Principiante', 'Experimentado', 'Élite'][predicted_anaerobic]
                predictions.append(record)
            predictions_df = pd.DataFrame(predictions)
            st.header("Predicciones")
            st.write(predictions_df)

            # Gráfico de distribución por categoría aeróbica
            st.header("Distribución por Categoría Aeróbica")
            category_aerobic_counts = predictions_df['predicted_aerobic'].value_counts()
            fig, ax = plt.subplots()
            sns.barplot(x=category_aerobic_counts.index, y=category_aerobic_counts.values, palette='viridis', ax=ax)
            ax.set_title('Número de Ciclistas por Categoría Aeróbica')
            ax.set_xlabel('Categoría Aeróbica')
            ax.set_ylabel('Número de Ciclistas')
            for i, count in enumerate(category_aerobic_counts.values):
                ax.text(i, count + 2, str(count), ha='center')
            st.pyplot(fig)

            # Gráfico de distribución por categoría anaeróbica
            st.header("Distribución por Categoría Anaeróbica")
            category_anaerobic_counts = predictions_df['predicted_anaerobic'].value_counts()
            fig, ax = plt.subplots()
            sns.barplot(x=category_anaerobic_counts.index, y=category_anaerobic_counts.values, palette='magma', ax=ax)
            ax.set_title('Número de Ciclistas por Categoría Anaeróbica')
            ax.set_xlabel('Categoría Anaeróbica')
            ax.set_ylabel('Número de Ciclistas')
            for i, count in enumerate(category_anaerobic_counts.values):
                ax.text(i, count + 2, str(count), ha='center')
            st.pyplot(fig)

            # Gráfico de distribución de edad
            st.header("Distribución de Edad")
            fig, ax = plt.subplots()
            sns.histplot(predictions_df['age'], bins=20, kde=True, palette='viridis', ax=ax)
            ax.set_title('Distribución de Edad de los Ciclistas')
            ax.set_xlabel('Edad')
            ax.set_ylabel('Frecuencia')
            st.pyplot(fig)

            # Gráfico de rendimiento en relación al average_power (boxplot) por categoría aeróbica
            st.header("Rendimiento en Relación al Average Power por Categoría Aeróbica")
            fig, ax = plt.subplots()
            sns.boxplot(x='predicted_aerobic', y='average_power', data=predictions_df, palette='viridis', ax=ax)
            ax.set_title('Distribución del Average Power por Categoría Aeróbica')
            ax.set_xlabel('Categoría Aeróbica')
            ax.set_ylabel('Average Power')
            st.pyplot(fig)

            # Gráfico de rendimiento en relación al average_power (boxplot) por categoría anaeróbica
            st.header("Rendimiento en Relación al Average Power por Categoría Anaeróbica")
            fig, ax = plt.subplots()
            sns.boxplot(x='predicted_anaerobic', y='average_power', data=predictions_df, palette='magma', ax=ax)
            ax.set_title('Distribución del Average Power por Categoría Anaeróbica')
            ax.set_xlabel('Categoría Anaeróbica')
            ax.set_ylabel('Average Power')
            st.pyplot(fig)

        else:
            st.error("El archivo CSV no contiene datos válidos.")

    else:
        # Volver al formulario de entrada si no hay archivo cargado
        st.header("Ingrese sus datos")
        user_data = user_input()

        # Predicciones
        if st.button("Predecir"):
            predicted_aerobic, predicted_anaerobic = predict_capacities(user_data)
            # Mapear las predicciones a las categorías equivalentes
            category_aerobic = ['Casual', 'Principiante', 'Experimentado', 'Élite'][predicted_aerobic]
            category_anaerobic = ['Casual', 'Principiante', 'Experimentado', 'Élite'][predicted_anaerobic]
            st.write(f"Tu estimación aeróbica es: {category_aerobic}")
            st.write(f"Tu estimación anaeróbica es: {category_anaerobic}")
