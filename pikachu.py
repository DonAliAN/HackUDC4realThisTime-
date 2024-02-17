import streamlit as st 
import pandas as pd
from streamlit_echarts import st_echarts

# Define los umbrales de consumo para las recomendaciones
umbral_alto_consumo = 350 
umbral_moderado_consumo = 225  

st.title('🌱 Análisis Avanzado de Consumo Eléctrico')

def identificar_columna_consumo(df, posibles_nombres):
    for nombre in posibles_nombres:
        if nombre.lower() in df.columns.str.lower().tolist():
            return df.columns[df.columns.str.lower() == nombre.lower()][0]
    return None

uploaded_file = st.file_uploader("Sube tu archivo de consumo eléctrico (CSV o Excel):", type=["csv", "xlsx"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    posibles_nombres_consumo = ['consumo', 'gasto', 'kwh', 'costo']
    columna_consumo = identificar_columna_consumo(df, posibles_nombres_consumo)
    
    if columna_consumo:
        df[columna_consumo] = pd.to_numeric(df[columna_consumo], errors='coerce')
        
        # Gráfica de consumo eléctrico
        options_consumo = {
            "xAxis": {"type": "category", "data": df.index.tolist(), "name": "Registro"},
            "yAxis": {"type": "value", "name": "Consumo (kWh)"},
            "tooltip": {"trigger": "axis", "formatter": "{b0}: {c0} kWh"},
            "series": [{"data": df[columna_consumo].tolist(), "type": "line", "showSymbol": False}],
        }
        st_echarts(options=options_consumo, height="400px")

        if 'Hora' in df.columns:
            df['Hora'] = pd.to_numeric(df['Hora'], errors='coerce').fillna(0).astype(int)
            consumo_por_hora = df.groupby('Hora')[columna_consumo].sum().reset_index()
            
            # Gráfica de consumo por hora
            options_hora = {
                "xAxis": {"type": "category", "data": consumo_por_hora['Hora'].tolist(), "name": "Hora del día"},
                "yAxis": {"type": "value", "name": "Consumo (kWh)"},
                "tooltip": {"trigger": "axis", "formatter": "Hora {b0}: {c0} kWh"},
                "series": [{"data": consumo_por_hora[columna_consumo].tolist(), "type": "bar"}],
            }
            st_echarts(options=options_hora, height="400px")

        # Recomendaciones 
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
            st.markdown("Tu consumo de energía es relativamente bajo. ¡Bien!")

    else:
        st.error("No se pudo detectar automáticamente una columna de consumo. Verifica tu archivo y asegúrate que tenga una columna que contenga la .")
else:
    st.markdown("## Por favor, sube un archivo para comenzar el análisis.", unsafe_allow_html=True)
