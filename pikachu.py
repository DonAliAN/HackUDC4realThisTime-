import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configuración inicial de la página
st.set_page_config(page_title="ElectroDatos - Análisis de Consumo Eléctrico", layout="wide")

# Título
st.title('ElectroDatos: Análisis de tu Consumo Eléctrico')

# Subida de archivo
uploaded_file = st.file_uploader("Sube tu archivo CSV de consumo eléctrico aquí:", type="csv")
if uploaded_file is not None:
    # Carga el archivo CSV
    df = pd.read_csv(uploaded_file)
    
    # Verifica si la columna esperada existe en el DataFrame
    if 'Consumo_KWh' in df.columns:
        # Realiza el análisis si la columna existe
        st.write("Vista previa de los datos cargados:")
        st.dataframe(df.head())

        # Análisis y visualización aquí
        total_consumo = df['Consumo_KWh'].sum()
        st.write(f"Consumo total: {total_consumo} KWh")

        # Más análisis y visualizaciones...
    else:
        # Si la columna no se encuentra, muestra un mensaje de error
        st.error("La columna 'Consumo_KWh' no se encuentra en el archivo. Por favor verifica el nombre de la columna.")
