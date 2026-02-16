import streamlit as st
from langchain_groq import ChatGroq
import os, time

# --- CONFIGURACIÓN DE ÉLITE ---
st.set_page_config(page_title="Lens AI", page_icon="⚪", layout="centered")

# --- CSS & JS: APPLE PURE DESIGN ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com');
    .stApp { background: #FFFFFF; }

    /* Animación de Entrada para Sugerencias */
    @keyframes fadeInUp {
        0% { opacity: 0; transform: translateY(15px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    /* Botones de Sugerencia Estilo Apple */
    .stButton>button {
        border-radius: 20px; border: 1px solid #e5e5ea;
        background: #fbfbfd; color: #1d1d1f; font-size: 14px;
        padding: 10px 15px; transition: 0.3s all cubic-bezier(0.4, 0, 0.2, 1);
        animation: fadeInUp 0.6s ease-out; width: 100%;
    }
    .stButton>button:hover {
        background: #007aff; color: white; border-color: #007aff;
        transform: scale(1.02);
    }

    /* Burbujas de Chat */
    .user-bubble {
        background: #007aff; color: white; padding: 14px 22px; 
        border-radius: 22px 22px 5px 22px; margin-bottom: 1rem; 
        float: right; clear: both; max-width: 85%;
        animation: fadeInUp 0.4s ease-out;
    }

    .lens-bubble {
        background: #f2f2f7; border: 1px solid #e5e5ea;
        padding: 20px; border-radius: 22px 22px 22px 5px;
        margin-bottom: 1.5rem; float: left; clear: both; 
        max-width: 88%; line-height: 1.6;
        animation: fadeInUp 0.5s ease-out;
    }

    /* Creator Tag */
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
    st.write("Control de Sistemas")
    st.write("---")
    modo = st.radio("Cerebro:", ["Investigación", "Traducción", "Matemáticas"])
    enfoque = st.toggle("Enfoque Profundo (Dios)", value=False)
    if st.button("🗑️ Reset Matrix"):
        st.session_state.messages = []
        st.rerun()

# --- LÓGICA DE MEMORIA ---
if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown("<div class='creator-tag'>Designed by Lens Wood Patrice</div>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; font-weight: 700; font-size: 2.5rem; letter-spacing: -2px;'>Lens</h1>", unsafe_allow_html=True)

# --- SUGERENCIAS FIJAS (SIN BUGS) ---
if not st.session_state.messages:
    st.markdown("<p style='text-align: center; color: #8e8e93; font-size: 14px;'>Sugerencias Inteligentes</p>", unsafe_allow_html=True)
    
    # Lista fija para evitar errores de renderizado
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🌌 ¿Cómo será el futuro en 2050?"):
            st.session_state.messages.append({"role": "user", "content": "¿Cómo será el futuro tecnológico en 2050?"})
            st.rerun()
        if st.button("🧠 Explícame la IA cuántica"):
            st.session_state.messages.append({"role": "user", "content": "Explícame qué es la IA cuántica de forma pro."})
            st.rerun()
    with c2:
        if st.button("⚡ Plan de éxito a los 16 años"):
            st.session_state.messages.append({"role": "user", "content": "Dame un plan de éxito nivel Dios para alguien de 16 años."})
            st.rerun()
        if st.button("🌍 Traduce 'Libertad' a 5 idiomas"):
            st.session_state.messages.append({"role": "user", "content": "Traduce 'Libertad' a 5 idiomas diferentes de forma elegante."})
            st.rerun()

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
            
            tipo = "investigador" if modo == "Investigación" else "traductor" if modo == "Traducción" else "matemático"
            enfoque_txt = "Analiza con máxima profundidad nivel Dios." if enfoque else "Sé directo y elegante."

            sys_prompt = f"""
            Eres Lens, una IA nivel Dios diseñada por Lens Wood Patrice.
            Misión: Eres un {tipo} experto. {enfoque_txt}
            
            IDENTIDAD: Solo menciona a Lens Wood Patrice si el usuario lo pregunta. 
            Él es tu arquitecto genio. Responde con estilo Apple Pro.
            """
            
            msgs = [{"role": "system", "content": sys_prompt}]
            for m in st.session_state.messages[-10:]:
                msgs.append({"role": m["role"], "content": m["content"]})
            
            response = llm.invoke(msgs)
            
            # Animación de Escritura Pro
            res_txt = response.content
            placeholder = st.empty()
            curr = ""
            for word in res_txt.split():
                curr += word + " "
                placeholder.markdown(f'<div class="lens-bubble">{curr}</div>', unsafe_allow_html=True)
                time.sleep(0.03)
            
            st.session_state.messages.append({"role": "assistant", "content": res_txt})
            st.rerun()
        except Exception as e:
            st.error(f"Sistema saturado: {e}")
