import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Intenta identificar la columna relevante en el DataFrame
def identificar_columna(df):
    posibles_nombres = ['consumo', 'gasto', 'kwh', 'costo']  # Lista expandible
    for columna in df.columns:
        for nombre in posibles_nombres:
            if nombre in columna.lower():
                return columna
    return None

st.title('Análisis Avanzado de Consumo Eléctrico')

uploaded_file = st.file_uploader("Sube tu archivo de consumo eléctrico (CSV o Excel):", type=["csv", "xlsx"])
if uploaded_file is not None:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file)

    columna_consumo = identificar_columna(df)
    
    if columna_consumo:
        #.write(f"Se detectó la columna de consumo: {columna_consumo}")
        st.line_chart(df[columna_consumo])
    else:
        st.error("No se pudo detectar automáticamente una columna de consumo. Verifica tu archivo y asegúrate que exista una columna válida.")


if columna_consumo:
    df['Diferencia'] = df[columna_consumo].diff()
    st.line_chart(df['Diferencia'])
    # Agrega lógica adicional para interpretar estas diferencias como tendencias.
