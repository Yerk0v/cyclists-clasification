import streamlit as st
import pandas as pd
from joblib import load
from sklearn.preprocessing import StandardScaler
import plotly.express as px

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
        - Características necesarias: 'age', 'gender', 'activities', 'bike', '20s_peak', '60s_peak', '180s_peak', '420s_peak', '720s_peak', 'weightkg'
        """)
    st.divider()
    st.caption("<p style='text-align:center'>Desarrollado por Yerko Muñoz</p>", unsafe_allow_html=True)

# Estado del botón
if 'clicked' not in st.session_state:
    st.session_state.clicked = {1: False}

def clicked(button):
    st.session_state.clicked[button] = True

st.button("Comencemos", on_click=clicked, args=[1])

# Subida de archivos y predicción
if st.session_state.clicked[1]:
    uploaded_file = st.file_uploader("Sube tu archivo CSV", type="csv")

    if uploaded_file is not None:
        # Cargar datos
        df = pd.read_csv(uploaded_file)

        st.header("Muestra de datos subidos")
        st.write(df.head())

        # Categorizar la variable objetivo
        def categorize_wpk(wpk):
            if wpk < 4.0:
                return 0
            elif 4.0 <= wpk <= 5.0:
                return 1
            elif 5.0 <= wpk <= 6.0:
                return 2
            else:
                return 3

        df['performance_metric'] = df['240s_peak_wpk'].apply(categorize_wpk)

        # Selección de características y escalamiento
        features = ['age', 'gender', 'activities', 'bike', '20s_peak', '60s_peak', '180s_peak', '420s_peak', '720s_peak', 'weightkg']
        X = df[features]
        
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Cargar el modelo y predecir
        model = load('model.joblib')
        predictions = model.predict(X_scaled)
        
        # Añadir las predicciones al DataFrame
        df['Predicción'] = predictions

        st.header("Resultados de las Predicciones")
        st.write(df.head())

        pred_csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Descargar predicciones", pred_csv, "predicciones.csv", "text/csv")

        # Información de categorías
        with st.expander("Ver información de categorías"):
            st.write("""
            **0**: Casual
            **1**: Amateur
            **2**: Experimentado
            **3**: Profesional
            """)

        # Agregar un botón para ver estadísticas
        if st.button("Ver estadísticas"):
            st.header("Estadísticas de las Predicciones")
            
            # Ejemplo de gráfico de barras con Plotly
            fig = px.histogram(df, x='Predicción', title='Distribución de Predicciones')
            st.plotly_chart(fig)
            
            # Más visualizaciones o estadísticas
            st.write("Estadísticas descriptivas:")
            st.write(df.describe())


