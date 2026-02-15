import streamlit as st
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_groq import ChatGroq
import os

# --- CONFIGURACIÓN DE ESTILO ---
st.set_page_config(page_title="AI Search Engine", page_icon="⚡", layout="wide")

# CSS para que parezca una App de Silicon Valley
st.markdown("""
    <style>
    .stApp { background: #0e1117; color: #e0e0e0; }
    .stTextInput input {
        border-radius: 15px;
        border: 1px solid #30363d;
        padding: 15px;
        background-color: #161b22 !important;
        color: white !important;
    }
    .answer-card {
        background-color: #1c2128;
        padding: 25px;
        border-radius: 15px;
        border-left: 5px solid #238636;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LLAVE DE SEGURIDAD ---
if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
else:
    # Si pruebas en tu PC, pon tu clave aquí entre las comillas
    os.environ["GROQ_API_KEY"] = "TU_LLAVE_DE_GROQ_AQUI"

# --- INTERFAZ ---
with st.sidebar:
    st.title("🚀 Settings")
    st.info("Buscador con IA en tiempo real. No guarda tus datos.")
    st.markdown("---")
    st.write("Versión: 1.0 (Beta)")

st.title("⚡ Seeke AI Clone")
st.subheader("El futuro de las búsquedas, hoy.")

query = st.text_input("", placeholder="¿Qué quieres descubrir hoy?")

if query:
    with st.spinner("🔍 Rastreando la web y generando respuesta..."):
        try:
            # 1. Buscador mejorado
            search = DuckDuckGoSearchRun()
            search_results = search.run(query)
            
            # 2. IA Profesional (Llama 3)
            llm = ChatGroq(model_name="llama3-8b-8192", temperature=0.3)
            
            prompt = f"""
            Actúa como un motor de búsqueda inteligente. 
            PREGUNTA: {query}
            INFORMACIÓN WEB: {search_results}
            
            Estructura tu respuesta así:
            1. Un resumen directo y claro.
            2. Puntos clave en viñetas.
            3. Una conclusión corta.
            Usa un tono profesional.
            """
            
            response = llm.invoke(prompt)
            
            # 3. Mostrar la respuesta con estilo
            st.markdown(f'<div class="answer-card">', unsafe_allow_html=True)
            st.markdown("### 📝 Análisis Inteligente")
            st.write(response.content)
            st.markdown('</div>', unsafe_allow_html=True)
            
            with st.expander("🌐 Ver fuentes consultadas"):
                st.write(search_results)
                
        except Exception as e:
            st.error(f"❌ Error de conexión. Detalles: {e}")

# Pie de página
st.markdown("---")
st.caption("Creado con ❤️ por un futuro desarrollador.")
