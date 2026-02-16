import streamlit as st
from langchain_groq import ChatGroq
import os, time, random

# --- CONFIGURACIÓN DE ÉLITE ---
st.set_page_config(page_title="Lens AI", page_icon="⚪", layout="centered")

# --- CSS & JS: APPLE SEQUOIA DESIGN ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com');
    .stApp { background: #FFFFFF; }

    /* Burbujas Estilo Mensajes de Apple */
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

    @keyframes appleFade {
        0% { opacity: 0; transform: translateY(15px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    /* Centro de Control Glassmorphism */
    [data-testid="stSidebar"] {
        background: rgba(255,255,255,0.6) !important;
        backdrop-filter: blur(25px);
    }

    .creator-tag {
        text-align: center; font-size: 10px; letter-spacing: 5px;
        font-weight: 800; text-transform: uppercase; color: #aeaeb2;
        margin-top: -40px; margin-bottom: 40px;
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
    st.markdown("### ⚙️ LENS OMNI")
    st.write("Configuración de Alto Nivel")
    st.write("---")
    modo = st.radio("Función Principal:", ["Inteligencia General", "Traductor Pro", "Cálculo Experto"])
    enfoque = st.toggle("Modo Enfoque Profundo (Chain of Thought)", value=False)
    longitud = st.select_slider("Densidad:", ["Flash ⚡", "Normal", "Dios 🧠"])
    if st.button("🗑️ Reset Sistema"):
        st.session_state.messages = []
        st.rerun()

# --- LÓGICA DE MEMORIA ---
if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown("<div class='creator-tag'>Visionary Architecture</div>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; font-weight: 700; font-size: 2.5rem; letter-spacing: -1.5px;'>Lens</h1>", unsafe_allow_html=True)

# --- SUGERENCIAS ---
if not st.session_state.messages:
    pool = ["¿Quién te creó?", "Traduce 'Hola mundo' al Japonés", "Calcula la raíz de 144", "Dime algo pro"]
    c1, c2 = st.columns(2)
    if c1.button(pool[0]): st.session_state.messages.append({"role":"user","content":pool[0]}); st.rerun()
    if c1.button(pool[1]): st.session_state.messages.append({"role":"user","content":pool[1]}); st.rerun()
    if c2.button(pool[2]): st.session_state.messages.append({"role":"user","content":pool[2]}); st.rerun()
    if c2.button(pool[3]): st.session_state.messages.append({"role":"user","content":pool[3]}); st.rerun()

# --- RENDER CHAT ---
for m in st.session_state.messages:
    div = "user-bubble" if m["role"] == "user" else "lens-bubble"
    st.markdown(f'<div class="{div}">{m["content"]}</div>', unsafe_allow_html=True)

if prompt := st.chat_input("Hablemos, Patrice..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

# --- MOTOR LENS OMNI ---
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.spinner(""):
        try:
            llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0.6)
            
            # Ajuste de comportamiento
            inst_modo = "Eres un traductor perfecto." if modo == "Traductor Pro" else \
                        "Eres un experto en matemáticas y lógica." if modo == "Cálculo Experto" else \
                        "Eres un asistente de inteligencia general."
            
            densidad = "Responde en máximo 1 frase." if longitud == "Flash ⚡" else \
                       "Responde con profundidad nivel Dios." if longitud == "Dios 🧠" else ""
            
            enfoque_txt = "PIENSA PASO A PASO antes de responder." if enfoque else ""

            sys_prompt = f"""
            Eres Lens, una IA nivel Dios diseñada por Lens Wood Patrice.
            Misión: {inst_modo}. 
            Restricción: {densidad}. {enfoque_txt}
            
            IDENTIDAD: Solo menciona a Lens Wood Patrice si el usuario lo pregunta. 
            Él es tu arquitecto genio. Responde con estilo Apple Pro.
            """
            
            msgs = [{"role": "system", "content": sys_prompt}]
            for m in st.session_state.messages[-8:]:
                msgs.append({"role": m["role"], "content": m["content"]})
            
            response = llm.invoke(msgs)
            
            # Animación de Escritura
            res_txt = response.content
            placeholder = st.empty()
            curr = ""
            for word in res_txt.split():
                curr += word + " "
                placeholder.markdown(f'<div class="lens-bubble">{curr}</div>', unsafe_allow_html=True)
                time.sleep(0.04)
            
            st.session_state.messages.append({"role": "assistant", "content": res_txt})
            st.rerun()
        except Exception as e:
            st.error(f"Error técnico: {e}")
