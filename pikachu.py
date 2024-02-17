import streamlit as st 
import pandas as pd
from streamlit_echarts import st_echarts
import streamlit as st
from streamlit_echarts import st_echarts
#from ChatBot import generar_respuesta
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

if 'conversation' not in st.session_state:
    st.session_state['conversation'] = []

def display_chatbot():
    st.title("Chatbot")
    # Usa un valor por defecto vacío para 'chat_input' para evitar errores en la primera ejecución
    user_input = st.text_input("Escribe tu mensaje aquí:", key="chat_input", value="")

    send_button = st.button("Enviar")
    if send_button and user_input:
        # Procesa el mensaje del usuario y obtiene una respuesta del chatbot
        user_message = user_input.strip()
        chatbot_response = generar_respuesta(user_message)

        # Añade los mensajes a la conversación
        st.session_state['conversation'].append(f"Tú: {user_message}")
        st.session_state['conversation'].append(f"Chatbot: {chatbot_response}")

        # Opcional: Limpia el input del usuario para facilitar una nueva entrada
        #st.session_state.chat_input = ""

    # Muestra la conversación acumulada
    st.write("Conversación:")
    for message in st.session_state['conversation']:
        st.text(message)


# Cargar datos desde el archivo Excel de entrenamiento
datos_entrenamiento = pd.read_excel('datos_entrenamiento.xlsx')

# Obtener las frases de entrenamiento y las etiquetas de entrenamiento
frases_entrenamiento = datos_entrenamiento['Frase'].tolist()
etiquetas_entrenamiento = datos_entrenamiento['Etiqueta'].tolist()

# Crear un clasificador de texto usando el algoritmo Naive Bayes
modelo = make_pipeline(CountVectorizer(), MultinomialNB())

# Entrenar el modelo con las frases de entrenamiento y sus etiquetas
modelo.fit(frases_entrenamiento, etiquetas_entrenamiento)

# Cargar datos desde el archivo Excel de etiquetas a funciones
etiquetas_funciones = pd.read_excel('etiquetas_funciones.xlsx', index_col=0)
etiquetas_funciones_dict = etiquetas_funciones['Funcion'].to_dict()

def generar_respuesta(frase_usuario):
    # Clasificar la frase del usuario
    etiqueta_predicha = modelo.predict([frase_usuario])[0]

    # Buscar la función (en este caso, respuesta) asociada a la etiqueta predicha
    respuesta_asociada = etiquetas_funciones_dict.get(etiqueta_predicha,
                                                      "No se encontró una función asociada a la etiqueta predicha.")
    respuesta = eval(respuesta_asociada)
    return respuesta

# Define los umbrales de consumo para las recomendaciones
umbral_alto_consumo = 350 
umbral_moderado_consumo = 225

def identificar_columna(df, posibles_nombres):
    for columna in df.columns:
        for nombre in posibles_nombres:
            if nombre in columna.lower():
                return columna
    return None
def analizar_consumo_medio_por_hora(datos):
    datos['datetime'] = pd.to_datetime(datos['datetime'])
    datos.set_index('datetime', inplace=True)

    # Ahora, puedes agrupar por hora y calcular el consumo medio
    consumo_medio_por_hora = datos.groupby(datos.index.hour)['Consumo'].mean()

    return consumo_medio_por_hora
def analizar_consumo_medio_por_dia(datos):
    """
    Devuelve el consumo medio por día de la semana.

    Parámetros:
    - datos: DataFrame de pandas con un índice DateTimeIndex.

    Retorna:
    - Un objeto Series de pandas con el consumo medio por día de la semana.
    """
    # No es necesario ajustar el DataFrame aquí, ya que se asume que 'datos'
    # tiene un índice DateTimeIndex debido al proceso de carga y preparación de los datos.
    consumo_medio_por_dia = datos.groupby(datos.index.dayofweek)['Consumo'].mean()

    return consumo_medio_por_dia
def generar_recomendaciones(horas_mayor_consumo, dia_mayor_consumo):
    """Devuelve recomendaciones basadas en el análisis de consumo."""
    recomendaciones = {
        'horas_pico': horas_mayor_consumo,
        'dia_mayor_consumo': ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'][dia_mayor_consumo]
    }
    return recomendaciones

st.title('🌱 Análisis Avanzado de Consumo Eléctrico')

def identificar_columna_consumo(df, posibles_nombres):
    for nombre in posibles_nombres:
        if nombre.lower() in df.columns.str.lower().tolist():
            return df.columns[df.columns.str.lower() == nombre.lower()][0]
    return None

uploaded_file = st.file_uploader("Sube tu archivo de consumo eléctrico (CSV o Excel):", type=["csv", "xlsx"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    datos = df

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
    display_chatbot()

else:
    st.markdown("## Por favor, sube un archivo para comenzar el análisis.", unsafe_allow_html=True)
