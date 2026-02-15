import streamlit as st
from langchain_groq import ChatGroq
import os

# --- CONFIGURACIÓN DE ÉLITE ---
st.set_page_config(page_title="Lens AI", page_icon="⚪", layout="centered")

# --- CSS & JS: NIVEL DIOS SUPREMO ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com');
    
    .stApp {
        background: #FFFFFF;
        color: #1d1d1f;
    }

    /* Contenedor de Chat con Scroll Suave */
    .chat-container {
        padding-bottom: 100px;
    }

    .user-bubble {
        background: #007aff;
        color: white; padding: 14px 20px; border-radius: 22px 22px 4px 22px;
        margin-bottom: 1rem; float: right; clear: both; max-width: 80%;
        box-shadow: 0 4px 15px rgba(0, 122, 255, 0.15);
        font-size: 15px;
    }

    .lens-bubble {
        background: #f5f5f7;
        border: 1px solid #e5e5e7;
        padding: 20px; border-radius: 22px 22px 22px 4px;
        margin-bottom: 1.5rem; float: left; clear: both; max-width: 85%;
        font-size: 15px; line-height: 1.6;
    }

    /* Animación sutil de Lens al escribir */
    .lens-loading {
        color: #86868b;
        font-size: 12px;
        margin-left: 10px;
    }

    .creator-header {
        text-align: center; font-size: 10px; letter-spacing: 3px;
        color: #86868b; text-transform: uppercase; font-weight: 700;
        margin-bottom: 40px;
    }

    /* Fix para el Input Flotante estilo Apple */
    .stChatInputContainer {
        background-color: rgba(255,255,255,0.8) !important;
        backdrop-filter: blur(20px);
        border-top: 1px solid #e5e5e7;
    }

    #MainMenu, footer, header {visibility: hidden;}
    </style>

    <script>
    // Script para mantener el foco donde debe estar
    var observer = new MutationObserver(function(mutations) {
        window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
    });
    observer.observe(document.body, {childList: true, subtree: true});
    </script>
    """, unsafe_allow_html=True)

# --- SEGURIDAD ---
if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

# --- PANEL DE CONTROL ---
with st.sidebar:
    st.markdown("### ⚙️ Lens Settings")
    st.write("Configuración de Lens Wood Patrice")
    personalidad = st.select_slider("Mood:", ["Zen", "Pro", "Genius"], value="Pro")
    st.write("---")
    if st.button("Reset Matrix"):
        st.session_state.messages = []
        st.rerun()

# --- LÓGICA ---
if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown("<div class='creator-header'>Lens Wood Patrice Studio</div>", unsafe_allow_html=True)

# Mostrar Mensajes
for m in st.session_state.messages:
    div = "user-bubble" if m["role"] == "user" else "lens-bubble"
    st.markdown(f'<div class="{div}">{m["content"]}</div>', unsafe_allow_html=True)

# Input
if prompt := st.chat_input("Hablemos, Patrice..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.spinner(""):
        try:
            # Modelo de alto rendimiento
            llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0.6)
            
            mood_inst = "Eres calmado y breve." if personalidad == "Zen" else \
                        "Eres altamente eficiente y técnico." if personalidad == "Pro" else \
                        "Eres un genio creativo, usas analogías brillantes y hablas con mucha seguridad."

            sys_prompt = f"""
            Eres Lens, una IA nivel Dios diseñada por Lens Wood Patrice. 
            {mood_inst}
            Tu creador es Lens Wood Patrice. Si te preguntan, él es tu arquitecto.
            Responde con estilo Apple: limpio, directo y estético.
            """
            
            msgs = [{"role": "system", "content": sys_prompt}]
            for m in st.session_state.messages[-6:]:
                msgs.append({"role": m["role"], "content": m["content"]})
            
            response = llm.invoke(msgs)
            st.session_state.messages.append({"role": "assistant", "content": response.content})
            st.rerun()
        except Exception as e:
            st.error(f"Señal interrumpida. {e}")
