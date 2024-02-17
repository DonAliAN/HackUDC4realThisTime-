import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Define los umbrales de consumo para las recomendaciones
umbral_alto_consumo = 100  # Ajusta este valor según tus necesidades
umbral_moderado_consumo = 50  # Ajusta este valor según tus necesidades

# Función para identificar la columna relevante en el DataFrame
def identificar_columna(df, posibles_nombres):
    for columna in df.columns:
        for nombre in posibles_nombres:
            if nombre in columna.lower():
                return columna
    return None

# Aplicando mejoras visuales con Markdown para el fondo y estilo de botones
st.markdown("""
<style>
body {
    background-color: #FFF5E4;
}
.stButton>button {
    border: 2px solid #4CAF50;
    border-radius: 5px;
    color: #FFFFFF;
    background-color: #4CAF50;
}
.streamlit-container {
    background: linear-gradient(to right, #faaca8, #ddd6f3);
}
</style>
""", unsafe_allow_html=True)

st.title('🌱 Análisis Avanzado de Consumo Eléctrico')

uploaded_file = st.file_uploader("Sube tu archivo de consumo eléctrico (CSV o Excel):", type=["csv", "xlsx"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    posibles_nombres_consumo = ['consumo', 'gasto', 'kwh', 'costo']
    columna_consumo = identificar_columna(df, posibles_nombres_consumo)
    
    if columna_consumo:
        df[columna_consumo] = pd.to_numeric(df[columna_consumo], errors='coerce')
        
        # Graficando el consumo eléctrico
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(df.index, df[columna_consumo], color='skyblue', linestyle='-', marker='o', linewidth=2, markersize=4)
        ax.set_title('Consumo Eléctrico a lo Largo del Tiempo')
        ax.set_xlabel('Registro')
        ax.set_ylabel('Consumo')
        ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        st.pyplot(fig)

        # Graficando el consumo por hora si la columna 'Hora' existe
        if 'Hora' in df.columns:
            df['Hora'] = pd.to_numeric(df['Hora'], errors='coerce').fillna(0).astype(int)
            consumo_por_hora = df.groupby('Hora')[columna_consumo].mean()
            fig, ax = plt.subplots(figsize=(10, 5))
            consumo_por_hora.plot(kind='bar', ax=ax, color='lightgreen')
            ax.set_title('Promedio de Consumo Eléctrico por Hora')
            ax.set_xlabel('Hora del Día')
            ax.set_ylabel('Consumo Promedio')
            ax.set_xticklabels(consumo_por_hora.index, rotation=45)
            st.pyplot(fig)
        
        # Recomendaciones Personalizadas para Ahorrar Energía
        st.subheader("💡 Consejos Personalizados para Ahorrar Energía")
        consumo_promedio = df[columna_consumo].mean()
        if consumo_promedio > umbral_alto_consumo:
            st.markdown("""
            - **Considera instalar paneles solares** para reducir tu dependencia de la red eléctrica.
            - **Revisa tus electrodomésticos más antiguos**; podrían estar consumiendo más energía de la necesaria.
            """)
        elif consumo_promedio > umbral_moderado_consumo:
            st.markdown("""
            - **Mejora el aislamiento de tu hogar** para mantener una temperatura agradable sin sobreusar calefacción o aire acondicionado.
            - **Utiliza regletas inteligentes** para apagar completamente los dispositivos que no estén en uso.
            """)
        else:
            st.markdown("Tu consumo de energía es relativamente bajo. ¡Excelente trabajo manteniéndolo así!")
    else:
        st.error("No se pudo detectar automáticamente una columna de consumo. Verifica tu archivo.")
else:
    st.markdown("## Por favor, sube un archivo para comenzar el análisis.", unsafe_allow_html=True)
