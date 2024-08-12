from sklearn.preprocessing import StandardScaler
import joblib
import pandas as pd

# Cargar los modelos
model_aerobico = joblib.load('model_aerobico.joblib')
model_anaerobico = joblib.load('model_anaerobico.joblib')

# Cargar el scaler utilizado durante el entrenamiento
scaler_aerobico = joblib.load('scaler_aerobico.joblib')
scaler_anaerobico = joblib.load('scaler_anaerobico.joblib')

def predict_capacities(data):
    data_df = pd.DataFrame([data])

    # Escalar características
    data_scaled = scaler_aerobico.transform(data_df)  # Cambia esto si el scaler es específico para cada modelo

    predicted_aerobic = model_aerobico.predict(data_scaled)[0]
    predicted_anaerobic = model_anaerobico.predict(data_scaled)[0]
    
    return predicted_aerobic, predicted_anaerobic

