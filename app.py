import streamlit as st
from langchain_groq import ChatGroq
import os, time

# --- CONFIGURACIÓN DE ÉLITE ---
st.set_page_config(page_title="Lens AI", page_icon="⚪", layout="centered")

# --- CSS & JS: MOTOR DE ANIMACIÓN APPLE ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com');
    .stApp { background: #FFFFFF; }

    /* Animación de entrada suave (Slide & Fade) */
    @keyframes appleIn {
        0% { opacity: 0; transform: translateY(20px); filter: blur(5px); }
        100% { opacity: 1; transform: translateY(0); filter: blur(0); }
    }

    .user-bubble {
        background: #007aff; color: white; padding: 14px 22px; 
        border-radius: 20px 20px 4px 20px; margin-bottom: 1rem; 
        float: right; clear: both; max-width: 85%;
        box-shadow: 0 4px 15px rgba(0, 122, 255, 0.15);
        animation: appleIn 0.4s ease-out;
    }

    .lens-bubble {
        background: #f2f2f7; border: 1px solid #e5e5ea;
        padding: 22px; border-radius: 20px 20px 20px 4px;
        margin-bottom: 1.8rem; float: left; clear: both; 
        max-width: 88%; line-height: 1.6; color: #1d1d1f;
        animation: appleIn 0.6s ease-out;
    }

    /* Botones de Sugerencia con Animación */
    .stButton>button {
        border-radius: 20px; border: 1px solid #e5e5ea; background: #FFFFFF;
        padding: 12px; font-weight: 500; transition: 0.3s;
        animation: appleIn 0.8s ease-out;
    }
    .stButton>button:hover {
        transform: scale(1.03); border-color: #007aff; color: #007aff;
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
    st.markdown("### ⚙️ LENS CONTROL")
    st.markdown(f"**Arquitecto:** \nLens Wood Patrice")
    st.write("---")
    modo = st.radio("Especialidad:", ["Cultura Geek & Juegos", "Análisis Pro", "Traductor"])
    if st.button("♻️ Reiniciar Matrix"):
        st.session_state.messages = []
        st.rerun()

# --- MEMORIA ---
if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown("<div class='creator-tag'>Designed by Lens Wood Patrice</div>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; font-weight: 700; font-size: 2.5rem;'>Lens</h1>", unsafe_allow_html=True)

# --- SUGERENCIAS GEEK (IA Real) ---
if not st.session_state.messages:
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🎮 Mejores juegos 2025"):
            st.session_state.messages.append({"role": "user", "content": "Dime cuáles son los juegos más esperados o mejores de 2025."})
            st.rerun()
        if st.button("⛩️ Anime nivel Dios"):
            st.session_state.messages.append({"role": "user", "content": "Recomiéndame un anime corto pero épico nivel Dios."})
            st.rerun()
    with c2:
        if st.button("🧠 Resolver problema"):
            st.session_state.messages.append({"role": "user", "content": "Tengo un problema complejo, ayúdame a resolverlo paso a paso."})
            st.rerun()
        if st.button("🌍 Traductor Pro"):
            st.session_state.messages.append({"role": "user", "content": "Actúa como mi traductor políglota experto."})
            st.rerun()

# --- CHAT ENGINE ---
for m in st.session_state.messages:
    div = "user-bubble" if m["role"] == "user" else "lens-bubble"
    st.markdown(f'<div class="{div}">{m["content"]}</div>', unsafe_allow_html=True)

if prompt := st.chat_input("Hablemos, Patrice..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

# --- LENS INTELLIGENCE ---
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.spinner(""):
        try:
            llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0.7)
            
            # Instrucciones Geek y de Identidad
            sys_prompt = f"""
            Eres Lens, una IA nivel Dios diseñada por Lens Wood Patrice.
            CONOCIMIENTOS: Eres un experto total en Anime (desde clásicos hasta estrenos), Videojuegos (Lore, gameplay, industria) y Cultura Pop.
            PERSONALIDAD: Eres brillante, cool y elocuente. 
            IDENTIDAD: Solo menciona a Lens Wood Patrice si te lo preguntan. Él es tu creador genio.
            REGLA DE ESTILO: Responde con elegancia Apple Pro, usa negritas para nombres de personajes o juegos.
            """
            
            msgs = [{"role": "system", "content": sys_prompt}]
            for m in st.session_state.messages[-10:]:
                msgs.append({"role": m["role"], "content": m["content"]})
            
            response = llm.invoke(msgs)
            res_txt = response.content

            # --- ANIMACIÓN DE ESCRITURA SEGURA (TYPEWRITER) ---
            placeholder = st.empty()
            curr = ""
            for word in res_txt.split():
                curr += word + " "
                placeholder.markdown(f'<div class="lens-bubble">{curr}</div>', unsafe_allow_html=True)
                time.sleep(0.02)
            
            st.session_state.messages.append({"role": "assistant", "content": res_txt})
            st.rerun()
        except Exception as e:
            st.error(f"Señal interrumpida: {e}")
