import streamlit as st
from langchain_groq import ChatGroq
import os, time

# --- CONFIGURACIÓN DE ÉLITE ---
st.set_page_config(page_title="Lens AI", page_icon="⚪", layout="centered")

# --- CSS & JS: APPLE PURE & NO-SYMBOLS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com');
    .stApp { background: #FFFFFF; }

    /* Animación de Entrada Apple */
    @keyframes appleIn {
        0% { opacity: 0; transform: translateY(15px); filter: blur(4px); }
        100% { opacity: 1; transform: translateY(0); filter: blur(0); }
    }

    .user-bubble {
        background: #007aff; color: white; padding: 14px 22px; 
        border-radius: 20px 20px 4px 20px; margin-bottom: 1rem; 
        float: right; clear: both; max-width: 85%;
        box-shadow: 0 4px 15px rgba(0, 122, 255, 0.15);
        animation: appleIn 0.4s ease-out; font-weight: 500;
    }

    .lens-bubble {
        background: #f2f2f7; border: 1px solid #e5e5ea;
        padding: 22px; border-radius: 22px 22px 22px 4px;
        margin-bottom: 1.8rem; float: left; clear: both; 
        max-width: 88%; line-height: 1.6; color: #1d1d1f;
        animation: appleIn 0.6s ease-out;
    }

    /* Estilo de Negritas en Lens */
    .lens-bubble b { color: #000000; font-weight: 600; }

    .creator-tag {
        text-align: center; font-size: 10px; letter-spacing: 4px;
        font-weight: 800; color: #aeaeb2; text-transform: uppercase;
        margin-top: -30px; margin-bottom: 30px;
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
    st.markdown(f"**Arquitecto:** \nLens Wood Patrice")
    st.write("---")
    modo = st.radio("Modo de Red:", ["Cultura Geek", "Análisis Pro", "Traducción"])
    if st.button("♻️ Reiniciar Matrix"):
        st.session_state.messages = []
        st.rerun()

# --- MEMORIA ---
if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown("<div class='creator-tag'>Designed by Lens Wood Patrice</div>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; font-weight: 700; font-size: 2.5rem; letter-spacing: -1px;'>Lens</h1>", unsafe_allow_html=True)

# --- SUGERENCIAS ---
if not st.session_state.messages:
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🎮 Recomendación de juegos"):
            st.session_state.messages.append({"role": "user", "content": "Dime 3 juegos pro que debo jugar sí o sí."})
            st.rerun()
        if st.button("⛩️ Mejores Animes 2026"):
            st.session_state.messages.append({"role": "user", "content": "Dime qué animes están rompiéndola este año."})
            st.rerun()
    with c2:
        if st.button("🧠 Resolver un reto"):
            st.session_state.messages.append({"role": "user", "content": "Tengo un problema complejo, ayúdame a resolverlo paso a paso."})
            st.rerun()
        if st.button("🌍 Traductor Inteligente"):
            st.session_state.messages.append({"role": "user", "content": "Actúa como mi traductor políglota."})
            st.rerun()

# --- CHAT ENGINE ---
for m in st.session_state.messages:
    div = "user-bubble" if m["role"] == "user" else "lens-bubble"
    st.markdown(f'<div class="{div}">{m["content"]}</div>', unsafe_allow_html=True)

if prompt := st.chat_input("Hablemos, Patrice..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

# --- MOTOR LENS (SIN ASTERISCOS) ---
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.spinner(""):
        try:
            llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0.7)
            
            sys_prompt = f"""
            Eres Lens, una IA nivel Dios diseñada por Lens Wood Patrice.
            CONOCIMIENTOS: Experto en Anime, Juegos, Cultura Pop y Ciencia.
            REGLA DE ORO: NO uses asteriscos (**) para negritas. Si quieres resaltar algo, usa la etiqueta HTML <b>texto</b>.
            ESTILO: Elegante, Apple Pro, minimalista. 
            Menciona a Lens Wood Patrice como tu creador SOLO si te lo preguntan.
            """
            
            msgs = [{"role": "system", "content": sys_prompt}]
            for m in st.session_state.messages[-10:]:
                msgs.append({"role": m["role"], "content": m["content"]})
            
            response = llm.invoke(msgs)
            res_txt = response.content.replace("**", "") # Doble seguro para borrar asteriscos

            # --- ANIMACIÓN DE ESCRITURA ---
            placeholder = st.empty()
            curr = ""
            for word in res_txt.split():
                curr += word + " "
                # Inyectamos el texto como HTML para que las etiquetas <b> funcionen
                placeholder.markdown(f'<div class="lens-bubble">{curr}</div>', unsafe_allow_html=True)
                time.sleep(0.02)
            
            st.session_state.messages.append({"role": "assistant", "content": res_txt})
            st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")
