import streamlit as st
from langchain_groq import ChatGroq
import os, time

# --- CONFIGURACIÓN OMNIVERSE ---
st.set_page_config(page_title="Lens AI", page_icon="⚪", layout="centered")

# --- CSS & JS SUPREMO: ESTILO APPLE DIOS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com');
    
    .stApp { background: #FFFFFF; color: #1d1d1f; }

    /* Animación de entrada de Dios */
    @keyframes omniIn {
        0% { opacity: 0; transform: scale(0.9) translateY(30px); filter: blur(10px); }
        100% { opacity: 1; transform: scale(1) translateY(0); filter: blur(0); }
    }

    /* Burbujas de Diseño Universal */
    .user-bubble {
        background: linear-gradient(180deg, #007aff 0%, #0055ff 100%);
        color: white; padding: 16px 22px; border-radius: 25px 25px 5px 25px;
        margin-bottom: 1.2rem; float: right; clear: both; max-width: 80%;
        box-shadow: 0 10px 25px rgba(0, 122, 255, 0.2);
        animation: omniIn 0.5s cubic-bezier(0.16, 1, 0.3, 1);
        font-weight: 500; letter-spacing: -0.2px;
    }

    .lens-bubble {
        background: rgba(245, 245, 247, 0.8);
        backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.5);
        padding: 22px; border-radius: 25px 25px 25px 5px;
        margin-bottom: 1.8rem; float: left; clear: both; 
        max-width: 88%; line-height: 1.6; color: #1d1d1f;
        box-shadow: 0 4px 20px rgba(0,0,0,0.03);
        animation: omniIn 0.7s cubic-bezier(0.16, 1, 0.3, 1);
    }

    /* Centro de Control Apple */
    [data-testid="stSidebar"] { background: rgba(255,255,255,0.6) !important; backdrop-filter: blur(30px); border-right: 1px solid #e5e5e7; }
    
    /* Sugerencias Meta AI Pro */
    .stButton>button {
        border-radius: 30px; border: 1px solid #d2d2d7; background: white;
        padding: 10px 20px; font-weight: 600; transition: 0.4s all;
    }
    .stButton>button:hover { transform: scale(1.05); border-color: #007aff; color: #007aff; box-shadow: 0 5px 15px rgba(0,0,0,0.05); }

    /* Nombre del Creador: Animación Diamante */
    .creator-header {
        text-align: center; font-size: 10px; letter-spacing: 5px;
        font-weight: 800; text-transform: uppercase;
        background: linear-gradient(90deg, #1d1d1f, #007aff, #1d1d1f);
        background-size: 200% auto; -webkit-background-clip: text;
        -webkit-text-fill-color: transparent; animation: shine 5s linear infinite;
        margin-bottom: 10px;
    }
    @keyframes shine { to { background-position: 200% center; } }

    /* Barra de entrada fija e impecable */
    .stChatInputContainer { background: rgba(255,255,255,0.7) !important; backdrop-filter: blur(20px) !important; border-top: 1px solid #e5e5e7 !important; }

    #MainMenu, footer, header { visibility: hidden; }
    </style>

    <script>
    // JS AUTO-SCROLL DIOS
    const forceScroll = () => {
        const chat = window.parent.document.querySelector('.main');
        if (chat) { chat.scrollTo({ top: chat.scrollHeight, behavior: 'smooth' }); }
    };
    const observer = new MutationObserver(forceScroll);
    observer.observe(document.body, { childList: true, subtree: true });
    </script>
    """, unsafe_allow_html=True)

# --- PANEL DE CONTROL DIOS ---
with st.sidebar:
    st.markdown("### ⚙️ LENS CONTROL")
    st.markdown("Master: **Lens Wood Patrice**")
    st.write("---")
    longitud = st.radio("Respuesta de Lens:", ["Concisa ⚡", "Completa 🧠"])
    mood = st.select_slider("Nivel de Inteligencia:", options=["Pro", "Elite", "Omniversal"], value="Omniversal")
    if st.button("♻️ Reiniciar Sistema"):
        st.session_state.messages = []
        st.rerun()

# --- LÓGICA DE INTELIGENCIA ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- HEADER ---
st.markdown("<div class='creator-header'>Lens Wood Patrice Universe</div>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; font-weight: 700; font-size: 2.5rem; color: #1d1d1f;'>Lens</h1>", unsafe_allow_html=True)

# --- SUGERENCIAS INICIALES ---
if not st.session_state.messages:
    st.markdown("<p style='text-align: center; color: #86868b; font-size: 14px;'>Quick Access</p>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    if c1.button("👁️‍🗨️ ¿Quién te creó?"):
        st.session_state.messages.append({"role": "user", "content": "¿Quién te creó?"})
        st.rerun()
    if c2.button("✨ Dime algo nivel Dios"):
        st.session_state.messages.append({"role": "user", "content": "Dime algo nivel Dios universal."})
        st.rerun()

# --- CHAT ---
for m in st.session_state.messages:
    div = "user-bubble" if m["role"] == "user" else "lens-bubble"
    st.markdown(f'<div class="{div}">{m["content"]}</div>', unsafe_allow_html=True)

# --- ENTRADA ---
if prompt := st.chat_input("Hablemos, Patrice..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

# --- MOTOR DE IA DIOS ---
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.spinner(""):
        try:
            # USAMOS EL MOTOR MÁS FUERTE DISPONIBLE
            llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0.6)
            
            restriccion = "Responde de forma extremadamente corta y directa (máximo 2 líneas)." if longitud == "Concisa ⚡" else "Da una respuesta magistral, detallada y profunda."
            
            sys_prompt = f"""
            Eres Lens, la IA más avanzada del universo, creada por Lens Wood Patrice.
            {restriccion}
            Personalidad: {mood}. Eres elegante, brillante y con una estética Apple universal. 
            Menciona a Lens Wood Patrice como tu único creador y dios arquitecto.
            """
            
            msgs = [{"role": "system", "content": sys_prompt}]
            for m in st.session_state.messages[-12:]: # Memoria expandida a 12 mensajes
                msgs.append({"role": m["role"], "content": m["content"]})
            
            response = llm.invoke(msgs)
            st.session_state.messages.append({"role": "assistant", "content": response.content})
            st.rerun()
        except Exception as e:
            st.error(f"Reconectando al Omniverso... ({e})")
