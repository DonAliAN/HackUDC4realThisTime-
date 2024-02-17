import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Función para identificar la columna relevante en el DataFrame
def identificar_columna(df):
    posibles_nombres = ['consumo', 'gasto', 'kwh', 'costo']  # Lista expandible
    for columna in df.columns:
        for nombre in posibles_nombres:
            if nombre in columna.lower():
                return columna
    return None

# Título de la aplicación y estilos personalizados
st.title('Análisis Avanzado de Consumo Eléctrico')

st.markdown("""
<style>
.big-font {
    font-size:30px !important;
    font-weight: bold;
}
.red-text {
    color: #FF0000 !important;
    font-size:20px;
}
.custom-font {
    font-size:22px !important;
    font-weight: bold;
}
.custom-color {
    color: #2a9d8f !important;
    font-size:20px;
}
</style>
""", unsafe_allow_html=True)

# Subida de archivo
uploaded_file = st.file_uploader("Sube tu archivo de consumo eléctrico (CSV o Excel):", type=["csv", "xlsx"])
if uploaded_file is not None:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file)

    columna_consumo = identificar_columna(df)
    
    if columna_consumo:
        st.markdown(f"<div class='custom-color'>Se detectó la columna de consumo: `{columna_consumo}`</div>", unsafe_allow_html=True)  # Uso de Markdown para resaltar
        st.line_chart(df[columna_consumo])

        # Asegúrate de que este código se ejecute solo si columna_consumo está definido
        df['Diferencia'] = df[columna_consumo].diff()
        st.subheader("Tendencias de Consumo")
        st.line_chart(df['Diferencia'])
    else:
        st.error("No se pudo detectar automáticamente una columna de consumo. Verifica tu archivo y asegúrate que exista una columna válida.")
else:
    st.markdown("<div class='big-font'>Por favor, sube un archivo para comenzar el análisis.</div>", unsafe_allow_html=True)
