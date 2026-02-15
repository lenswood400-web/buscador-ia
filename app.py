import streamlit as st
from langchain_groq import ChatGroq
import os

# --- CONFIGURACIÓN DE ÉLITE ---
st.set_page_config(page_title="Lens AI", page_icon="⚪", layout="centered")

# --- INTERFAZ NIVEL DIOS (CSS AVANZADO) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com');
    
    .stApp {
        background: radial-gradient(circle at top right, #ffffff 0%, #f0f0f5 100%);
        color: #1d1d1f;
    }

    /* Burbujas con Animación de Entrada */
    @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

    .user-bubble {
        background: linear-gradient(135deg, #007aff 0%, #0056b3 100%);
        color: white; padding: 14px 20px; border-radius: 22px 22px 4px 22px;
        margin-bottom: 1rem; float: right; clear: both; max-width: 80%;
        box-shadow: 0 4px 15px rgba(0, 122, 255, 0.2);
        animation: fadeIn 0.3s ease-out;
    }

    .lens-bubble {
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.4);
        padding: 20px; border-radius: 22px 22px 22px 4px;
        margin-bottom: 1.5rem; float: left; clear: both; max-width: 85%;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.05);
        animation: fadeIn 0.4s ease-out;
    }

    /* Panel de Configuración Lateral */
    .stSidebar { background-color: rgba(255, 255, 255, 0.4) !important; backdrop-filter: blur(10px); }
    
    .creator-header {
        text-align: center; font-size: 10px; letter-spacing: 3px;
        color: #86868b; text-transform: uppercase; font-weight: 700;
        margin-top: -50px; margin-bottom: 20px;
    }

    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- SEGURIDAD ---
if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
else:
    os.environ["GROQ_API_KEY"] = "TU_LLAVE"

# --- PANEL DE CONFIGURACIÓN (CENTRO DE CONTROL) ---
with st.sidebar:
    st.markdown("### ⚙️ Centro de Control")
    st.markdown("---")
    personalidad = st.select_slider(
        "Tono de Lens:",
        options=["Muy Serio", "Profesional", "Colega/Bro"],
        value="Profesional"
    )
    modo_seguro = st.toggle("Protocolo de Seguridad Activo", value=True)
    if st.button("Limpiar Memoria de Lens"):
        st.session_state.messages = []
        st.rerun()
    st.write("---")
    st.caption(f"Hardware: Llama 3.3 70B\nDeveloper: Lens Wood Patrice")

# --- LÓGICA DE MENSAJES ---
if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown("<div class='creator-header'>Lens Wood Patrice Studio</div>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; font-weight: 600;'>Lens</h1>", unsafe_allow_html=True)

for m in st.session_state.messages:
    div = "user-bubble" if m["role"] == "user" else "lens-bubble"
    st.markdown(f'<div class="{div}">{m["content"]}</div>', unsafe_allow_html=True)

# --- RESPUESTA DE LENS ---
if prompt := st.chat_input("¿En qué piensas?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.spinner(""):
        try:
            llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0.5)
            
            # Adaptamos el prompt según la configuración del slider
            extra_inst = "Habla de forma muy técnica y seria." if personalidad == "Muy Serio" else \
                         "Habla como un colega cercano, usando 'bro' y siendo divertido." if personalidad == "Colega/Bro" else \
                         "Sé equilibrado, profesional y educado."

            sys_prompt = f"""
            Eres Lens, una IA de nivel Dios creada por Lens Wood Patrice. 
            {extra_inst}
            Seguridad activa: {modo_seguro}. Si es True, no hagas nada ilegal.
            Creador: Lens Wood Patrice es tu único desarrollador.
            """
            
            msgs = [{"role": "system", "content": sys_prompt}]
            for m in st.session_state.messages[-6:]:
                msgs.append({"role": m["role"], "content": m["content"]})
            
            response = llm.invoke(msgs)
            st.session_state.messages.append({"role": "assistant", "content": response.content})
            st.rerun()
        except Exception as e:
            st.error(f"Error en los núcleos de Lens. ({e})")
