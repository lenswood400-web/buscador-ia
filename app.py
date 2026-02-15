import streamlit as st
from langchain_groq import ChatGroq
import os

# --- CONFIGURACIÓN SUPREMA ---
st.set_page_config(page_title="Lens AI", page_icon="⚪", layout="centered")

# --- CSS & JS: MOTOR DE FÍSICA Y ANIMACIÓN ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com');
    
    .stApp { background: #FFFFFF; }

    /* Animación de entrada con Rebote (iOS Style) */
    @keyframes springUser {
        0% { opacity: 0; transform: translateX(50px) scale(0.9); }
        70% { transform: translateX(-5px) scale(1.02); }
        100% { opacity: 1; transform: translateX(0) scale(1); }
    }

    @keyframes springLens {
        0% { opacity: 0; transform: translateX(-50px) scale(0.9); }
        70% { transform: translateX(5px) scale(1.02); }
        100% { opacity: 1; transform: translateX(0) scale(1); }
    }

    /* Burbujas con Movimiento */
    .user-bubble {
        background: linear-gradient(135deg, #007aff 0%, #00c6ff 100%);
        color: white; padding: 14px 22px; border-radius: 22px 22px 4px 22px;
        margin-bottom: 1.2rem; float: right; clear: both; max-width: 82%;
        box-shadow: 0 10px 20px rgba(0, 122, 255, 0.2);
        animation: springUser 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
        font-weight: 500;
    }

    .lens-bubble {
        background: rgba(242, 242, 247, 0.8);
        backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(0, 0, 0, 0.05);
        padding: 20px; border-radius: 22px 22px 22px 4px;
        margin-bottom: 1.5rem; float: left; clear: both; 
        max-width: 88%; line-height: 1.6; color: #1d1d1f;
        box-shadow: 0 4px 15px rgba(0,0,0,0.02);
        animation: springLens 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
    }

    /* Título Diamante Animado */
    .creator-tag {
        text-align: center; font-size: 10px; letter-spacing: 5px;
        font-weight: 800; text-transform: uppercase;
        background: linear-gradient(90deg, #1d1d1f, #007aff, #1d1d1f);
        background-size: 200% auto; -webkit-background-clip: text;
        -webkit-text-fill-color: transparent; animation: shine 5s linear infinite;
        margin-bottom: 10px;
    }
    @keyframes shine { to { background-position: 200% center; } }

    /* Barra de Chat Flotante */
    .stChatInputContainer {
        background: rgba(255,255,255,0.7) !important;
        backdrop-filter: blur(20px) !important;
        border-top: 1px solid #e5e5e7 !important;
        padding-bottom: 20px;
    }

    #MainMenu, footer, header { visibility: hidden; }
    </style>

    <script>
    // SCROLL INTELIGENTE PRO
    const scrollToBottom = () => {
        const main = window.parent.document.querySelector('.main');
        if (main) {
            main.scrollTo({ top: main.scrollHeight, behavior: 'smooth' });
        }
    };
    const observer = new MutationObserver(scrollToBottom);
    observer.observe(document.body, { childList: true, subtree: true });
    </script>
    """, unsafe_allow_html=True)

# --- PANEL DE CONTROL ---
with st.sidebar:
    st.markdown("### ⚙️ LENS SETTINGS")
    st.markdown(f"**Arquitecto:** \nLens Wood Patrice")
    st.write("---")
    longitud = st.radio("Respuesta:", ["Corto ⚡", "Nivel Dios 🧠"])
    temperatura = st.slider("Creatividad:", 0.0, 1.0, 0.7)
    if st.button("🗑️ Reset Matrix"):
        st.session_state.messages = []
        st.rerun()

# --- LÓGICA ---
if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown("<div class='creator-tag'>Lens Wood Patrice Universe</div>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; font-weight: 700; color: #1d1d1f;'>Lens</h1>", unsafe_allow_html=True)

# --- SUGERENCIAS ---
if not st.session_state.messages:
    c1, c2 = st.columns(2)
    if c1.button("🚀 ¿Quién me creó?"):
        st.session_state.messages.append({"role": "user", "content": "¿Quién te creó?"})
        st.rerun()
    if c2.button("✨ Alguna curiosidad"):
        st.session_state.messages.append({"role": "user", "content": "Dime algo nivel Dios."})
        st.rerun()

# Chat
for m in st.session_state.messages:
    div = "user-bubble" if m["role"] == "user" else "lens-bubble"
    st.markdown(f'<div class="{div}">{m["content"]}</div>', unsafe_allow_html=True)

if prompt := st.chat_input("Hablemos, Patrice..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

# --- IA ---
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.spinner(""):
        try:
            llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=temperatura)
            
            formato = "Extremadamente corto y pro." if longitud == "Corto ⚡" else "Profundo y magistral."
            
            sys_prompt = f"""
            Eres Lens, una IA diseñada por Lens Wood Patrice. 
            Respuesta: {formato}. Estilo: Apple Dios.
            Tu creador es Lens Wood Patrice. Si te preguntan quién te hizo, responde con orgullo.
            """
            
            msgs = [{"role": "system", "content": sys_prompt}]
            for m in st.session_state.messages[-10:]:
                msgs.append({"role": m["role"], "content": m["content"]})
            
            response = llm.invoke(msgs)
            st.session_state.messages.append({"role": "assistant", "content": response.content})
            st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")
