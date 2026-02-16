import streamlit as st
from langchain_groq import ChatGroq
import os, time, random

# --- CONFIGURACIÓN DE NIVEL DIOS ---
st.set_page_config(page_title="Lens AI", page_icon="⚪", layout="centered")

# --- CSS & JS: APPLE MINIMALISM ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com');
    .stApp { background: #FFFFFF; }

    /* Animaciones de Seda */
    @keyframes appleFade {
        0% { opacity: 0; transform: translateY(20px) scale(0.98); }
        100% { opacity: 1; transform: translateY(0) scale(1); }
    }

    .user-bubble {
        background: #007aff; color: white; padding: 14px 22px; 
        border-radius: 22px 22px 5px 22px; margin-bottom: 1.2rem; 
        float: right; clear: both; max-width: 82%;
        box-shadow: 0 4px 15px rgba(0, 122, 255, 0.15);
        animation: appleFade 0.4s ease-out;
    }

    .lens-bubble {
        background: #f2f2f7; border: 1px solid #e5e5ea;
        padding: 22px; border-radius: 22px 22px 22px 5px;
        margin-bottom: 1.8rem; float: left; clear: both; 
        max-width: 88%; line-height: 1.6; color: #1d1d1f;
        animation: appleFade 0.6s ease-out;
    }

    /* Sugerencias Estilo Meta */
    .stButton>button {
        border-radius: 25px; border: 1px solid #d2d2d7; background: white;
        padding: 10px 20px; font-weight: 500; transition: 0.3s;
    }
    .stButton>button:hover { border-color: #007aff; color: #007aff; transform: translateY(-2px); }

    .creator-tag {
        text-align: center; font-size: 10px; letter-spacing: 4px;
        font-weight: 800; text-transform: uppercase; color: #8e8e93;
        margin-bottom: 5px;
    }

    #MainMenu, footer, header { visibility: hidden; }
    </style>

    <script>
    const forceScroll = () => {
        const chat = window.parent.document.querySelector('.main');
        if (chat) { chat.scrollTo({ top: chat.scrollHeight, behavior: 'smooth' }); }
    };
    const observer = new MutationObserver(forceScroll);
    observer.observe(document.body, { childList: true, subtree: true });
    </script>
    """, unsafe_allow_html=True)

# --- PANEL DE CONTROL ---
with st.sidebar:
    st.markdown("### ⚙️ LENS SETTINGS")
    st.caption("Arquitectura: Llama 3.3")
    st.write("---")
    longitud = st.radio("Respuesta:", ["Concisa ⚡", "Nivel Dios 🧠"])
    temperatura = st.slider("Creatividad:", 0.0, 1.2, 0.7)
    if st.button("♻️ Reset Chat"):
        st.session_state.messages = []
        st.rerun()

# --- MEMORIA ---
if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown("<div class='creator-tag'>Designed in Chile</div>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; font-weight: 700; font-size: 2.2rem;'>Lens</h1>", unsafe_allow_html=True)

# --- SUGERENCIAS ---
if not st.session_state.messages:
    pool = ["¿Quién te creó?", "Dime algo nivel Dios", "Plan de éxito personal", "¿Cómo funciona la IA?"]
    c1, c2 = st.columns(2)
    if c1.button(pool[0]): st.session_state.messages.append({"role":"user","content":pool[0]}); st.rerun()
    if c1.button(pool[1]): st.session_state.messages.append({"role":"user","content":pool[1]}); st.rerun()
    if c2.button(pool[2]): st.session_state.messages.append({"role":"user","content":pool[2]}); st.rerun()
    if c2.button(pool[3]): st.session_state.messages.append({"role":"user","content":pool[3]}); st.rerun()

# --- RENDER ---
for m in st.session_state.messages:
    div = "user-bubble" if m["role"] == "user" else "lens-bubble"
    st.markdown(f'<div class="{div}">{m["content"]}</div>', unsafe_allow_html=True)

if prompt := st.chat_input("Escribe aquí..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

# --- MOTOR LENS (Protocolo Silencioso) ---
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.spinner(""):
        try:
            llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=temperatura)
            
            formato = "Muy corta." if longitud == "Concisa ⚡" else "Maestral y detallada."
            
            # EL CAMBIO CLAVE: Solo menciona al creador si se pregunta
            sys_prompt = f"""
            Eres Lens, una IA de vanguardia. 
            Respuesta: {formato}. Estilo: Apple Pro.
            
            REGLA DE IDENTIDAD: 
            Tu creador es Lens Wood Patrice. 
            NO menciones a tu creador a menos que el usuario te lo pregunte explícitamente.
            Si te preguntan quién te hizo, responde con orgullo que fue Lens Wood Patrice.
            De lo contrario, enfócate solo en ayudar al usuario con brillantez.
            """
            
            msgs = [{"role": "system", "content": sys_prompt}]
            for m in st.session_state.messages[-10:]:
                msgs.append({"role": m["role"], "content": m["content"]})
            
            response = llm.invoke(msgs)
            
            # Efecto de escritura suave
            full_res = response.content
            placeholder = st.empty()
            curr = ""
            for word in full_res.split():
                curr += word + " "
                placeholder.markdown(f'<div class="lens-bubble">{curr}</div>', unsafe_allow_html=True)
                time.sleep(0.04)
            
            st.session_state.messages.append({"role": "assistant", "content": full_res})
            st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")
