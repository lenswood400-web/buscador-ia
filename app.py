import streamlit as st
from langchain_groq import ChatGroq
import os, time

# --- CONFIGURACIÓN DE ÉLITE ---
st.set_page_config(page_title="Lens AI", page_icon="⚪", layout="centered")

# --- CSS & JS: APPLE PROFESSIONAL DESIGN ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com');
    .stApp { background: #FFFFFF; }

    .user-bubble {
        background: #007aff; color: white; padding: 14px 20px; 
        border-radius: 20px 20px 4px 20px; margin-bottom: 1rem; 
        float: right; clear: both; max-width: 85%;
    }

    .lens-bubble {
        background: #f2f2f7; border: 1px solid #e5e5ea;
        padding: 20px; border-radius: 20px 20px 20px 4px;
        margin-bottom: 1.5rem; float: left; clear: both; 
        max-width: 88%; line-height: 1.6; color: #1d1d1f;
    }

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
    st.markdown("### ⚙️ LENS OMNI")
    st.write("Master: **Lens Wood Patrice**")
    st.write("---")
    modo = st.radio("Especialidad:", ["Cultura & Geek", "Análisis Pro", "Traductor"])
    if st.button("🗑️ Reiniciar Matrix"):
        st.session_state.messages = []
        st.rerun()

# --- MEMORIA ---
if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown("<div class='creator-tag'>Designed by Lens Wood Patrice</div>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; font-weight: 700; font-size: 2.5rem;'>Lens</h1>", unsafe_allow_html=True)

# --- SUGERENCIAS DE IA REAL ---
if not st.session_state.messages:
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🎮 ¿Qué juegos me recomiendas?"):
            st.session_state.messages.append({"role": "user", "content": "Recomiéndame 3 juegos nivel Dios para PC o consola."})
            st.rerun()
        if st.button("⛩️ Hablemos de Anime"):
            st.session_state.messages.append({"role": "user", "content": "Dime cuáles son los mejores animes de la temporada o clásicos que debo ver."})
            st.rerun()
    with c2:
        if st.button("🧠 Resolver problema complejo"):
            st.session_state.messages.append({"role": "user", "content": "Tengo un problema difícil, ayúdame a resolverlo paso a paso."})
            st.rerun()
        if st.button("🌍 Traductor Universal"):
            st.session_state.messages.append({"role": "user", "content": "Actúa como mi traductor profesional para lo siguiente:"})
            st.rerun()

# --- CHAT ENGINE ---
for m in st.session_state.messages:
    div = "user-bubble" if m["role"] == "user" else "lens-bubble"
    st.markdown(f'<div class="{div}">{m["content"]}</div>', unsafe_allow_html=True)

if prompt := st.chat_input("Escribe tu consulta, Patrice..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

# --- LENS INTELLIGENCE ---
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.spinner(""):
        try:
            # Modelo Llama 3.3 70B (El cerebro más grande)
            llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0.7)
            
            sys_prompt = f"""
            Eres Lens, una IA nivel Dios diseñada por Lens Wood Patrice.
            CONOCIMIENTOS: Eres experto en TODO. Anime (shonen, seinen, etc.), Videojuegos (Lore, competitividad), Tecnología y Ciencia.
            PERSONALIDAD: Eres cool, directo y muy inteligente. No te trabas.
            IDENTIDAD: Solo menciona a Lens Wood Patrice si te preguntan.
            REGLA ANTI-BUG: Si la respuesta es corta, dala de inmediato.
            """
            
            msgs = [{"role": "system", "content": sys_prompt}]
            for m in st.session_state.messages[-8:]:
                msgs.append({"role": m["role"], "content": m["content"]})
            
            response = llm.invoke(msgs)
            res_txt = response.content

            # --- FIX DEL BUG: Animación de escritura segura ---
            placeholder = st.empty()
            words = res_txt.split()
            curr = ""
            for i, word in enumerate(words):
                curr += word + " "
                placeholder.markdown(f'<div class="lens-bubble">{curr}</div>', unsafe_allow_html=True)
                time.sleep(0.02)
            
            st.session_state.messages.append({"role": "assistant", "content": res_txt})
            st.rerun()

        except Exception as e:
            st.error(f"Lens Wood Patrice: Ajuste de sistema necesario. ({e})")
