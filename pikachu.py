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
    # Carga y muestra el DataFrame
    df = pd.read_csv(uploaded_file)
    st.write("Vista previa de los datos cargados:")
    st.dataframe(df.head())

    # Realiza un análisis simple
    st.subheader("Análisis Básico")
    total_consumo = df['Consumo_KWh'].sum()
    promedio_consumo = df['Consumo_KWh'].mean()
    st.write(f"Consumo total: {total_consumo} KWh")
    st.write(f"Consumo promedio por registro: {promedio_consumo:.2f} KWh")

    # Visualización de datos
    st.subheader("Visualización del Consumo")
    st.line_chart(df['Consumo_KWh'])

    # Gráfico personalizado con Matplotlib
    fig, ax = plt.subplots()
    ax.plot(df.index, df['Consumo_KWh'], color='purple')
    ax.set_xlabel('Registro')
    ax.set_ylabel('Consumo KWh')
    ax.set_title('Consumo Eléctrico a lo Largo del Tiempo')
    st.pyplot(fig)
else:
    st.info("Por favor, sube un archivo CSV para comenzar el análisis.")

