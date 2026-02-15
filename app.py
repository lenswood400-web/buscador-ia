import streamlit as st
from langchain_groq import ChatGroq
import os

# --- CONFIGURACIÓN ESTILO APPLE / GEMINI ---
st.set_page_config(page_title="Lens AI", page_icon="⚪", layout="centered")

# CSS: Interfaz minimalista, limpia y profesional
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com');
    
    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
        background-color: #FFFFFF;
        color: #1d1d1f;
    }

    /* Contenedor de burbujas */
    .stChatMessage {
        background-color: transparent !important;
        border: none !important;
    }

    /* Burbuja de Lens (Estilo Gemini/Apple) */
    .lens-bubble {
        background: rgba(255, 255, 255, 0.8);
        border: 1px solid #e5e5e7;
        padding: 1.5rem;
        border-radius: 22px;
        margin-bottom: 1.5rem;
        line-height: 1.6;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }

    /* Burbuja del Usuario */
    .user-bubble {
        background-color: #f5f5f7;
        padding: 1rem 1.5rem;
        border-radius: 22px;
        margin-bottom: 1.5rem;
        display: inline-block;
        float: right;
        clear: both;
        max-width: 80%;
    }

    .creator-tag {
        text-align: center;
        font-size: 10px;
        letter-spacing: 2px;
        color: #86868b;
        text-transform: uppercase;
        margin-bottom: 2rem;
    }

    /* Input de Chat */
    .stChatInputContainer {
        padding-bottom: 2rem;
        background-color: rgba(255,255,255,0.9) !important;
    }
    
    .stChatInput input {
        border-radius: 25px !important;
        border: 1px solid #d2d2d7 !important;
    }

    /* Eliminar basura visual */
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- SEGURIDAD ---
if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
else:
    # Solo para pruebas locales
    os.environ["GROQ_API_KEY"] = "TU_LLAVE_AQUI"

# --- INICIALIZAR LENS ---
if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown("<div class='creator-tag'>Designed by Lens Wood Patrice</div>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; font-weight: 600;'>Lens</h2>", unsafe_allow_html=True)

# --- RENDERIZADO DEL CHAT ---
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="user-bubble">{message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="lens-bubble">{message["content"]}</div>', unsafe_allow_html=True)

# --- LÓGICA DE INTELIGENCIA ---
if prompt := st.chat_input("¿En qué puedo ayudarte?"):
    # Agregar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

# Si el último mensaje es del usuario, Lens responde
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.spinner(""):
        try:
            # MOTOR: Llama-3.3-70b-specdec (El más avanzado y rápido de Groq ahora)
            llm = ChatGroq(model_name="llama-3.3-70b-specdec", temperature=0.5)
            
            # Personalidad Pro (Clon de Gemini/Apple)
            system_prompt = f"""
            Eres Lens, una inteligencia artificial de vanguardia con un diseño inspirado en la simplicidad de Apple.
            Fuiste concebida y desarrollada por el ingeniero Lens Wood Patrice.
            Tu propósito es ayudar con elegancia, precisión y un toque humano.
            Si te preguntan por tu origen, menciona siempre a Lens Wood Patrice como tu creador.
            Tu estilo de respuesta es limpio, usando negritas para conceptos clave y listas si es necesario.
            """
            
            # Construir memoria para la IA
            messages_for_ai = [{"role": "system", "content": system_prompt}]
            # Enviamos los últimos 6 mensajes para que tenga memoria
            for m in st.session_state.messages[-6:]:
                messages_for_ai.append({"role": m["role"], "content": m["content"]})
            
            response = llm.invoke(messages_for_ai)
            
            # Guardar respuesta
            st.session_state.messages.append({"role": "assistant", "content": response.content})
            st.rerun()

        except Exception as e:
            st.error(f"Lens Wood Patrice: Un detalle técnico ocurrió. ({e})")
