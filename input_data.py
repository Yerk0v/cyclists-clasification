import streamlit as st

def user_input():
    age = st.number_input("Edad", min_value=0, max_value=120, step=1, key="age_input")
    gender = st.selectbox("Género", ["Masculino", "Femenino"], key="gender_selectbox")
    activities = st.number_input("Cantidad total de actividades en los últimos 2 años", min_value=0.0, step=1.0, key="total_activities_input")
    weightkg = st.number_input("Tu peso (en KG)", min_value=0, step=1, key="weightkg_ciclista_input")
    frecuencia_semanal = st.number_input("Frecuencia semanal (sesiones por semana)", min_value=0.0, step=1.0, key="frecuencia_semanal_input")
    workout_time = st.number_input("Duración del entrenamiento (minutos)", min_value=0.0, step=1.0, key="workout_time_input")
    total_distance = st.number_input("Distancia total (kilómetros)", min_value=0.0, step=1.0, key="total_distance_input")
    elevation_gain = st.number_input("Ganancia de elevación (metros)", min_value=0.0, step=1.0, key="elevation_gain_input")
    average_speed = st.number_input("Velocidad promedio (km/h)", min_value=0.0, step=1.0, key="average_speed_input")
    average_power = st.number_input("Potencia promedio en todas las actividades", min_value=0.0, step=1.0, key="average_power_total_input")
    average_hr = st.number_input("Frecuencia cardíaca promedio (BPM)", min_value=0.0, step=1.0, key="average_hr_input")

    # Convertir género a binario
    gender_binary = 1 if gender == "Masculino" else 0

    # Almacenar los datos ingresados en un diccionario en el orden correcto
    data = {
        'age': age,
        'gender': gender_binary,
        'activities': activities,
        'weightkg': weightkg,
        'frecuencia_semanal': frecuencia_semanal,
        'workout_time': workout_time,
        'total_distance': total_distance,
        'elevation_gain': elevation_gain,
        'average_speed': average_speed,
        'average_power': average_power,
        'average_hr': average_hr,
    }

    return data
