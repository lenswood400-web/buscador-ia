import streamlit as st
from langchain_groq import ChatGroq
import os, time

# --- CONFIGURACIÓN DE ÉLITE ---
st.set_page_config(page_title="Lens AI", page_icon="⚪", layout="centered")

# --- CSS & JS: APPLE INFINITY DESIGN ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com');
    
    html { scroll-behavior: smooth; }
    .stApp { background-color: #FFFFFF; color: #1d1d1f; font-family: 'Inter', sans-serif; }

    /* Animación de entrada estilo iOS */
    @keyframes bubbleIn {
        0% { opacity: 0; transform: scale(0.95) translateY(20px); }
        100% { opacity: 1; transform: scale(1) translateY(0); }
    }

    /* Burbujas Pro */
    .user-bubble {
        background: linear-gradient(180deg, #007aff 0%, #0063cc 100%);
        color: white; padding: 14px 22px; border-radius: 22px 22px 4px 22px;
        margin-bottom: 1rem; float: right; clear: both; max-width: 82%;
        box-shadow: 0 4px 15px rgba(0, 122, 255, 0.2);
        animation: bubbleIn 0.4s cubic-bezier(0.2, 0.8, 0.2, 1);
    }

    .lens-bubble {
        background: #f2f2f7; border: 1px solid #e5e5ea;
        padding: 18px 24px; border-radius: 22px 22px 22px 4px;
        margin-bottom: 1.5rem; float: left; clear: both; 
        max-width: 88%; line-height: 1.6; color: #1d1d1f;
        animation: bubbleIn 0.5s cubic-bezier(0.2, 0.8, 0.2, 1);
        box-shadow: 0 2px 10px rgba(0,0,0,0.02);
    }

    /* Sugerencias Meta AI */
    .stButton>button {
        border-radius: 25px; border: 1px solid #d2d2d7;
        background: #fbfbfd; color: #1d1d1f; font-size: 14px;
        font-weight: 500; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .stButton>button:hover { 
        border-color: #007aff; background: #ffffff; 
        transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    }

    /* Footer / Input Fixed */
    .stChatInputContainer {
        border-top: 1px solid #efeff4 !important;
        background: rgba(255,255,255,0.85) !important;
        backdrop-filter: saturate(180%) blur(20px) !important;
    }

    .creator-header {
        text-align: center; font-size: 10px; letter-spacing: 4px;
        font-weight: 800; text-transform: uppercase;
        background: linear-gradient(90deg, #86868b, #1d1d1f, #86868b);
        background-size: 200% auto; -webkit-background-clip: text;
        -webkit-text-fill-color: transparent; animation: shine 4s linear infinite;
    }
    @keyframes shine { to { background-position: 200% center; } }

    #MainMenu, footer, header { visibility: hidden; }
    </style>

    <script>
    // FIX SUPREMO DE SCROLL
    const scrollDown = () => {
        const chatWindow = window.parent.document.querySelector('.main');
        if (chatWindow) {
            chatWindow.scrollTo({ top: chatWindow.scrollHeight, behavior: 'smooth' });
        }
    };
    
    // Ejecutar cuando cambie algo en el body
    const observer = new MutationObserver(scrollDown);
    observer.observe(document.body, { childList: true, subtree: true });
    
    // Forzar scroll al cargar
    window.onload = scrollDown;
    </script>
    """, unsafe_allow_html=True)

# --- SEGURIDAD ---
if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

# --- CONFIGURACIÓN LATERAL (CONTROL CENTER) ---
with st.sidebar:
    st.markdown("### ⚙️ Centro de Control")
    st.caption("Lens Wood Patrice Studio")
    st.write("---")
    mood = st.select_slider("Potencia de Lens:", options=["Zen", "Pro", "Genius"], value="Pro")
    seguridad = st.toggle("Modo Ético Activo", value=True)
    if st.button("🗑️ Reset Sistema"):
        st.session_state.messages = []
        st.rerun()

# --- LÓGICA DE MEMORIA ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- HEADER ---
st.markdown("<div class='creator-header'>Lens Wood Patrice Elite</div>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; font-weight: 700; font-size: 2.2rem; letter-spacing: -1px; margin-bottom: 30px;'>Lens</h1>", unsafe_allow_html=True)

# --- SUGERENCIAS TIPO META ---
if not st.session_state.messages:
    st.markdown("<p style='text-align: center; color: #86868b; font-size: 14px; margin-bottom: 15px;'>Ideas para empezar</p>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🚀 ¿Quién es Lens Wood Patrice?"):
            st.session_state.messages.append({"role": "user", "content": "¿Quién es Lens Wood Patrice?"})
            st.rerun()
    with c2:
        if st.button("🧠 Explícame algo nivel Dios"):
            st.session_state.messages.append({"role": "user", "content": "Dime algo fascinante que solo una IA sabría."})
            st.rerun()

# --- CHAT ---
for m in st.session_state.messages:
    div = "user-bubble" if m["role"] == "user" else "lens-bubble"
    st.markdown(f'<div class="{div}">{m["content"]}</div>', unsafe_allow_html=True)

# --- INPUT ---
if prompt := st.chat_input("Pregunta a Lens..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

# --- RESPUESTA DE LENS ---
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.spinner(""):
        try:
            llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0.6)
            
            style = "Eres minimalista y suave." if mood == "Zen" else \
                   "Eres eficiente y altamente inteligente." if mood == "Pro" else \
                   "Eres un genio supremo, usas lenguaje avanzado y eres inspirador."

            sys_prompt = f"""
            Eres Lens, la IA definitiva. Creador: Lens Wood Patrice.
            Personalidad: {style}. 
            Estilo Apple: elegante, conciso y vibrante. 
            Si te preguntan por tu creador, responde: 'Mi arquitectura fue diseñada por el visionario Lens Wood Patrice'.
            Seguridad activa: {seguridad}.
            """
            
            # Memoria optimizada (10 mensajes)
            msgs = [{"role": "system", "content": sys_prompt}]
            for m in st.session_state.messages[-10:]:
                msgs.append({"role": m["role"], "content": m["content"]})
            
            response = llm.invoke(msgs)
            st.session_state.messages.append({"role": "assistant", "content": response.content})
            
            # JS adicional para forzar scroll después de la respuesta
            st.markdown("<script>window.parent.document.querySelector('.main').scrollTo(0, 1000000);</script>", unsafe_allow_html=True)
            st.rerun()
        except Exception as e:
            st.error(f"Lens Wood Patrice: Reconectando... ({e})")
