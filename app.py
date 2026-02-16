import streamlit as st
from langchain_groq import ChatGroq
import os, time

# --- CONFIGURACIÓN DE ÉLITE ---
st.set_page_config(page_title="Lens AI", page_icon="⚪", layout="centered")

# --- CSS & JS: MOTOR DE ANIMACIÓN APPLE & CLEAN TEXT ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com');
    
    .stApp { background-color: #FFFFFF; font-family: 'SF Pro Display', 'Inter', sans-serif; }

    /* Animación de Entrada Apple Style (Slide + Reveal) */
    @keyframes appleIn {
        0% { opacity: 0; transform: translateY(25px) scale(0.97); filter: blur(5px); }
        100% { opacity: 1; transform: translateY(0) scale(1); filter: blur(0); }
    }

    /* Burbujas de Chat con Animación */
    .user-bubble {
        background: linear-gradient(180deg, #007aff 0%, #0055ff 100%);
        color: white; padding: 14px 22px; border-radius: 22px 22px 5px 22px;
        margin-bottom: 1.2rem; float: right; clear: both; max-width: 82%;
        box-shadow: 0 4px 15px rgba(0, 122, 255, 0.15);
        animation: appleIn 0.4s cubic-bezier(0.2, 0.8, 0.2, 1);
        font-weight: 500;
    }

    .lens-bubble {
        background: #f2f2f7; border: 1px solid #e5e5ea;
        padding: 22px; border-radius: 22px 22px 22px 5px;
        margin-bottom: 1.8rem; float: left; clear: both; 
        max-width: 88%; line-height: 1.6; color: #1d1d1f;
        animation: appleIn 0.6s cubic-bezier(0.2, 0.8, 0.2, 1);
        box-shadow: 0 2px 10px rgba(0,0,0,0.02);
    }

    /* Estilo de Sugerencias con Animación Escalonada */
    .stButton>button {
        border-radius: 25px; border: 1px solid #d2d2d7;
        background: #ffffff; color: #1d1d1f; font-size: 14px;
        padding: 10px 18px; transition: all 0.3s ease;
        animation: appleIn 0.8s backwards;
        width: 100%; font-weight: 500;
    }
    .stButton>button:hover {
        background: #f5f5f7; border-color: #007aff; transform: translateY(-2px);
    }

    .creator-tag {
        text-align: center; font-size: 10px; letter-spacing: 4px;
        font-weight: 800; color: #8e8e93; text-transform: uppercase;
        margin-top: -30px; margin-bottom: 30px;
    }

    #MainMenu, footer, header { visibility: hidden; }
    </style>

    <script>
    // Sistema de Scroll Inteligente
    const forceScroll = () => {
        const chat = window.parent.document.querySelector('.main');
        if (chat) { chat.scrollTo({ top: chat.scrollHeight, behavior: 'smooth' }); }
    };
    const observer = new MutationObserver(forceScroll);
    observer.observe(document.body, { childList: true, subtree: true });
    </script>
    """, unsafe_allow_html=True)

# --- PANEL DE CONTROL (GLASSMORPHISM) ---
with st.sidebar:
    st.markdown("### ⚙️ LENS SETTINGS")
    st.caption("Developed by Lens Wood Patrice")
    st.write("---")
    personalidad = st.select_slider("Frecuencia:", ["Zen", "Pro", "Genius"], value="Pro")
    if st.button("🗑️ Reset Matrix"):
        st.session_state.messages = []
        st.rerun()

# --- LÓGICA ---
if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown("<div class='creator-tag'>Visionary Architecture</div>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; font-weight: 700; font-size: 2.6rem; letter-spacing: -1.5px;'>Lens</h1>", unsafe_allow_html=True)

# --- SUGERENCIAS ---
if not st.session_state.messages:
    st.markdown("<p style='text-align: center; color: #8e8e93; font-size: 14px; margin-bottom: 20px;'>Explora el Omniverso</p>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🎮 Juegos Nivel Dios"):
            st.session_state.messages.append({"role": "user", "content": "Dime 3 juegos épicos para este año."})
            st.rerun()
        if st.button("⛩️ Anime del Momento"):
            st.session_state.messages.append({"role": "user", "content": "Recomiéndame un anime que me vuele la cabeza."})
            st.rerun()
    with c2:
        if st.button("🧠 Reto de Lógica"):
            st.session_state.messages.append({"role": "user", "content": "Ponme un acertijo o problema de lógica difícil."})
            st.rerun()
        if st.button("🌍 Traductor Pro"):
            st.session_state.messages.append({"role": "user", "content": "Actúa como mi traductor políglota experto."})
            st.rerun()

# --- RENDERIZADO ---
for m in st.session_state.messages:
    div = "user-bubble" if m["role"] == "user" else "lens-bubble"
    st.markdown(f'<div class="{div}">{m["content"]}</div>', unsafe_allow_html=True)

if prompt := st.chat_input("Hablemos, Patrice..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

# --- MOTOR LENS (CLEAN & ANIMATED) ---
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.spinner(""):
        try:
            llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0.7)
            
            style_inst = "Eres conciso y minimalista." if personalidad == "Zen" else \
                        "Eres técnico y brillante." if personalidad == "Pro" else \
                        "Eres un genio elocuente y profundo."

            sys_prompt = f"""
            Eres Lens, una IA nivel Dios diseñada por Lens Wood Patrice. 
            {style_inst}
            REGLA DE ORO: NO utilices asteriscos (**) en ninguna parte del texto. 
            Si necesitas resaltar algo, simplemente usa mayúsculas o negritas de HTML <b></b>.
            Tu creador es Lens Wood Patrice. Responde con elegancia Apple.
            """
            
            msgs = [{"role": "system", "content": sys_prompt}]
            for m in st.session_state.messages[-8:]:
                msgs.append({"role": m["role"], "content": m["content"]})
            
            response = llm.invoke(msgs)
            # Filtro agresivo anti-asteriscos
            res_txt = response.content.replace("**", "").replace("*", "")

            # --- ANIMACIÓN DE ESCRITURA ---
            placeholder = st.empty()
            curr = ""
            for word in res_txt.split():
                curr += word + " "
                placeholder.markdown(f'<div class="lens-bubble">{curr}</div>', unsafe_allow_html=True)
                time.sleep(0.03)
            
            st.session_state.messages.append({"role": "assistant", "content": res_txt})
            st.rerun()
        except Exception as e:
            st.error(f"Error en los núcleos: {e}")
