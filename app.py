import streamlit as st
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_groq import ChatGroq
import os

# --- INTERFAZ PROFESIONAL ---
st.set_page_config(page_title="Seeke AI Clone", page_icon="🔍", layout="wide")

# Estilo visual tipo aplicación moderna
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: white; }
    .stTextInput input { border-radius: 20px; border: 1px solid #30363d; background-color: #161b22; color: white; }
    .stButton button { border-radius: 20px; background-color: #238636; color: white; border: none; }
    </style>
    """, unsafe_allow_html=True)

st.title("🔍 Mi Buscador IA Inteligente")
st.write("Escribe tu duda y buscaré en toda la web para darte una respuesta real.")

# --- LÓGICA DE LA IA ---
# Aquí usamos st.secrets para que sea seguro en la web
if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
else:
    # Para probar en tu PC antes de subirlo, puedes poner tu llave aquí temporalmente:
    os.environ["GROQ_API_KEY"] = "TU_LLAVE_DE_GROQ_AQUI"

query = st.text_input("", placeholder="¿Qué quieres investigar?")

if query:
    with st.spinner("Analizando la web en tiempo real..."):
        try:
            # Busca en Google/DuckDuckGo
            search = DuckDuckGoSearchRun()
            contexto = search.run(query)
            
            # Procesa con la IA (Llama 3 es gratis y rápida)
            llm = ChatGroq(model_name="llama3-8b-8192")
            prompt = f"Eres un buscador tipo Perplexity o Seeke. Basándote en este contexto: {contexto}, responde a: {query}. Usa un tono profesional y directo."
            
            respuesta = llm.invoke(prompt)
            
            # Muestra el resultado de forma elegante
            st.markdown("### 💡 Respuesta")
            st.info(respuesta.content)
            
            with st.expander("Ver fuentes de información"):
                st.write(contexto)
                
        except Exception as e:
            st.error(f"Ocurrió un error. Revisa tu API Key. Detalle: {e}")
