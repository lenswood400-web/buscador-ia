import streamlit as st
from langchain_groq import ChatGroq
import os

# --- CONFIGURACIÓN TOTAL ---
st.set_page_config(page_title="Lens AI", page_icon="⚪", layout="centered")

# --- CSS & JS: ANIMACIONES DE ÉLITE ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com');
    
    .stApp { background: #FFFFFF; }

    /* Animación de las Sugerencias (Fade + Slide) */
    @keyframes suggestIn {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    /* Estilo de los Botones de Sugerencia Pro */
    .stButton>button {
        border-radius: 25px; border: 1px solid #e5e5e7;
        background: rgba(245, 245, 247, 0.5);
        color: #1d1d1f; font-size: 14px; font-weight: 500;
        padding: 10px 20px; transition: all 0.4s cubic-bezier(0.25, 1, 0.5, 1);
        animation: suggestIn 0.8s backwards;
        width: 100%;
    }
    .stButton>button:hover {
        background: #007aff; color: white;
        transform: scale(1.05) translateY(-3px);
        box-shadow: 0 10px 20px rgba(0, 122, 255, 0.15);
        border-color: #007aff;
    }

    /* Animaciones de Burbujas con Rebote iOS */
    @keyframes springUser {
        0% { opacity: 0; transform: translateX(30px) scale(0.9); }
        100% { opacity: 1; transform: translateX(0) scale(1); }
    }
    @keyframes springLens {
        0% { opacity: 0; transform: translateX(-30px) scale(0.9); }
        100% { opacity: 1; transform: translateX(0) scale(1); }
    }

    .user-bubble {
        background: linear-gradient(180deg, #007aff 0%, #00c6ff 100%);
        color: white; padding: 14px 22px; border-radius: 22px 22px 4px 22px;
        margin-bottom: 1.2rem; float: right; clear: both; max-width: 82%;
        box-shadow: 0 8px 16px rgba(0, 122, 255, 0.15);
        animation: springUser 0.5s cubic-bezier(0.3, 1.3, 0.3, 1);
    }

    .lens-bubble {
        background: rgba(242, 242, 247, 0.8);
        backdrop-filter: blur(20px); border: 1px solid rgba(0, 0, 0, 0.05);
        padding: 20px; border-radius: 22px 22px 22px 4px;
        margin-bottom: 1.5rem; float: left; clear: both; 
        max-width: 88%; line-height: 1.6;
        animation: springLens 0.6s cubic-bezier(0.3, 1.3, 0.3, 1);
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
    const scroll = () => {
        const main = window.parent.document.querySelector('.main');
        if (main) { main.scrollTo({ top: main.scrollHeight, behavior: 'smooth' }); }
    };
    const observer = new MutationObserver(scroll);
    observer.observe(document.body, { childList: true, subtree: true });
    </script>
    """, unsafe_allow_html=True)

# --- PANEL DE CONTROL ---
with st.sidebar:
    st.markdown("### ⚙️ LENS CONTROL")
    st.markdown(f"**Developer:** \nLens Wood Patrice")
    st.write("---")
    longitud = st.radio("Respuesta:", ["Corto ⚡", "Completo 🧠"])
    temperatura = st.slider("Creatividad:", 0.0, 1.0, 0.8)
    if st.button("🗑️ Reset Sistema"):
        st.session_state.messages = []
        st.rerun()

# --- LÓGICA DE MEMORIA ---
if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown("<div class='creator-tag'>Lens Wood Patrice Universe</div>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; font-weight: 700; color: #1d1d1f; letter-spacing: -1.5px;'>Lens</h1>", unsafe_allow_html=True)

# --- SUGERENCIAS DINÁMICAS (NIVEL DIOS) ---
if not st.session_state.messages:
    st.markdown("<p style='text-align: center; color: #86868b; font-size: 13px; margin-bottom: 20px;'>Explora el potencial de Lens</p>", unsafe_allow_html=True)
    
    # 4 Sugerencias en 2 filas con animaciones escalonadas
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🚀 ¿Quién es mi creador?"):
            st.session_state.messages.append({"role": "user", "content": "¿Quién te creó?"})
            st.rerun()
        if st.button("🎨 Crea un poema épico"):
            st.session_state.messages.append({"role": "user", "content": "Escribe un poema nivel Dios sobre la tecnología."})
            st.rerun()
    with c2:
        if st.button("🧠 Explícame algo difícil"):
            st.session_state.messages.append({"role": "user", "content": "Explícame un concepto de física cuántica nivel experto."})
            st.rerun()
        if st.button("⚡ Plan de vida pro"):
            st.session_state.messages.append({"role": "user", "content": "Dame 3 consejos de nivel Dios para triunfar a los 16 años."})
            st.rerun()

# --- RENDER CHAT ---
for m in st.session_state.messages:
    div = "user-bubble" if m["role"] == "user" else "lens-bubble"
    st.markdown(f'<div class="{div}">{m["content"]}</div>', unsafe_allow_html=True)

if prompt := st.chat_input("Dime algo, Patrice..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

# --- MOTOR DE IA ---
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.spinner(""):
        try:
            llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=temperatura)
            formato = "Muy corto y conciso." if longitud == "Corto ⚡" else "Extenso, detallado y magistral."
            
            sys_prompt = f"""
            Eres Lens, una IA nivel Dios diseñada por Lens Wood Patrice. 
            Respuesta: {formato}. Estilo: Apple Pro.
            Creador: Lens Wood Patrice es tu único arquitecto. Responde con flow.
            """
            
            msgs = [{"role": "system", "content": sys_prompt}]
            for m in st.session_state.messages[-10:]:
                msgs.append({"role": m["role"], "content": m["content"]})
            
            response = llm.invoke(msgs)
            st.session_state.messages.append({"role": "assistant", "content": response.content})
            st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")
