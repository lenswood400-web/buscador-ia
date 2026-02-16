import streamlit as st
from langchain_groq import ChatGroq
import os, time, random

# --- CONFIGURACIÓN DIOS DEL TODO ---
st.set_page_config(page_title="Lens AI", page_icon="⚪", layout="centered")

# --- CSS & JS: APPLE GLASSMORPHISM & ANIMATIONS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com');
    
    .stApp { background: #FFFFFF; }

    /* Animación de Entrada Apple Style */
    @keyframes appleIn {
        0% { opacity: 0; transform: translateY(30px) scale(0.95); filter: blur(10px); }
        100% { opacity: 1; transform: translateY(0) scale(1); filter: blur(0); }
    }

    .user-bubble {
        background: linear-gradient(180deg, #007aff 0%, #0055ff 100%);
        color: white; padding: 14px 22px; border-radius: 22px 22px 5px 22px;
        margin-bottom: 1.2rem; float: right; clear: both; max-width: 82%;
        box-shadow: 0 10px 25px rgba(0, 122, 255, 0.2);
        animation: appleIn 0.5s cubic-bezier(0.2, 0.8, 0.2, 1);
        font-weight: 500;
    }

    .lens-bubble {
        background: rgba(242, 242, 247, 0.7);
        backdrop-filter: blur(20px); border: 1px solid rgba(0,0,0,0.05);
        padding: 22px; border-radius: 22px 22px 22px 5px;
        margin-bottom: 1.8rem; float: left; clear: both; 
        max-width: 88%; line-height: 1.6;
        animation: appleIn 0.7s cubic-bezier(0.2, 0.8, 0.2, 1);
    }

    /* Sugerencias Estilo Meta/Apple */
    .stButton>button {
        border-radius: 30px; border: 1px solid #d2d2d7; background: white;
        padding: 10px 20px; font-weight: 600; transition: 0.4s all;
        animation: appleIn 0.8s ease-out;
    }
    .stButton>button:hover { transform: scale(1.05); border-color: #007aff; color: #007aff; }

    /* Sidebar Liquid Glass */
    [data-testid="stSidebar"] {
        background: rgba(255,255,255,0.4) !important;
        backdrop-filter: blur(30px) !important;
        border-right: 1px solid rgba(0,0,0,0.05);
    }

    .creator-tag {
        text-align: center; font-size: 10px; letter-spacing: 5px;
        font-weight: 800; text-transform: uppercase;
        background: linear-gradient(90deg, #1d1d1f, #007aff, #1d1d1f);
        background-size: 200% auto; -webkit-background-clip: text;
        -webkit-text-fill-color: transparent; animation: shine 5s linear infinite;
    }
    @keyframes shine { to { background-position: 200% center; } }

    #MainMenu, footer, header { visibility: hidden; }
    </style>

    <script>
    // FIX DE SCROLL INTELIGENTE
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
    st.markdown("### ⚙️ LENS CONTROL")
    st.markdown(f"**Arquitecto:** \nLens Wood Patrice")
    st.write("---")
    longitud = st.radio("Densidad de Respuesta:", ["Concisa ⚡", "Nivel Dios 🧠", "Poética 🎭"])
    temperatura = st.slider("Creatividad (Entropy):", 0.0, 1.2, 0.7)
    modelo_ia = st.selectbox("Cerebro Lógico:", ["Llama 3.3 70B", "Llama 3.1 8B (Fast)"])
    if st.button("♻️ Reiniciar Memoria"):
        st.session_state.messages = []
        st.rerun()

# --- LÓGICA DE MEMORIA ---
if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown("<div class='creator-tag'>Lens Wood Patrice Universe</div>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; font-weight: 700; font-size: 2.5rem; letter-spacing: -2px;'>Lens</h1>", unsafe_allow_html=True)

# --- SUGERENCIAS DINÁMICAS (Cambian al azar) ---
if not st.session_state.messages:
    pool_sugerencias = [
        "🚀 ¿Quién es Lens Wood Patrice?", "🧠 Explícame algo nivel Dios",
        "🎨 Escribe un poema futurista", "⚡ Plan de éxito a los 16 años",
        "🌌 ¿Qué hay más allá del universo?", "🦾 ¿Cómo dominar la IA?",
        "💎 Dame un consejo de millonario", "🍎 ¿Por qué Apple es pro?"
    ]
    sugerencias = random.sample(pool_sugerencias, 4)
    
    st.markdown("<p style='text-align: center; color: #86868b; font-size: 14px;'>Sugerencias de hoy</p>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button(sugerencias[0]): st.session_state.messages.append({"role": "user", "content": sugerencias[0]}); st.rerun()
        if st.button(sugerencias[1]): st.session_state.messages.append({"role": "user", "content": sugerencias[1]}); st.rerun()
    with c2:
        if st.button(sugerencias[2]): st.session_state.messages.append({"role": "user", "content": sugerencias[2]}); st.rerun()
        if st.button(sugerencias[3]): st.session_state.messages.append({"role": "user", "content": sugerencias[3]}); st.rerun()

# --- RENDER CHAT ---
for m in st.session_state.messages:
    div = "user-bubble" if m["role"] == "user" else "lens-bubble"
    st.markdown(f'<div class="{div}">{m["content"]}</div>', unsafe_allow_html=True)

if prompt := st.chat_input("Hablemos,bro..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

# --- MOTOR DE RESPUESTA CON TYPEWRITER (ANIMACIÓN DE DIOS) ---
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.spinner(""):
        try:
            model_id = "llama-3.3-70b-versatile" if modelo_ia == "Llama 3.3 70B" else "llama-3.1-8b-instant"
            llm = ChatGroq(model_name=model_id, temperature=temperatura)
            
            formato = "Muy conciso (2 líneas)." if longitud == "Concisa ⚡" else \
                      "Extenso y profundo." if longitud == "Nivel Dios 🧠" else \
                      "Elegante, artístico y con rimas sutiles."
            
            sys_prompt = f"""
            Eres Lens, la IA definitiva de Lens Wood Patrice. 
            Respuesta: {formato}. Estilo: Apple Dios.
            Siempre ser amable.
            """
            
            msgs = [{"role": "system", "content": sys_prompt}]
            for m in st.session_state.messages[-10:]:
                msgs.append({"role": m["role"], "content": m["content"]})
            
            response = llm.invoke(msgs)
            
            # --- EFECTO TYPEWRITER ---
            full_res = response.content
            placeholder = st.empty()
            content_simulado = ""
            
            # Animación de escritura palabra por palabra
            for word in full_res.split():
                content_simulado += word + " "
                placeholder.markdown(f'<div class="lens-bubble">{content_simulado}</div>', unsafe_allow_html=True)
                time.sleep(0.05) # Velocidad de Dios
            
            st.session_state.messages.append({"role": "assistant", "content": full_res})
            st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")

