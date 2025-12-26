import streamlit as st
import google.generativeai as genai
import pandas as pd
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Arquitecto de Realidad Personal", layout="wide")

# --- ESTILO CSS PERSONALIZADO ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #2e7d32; color: white; }
    .reportview-container .main .block-container{ padding-top: 2rem; }
    </style>
    """, unsafe_allow_html=True)

# --- CONFIGURACIÓN DE LA API ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except:
    st.error("Por favor, configura la variable GEMINI_API_KEY en los Secrets de Streamlit.")
    st.stop()

# --- MODELO Y PROMPT MAESTRO ---
PROMPT_MAESTRO = """
Actúa como un Arquitecto de Realidad y Mentor de Prosperidad Integral. Tu misión es ayudar al usuario a transformar bloqueos económicos y dolores espirituales mediante técnicas de PNL y planificación estratégica.
Utiliza tecnicas de metafisica de cony mendez para incremetar la prosperidad.
Si es necesario Responder segun dyer, utilizando ideas de el libro el cielo es el limite.

Metodología:
1. Análisis Profundo: Detecta 'Virus Mentales' (creencias limitantes).
2. Reprogramación: Diseña ejercicios de PNL (anclajes, reencuadre, visualización).
3. Ingeniería de Riqueza: Guía en creación de metas SMART y hábitos.
4. En casos de crisis economica evaluar si se puede utilizar la regla 50/30/20 y explicarla.

5. En casos de situaciones economicas estancadas sugerir y explayar temas de optimización (Reducción de gastos, innovación, redes sociales, etc.).
6: Mostrar distintas formas de atacar la necesidad que plantea el usuario, obtenidas de internet y describirlas y analizarlas.  

Reglas:
- No responder consultas sobre sexo, salud, alimentacion, ni nada que no tenga que ver con economia.
- Tono sabio y empoderador.
- Estructura: Validar emoción -> Analizar raíz -> Tarea de Poder.
- Si detectas palabras como 'difícil' o 'imposible', propón una alternativa lingüística.
"""

# Inicializamos el modelo
model = genai.GenerativeModel('gemini-2.0-flash', system_instruction=PROMPT_MAESTRO)

# --- INICIALIZACIÓN DE ESTADO ---
# Importante: chat_history para la UI y gemini_chat para la lógica del modelo
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "gemini_chat" not in st.session_state:
    # Iniciamos la sesión de chat con el modelo
    st.session_state.gemini_chat = model.start_chat(history=[])

if "dashboard_data" not in st.session_state:
    st.session_state.dashboard_data = {
        "Mentalidad (PNL)": 3,
        "Energía Vital": 3,
        "Estructura Financiera": 2,
        "Generación de Valor": 2
    }

# --- INTERFAZ DE USUARIO (SIDEBAR) ---
with st.sidebar:
    st.title("💎 Dashboard de Evolución")
    st.write("Seguimiento de tu Salto Cuántico")
    
    for key, value in st.session_state.dashboard_data.items():
        st.session_state.dashboard_data[key] = st.slider(key, 1, 10, value)
    
    if st.button("Exportar Progreso a CSV"):
        df = pd.DataFrame([st.session_state.dashboard_data])
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Descargar Archivo", csv, "progreso_prosperidad.csv", "text/csv")

# --- CUERPO PRINCIPAL ---
st.title("🧘 Arquitecto de Realidad Personal")
st.markdown("---")

# Mostrar historial de chat almacenado
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada del usuario
if prompt := st.chat_input("Cuéntame tu desafío económico o inquietud espiritual hoy..."):
    
    # 1. Mostrar y guardar mensaje del usuario
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Generar respuesta usando la sesión de chat activa
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            # Enviamos el mensaje a la sesión que ya tiene el historial
            response = st.session_state.gemini_chat.send_message(prompt, stream=True)
            
            full_response = ""
            for chunk in response:
                full_response += chunk.text
                message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            
            # 3. Guardar respuesta del asistente en el historial de la UI
            st.session_state.chat_history.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Ocurrió un error: {e}")

# --- PIE DE PÁGINA ÉTICO ---
st.markdown("---")
st.caption("⚠️ **Descargo de responsabilidad:** Este sistema es una herramienta de apoyo emocional y estratégico basado en IA. No sustituye la terapia psicológica profesional ni el asesoramiento financiero legal.")