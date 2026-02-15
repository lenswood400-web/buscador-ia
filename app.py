import streamlit as st
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_groq import ChatGroq
import os

# --- DISEÑO NIVEL PRO ---
st.set_page_config(page_title="Seeke AI Clone", page_icon="🚀", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    .stTextInput input { border-radius: 10px; background-color: #161b22; color: white; border: 1px solid #30363d; }
    .answer-box { background-color: #161b22; padding: 20px; border-radius: 15px; border: 1px solid #30363d; line-height: 1.6; }
    </style>
    """, unsafe_allow_html=True)

# --- SEGURIDAD ---
if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
else:
    # SI PRUEBAS EN TU PC, PEGA TU LLAVE AQUÍ ABAJO:
    os.environ["GROQ_API_KEY"] = "TU_LLAVE_DE_GROQ_AQUI"

st.title("🚀 Seeke AI Clone")
st.caption("Buscador inteligente gratuito | Creado por un futuro Ingeniero")

pregunta = st.text_input("", placeholder="¿Qué quieres saber hoy?")

if pregunta:
    with st.spinner("🧠 Buscando en la web y procesando con IA..."):
        try:
            # 1. Buscamos info (Usamos el objeto directamente para evitar el error de importación)
            buscador = DuckDuckGoSearchRun()
            datos_web = buscador.run(pregunta)
            
            # 2. Conectamos con la IA
            ia = ChatGroq(model_name="llama3-8b-8192", temperature=0.2)
            
            instrucciones = f"""
            Eres un buscador experto. Responde a: '{pregunta}' 
            Usa esta información real: {datos_web}
            
            Responde con:
            - Un resumen potente.
            - 3 puntos clave.
            - Una conclusión.
            """
            
            resultado = ia.invoke(instrucciones)
            
            # 3. Mostramos la respuesta
            st.markdown("### 📝 Respuesta de la IA")
            st.markdown(f'<div class="answer-box">{resultado.content}</div>', unsafe_allow_html=True)
            
            with st.expander("🌐 Ver fuentes"):
                st.write(datos_web)
                
        except Exception as e:
            st.error(f"¡Casi lo tenemos! Hubo un detalle: {e}")
            st.info("Tip: Asegúrate de que tu llave de Groq esté bien puesta en los 'Secrets' de Streamlit.")

st.markdown("---")
st.markdown("💡 *El código es persistencia. ¡Sigue adelante!*")
