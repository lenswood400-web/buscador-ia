import streamlit as st
from langchain_groq import ChatGroq
import os

# --- CONFIGURACIÓN DE ALTO NIVEL ---
st.set_page_config(page_title="Lens AI", page_icon="⚪", layout="centered")

# --- CSS: ESTÉTICA APPLE PREMUM & SUGERENCIAS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com');
    
    .stApp { background-color: #FFFFFF; color: #1d1d1f; }

    /* Nombre del Creador con Gradiente Animado */
    .creator-header {
        text-align: center; font-size: 11px; letter-spacing: 4px;
        font-weight: 700; text-transform: uppercase;
        background: linear-gradient(to right, #8e8e93, #1d1d1f, #8e8e93);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient 3s linear infinite;
        margin-bottom: 5px;
    }
    @keyframes gradient { to { background-position: 200% center; } }

    /* Burbujas de Chat Refinadas */
    .user-bubble {
        background: #007aff; color: white; padding: 14px 20px; 
        border-radius: 22px 22px 4px 22px; margin-bottom: 1rem; 
        float: right; clear: both; max-width: 80%;
        box-shadow: 0 4px 12px rgba(0, 122, 255, 0.15); font-size: 15px;
    }

    .lens-bubble {
        background: #f5f5f7; border: 1px solid #e5e5e7;
        padding: 20px; border-radius: 22px 22px 22px 4px;
        margin-bottom: 1.5rem; float: left; clear: both; 
        max-width: 85%; font-size: 15px; line-height: 1.6;
    }

    /* Sugerencias estilo Meta AI */
    .suggestion-container {
        display: flex; flex-wrap: wrap; justify-content: center; gap: 10px; margin-top: 20px;
    }
    .suggestion-btn {
        background: #FFFFFF; border: 1px solid #d2d2d7; padding: 8px 16px;
        border-radius: 18px; font-size: 13px; color: #1d1d1f; cursor: pointer;
        transition: all 0.2s ease;
    }
    .suggestion-btn:hover { background: #f5f5f7; border-color: #86868b; }

    /* Fix Scroll y Input */
    .stChatInputContainer { background-color: rgba(255,255,255,0.9) !important; backdrop-filter: blur(20px); }
    #MainMenu, footer, header {visibility: hidden;}
    </style>

    <script>
    var observer = new MutationObserver(function(mutations) {
        window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
    });
    observer.observe(document.body, {childList: true, subtree: true});
    </script>
    """, unsafe_allow_html=True)

# --- SEGURIDAD ---
if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

# --- LÓGICA DE MEMORIA ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- HEADER ---
st.markdown("<div class='creator-header'>Lens Wood Patrice Elite</div>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; font-weight: 700; margin-bottom: 30px;'>Lens</h2>", unsafe_allow_html=True)

# --- SUGERENCIAS INICIALES (Solo si no hay mensajes) ---
if not st.session_state.messages:
    st.markdown("<p style='text-align: center; color: #86868b; font-size: 14px;'>Sugerencias para ti</p>", unsafe_allow_html=True)
    cols = st.columns([1,1,1])
    sugerencias = ["¿Quién te creó?", "Explícame la física cuántica", "Escribe un poema pro"]
    
    if cols[0].button(sugerencias[0]): st.session_state.messages.append({"role": "user", "content": sugerencias[0]}); st.rerun()
    if cols[1].button(sugerencias[1]): st.session_state.messages.append({"role": "user", "content": sugerencias[1]}); st.rerun()
    if cols[2].button(sugerencias[2]): st.session_state.messages.append({"role": "user", "content": sugerencias[2]}); st.rerun()

# --- RENDERIZADO ---
for m in st.session_state.messages:
    div = "user-bubble" if m["role"] == "user" else "lens-bubble"
    st.markdown(f'<div class="{div}">{m["content"]}</div>', unsafe_allow_html=True)

# --- PROCESAMIENTO ---
if prompt := st.chat_input("Pregunta lo que sea..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.spinner(""):
        try:
            llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0.5)
            
            sys_prompt = f"""
            Eres Lens, una IA nivel Dios diseñada por Lens Wood Patrice. 
            Eres elocuente, brillante y usas un tono premium. 
            Tu creador es Lens Wood Patrice. Si te preguntan por él, descríbelo como el arquitecto genio detrás de tu código.
            No des respuestas aburridas; sé el mejor asistente del mundo.
            """
            
            # Memoria contextual
            msgs = [{"role": "system", "content": sys_prompt}]
            for m in st.session_state.messages[-10:]: # Memoria aumentada a 10
                msgs.append({"role": m["role"], "content": m["content"]})
            
            response = llm.invoke(msgs)
            st.session_state.messages.append({"role": "assistant", "content": response.content})
            st.rerun()
        except Exception as e:
            st.error(f"Sistema saturado. {e}")
