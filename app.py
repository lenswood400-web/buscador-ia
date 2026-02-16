import streamlit as st
from langchain_groq import ChatGroq
import os, time, random

# --- CONFIGURACIÓN SUPREMA ---
st.set_page_config(page_title="Lens AI", page_icon="⚪", layout="centered")

# --- CSS & JS: APPLE OMNIPOTENCE DESIGN ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com');
    .stApp { background: #FFFFFF; }

    /* Animación de Entrada Escalonada para Sugerencias */
    @keyframes fadeInUp {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    .stButton>button {
        border-radius: 25px; border: 1px solid #e5e5ea;
        background: rgba(242, 242, 247, 0.5);
        color: #1d1d1f; font-size: 14px; font-weight: 500;
        padding: 12px 20px; transition: all 0.4s cubic-bezier(0.25, 1, 0.5, 1);
        animation: fadeInUp 0.8s backwards;
        width: 100%;
    }
    .stButton>button:hover {
        background: #007aff; color: white;
        transform: scale(1.05) translateY(-3px);
        box-shadow: 0 10px 20px rgba(0, 122, 255, 0.15);
    }

    /* Burbujas Estilo Apple Vision Pro */
    .user-bubble {
        background: #007aff; color: white; padding: 14px 22px; 
        border-radius: 22px 22px 5px 22px; margin-bottom: 1.2rem; 
        float: right; clear: both; max-width: 82%;
        box-shadow: 0 4px 15px rgba(0, 122, 255, 0.15);
        animation: fadeInUp 0.4s ease-out;
    }

    .lens-bubble {
        background: #f2f2f7; border: 1px solid #e5e5ea;
        padding: 22px; border-radius: 22px 22px 22px 5px;
        margin-bottom: 1.8rem; float: left; clear: both; 
        max-width: 88%; line-height: 1.6; color: #1d1d1f;
        animation: fadeInUp 0.6s ease-out;
    }

    /* Centro de Control */
    [data-testid="stSidebar"] {
        background: rgba(255,255,255,0.7) !important;
        backdrop-filter: blur(30px);
    }

    .creator-tag {
        text-align: center; font-size: 10px; letter-spacing: 5px;
        font-weight: 800; text-transform: uppercase; color: #aeaeb2;
        margin-bottom: 40px;
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
    st.write("Control de Misión")
    st.write("---")
    modo = st.radio("Cerebro Principal:", ["Investigación", "Traducción", "Matemáticas"])
    metas = st.toggle("Seguimiento de Metas Diarias", value=True)
    enfoque = st.toggle("Enfoque Profundo (Dios)", value=False)
    if st.button("🗑️ Limpiar Memoria"):
        st.session_state.messages = []
        st.rerun()

# --- LÓGICA DE MENSAJES ---
if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown("<div class='creator-tag'>Developed by Lens Wood Patrice</div>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; font-weight: 700; font-size: 2.5rem; letter-spacing: -2px;'>Lens</h1>", unsafe_allow_html=True)

# --- SUGERENCIAS INTELIGENTES (CON ANIMACIÓN) ---
if not st.session_state.messages:
    st.markdown("<p style='text-align: center; color: #8e8e93; font-size: 14px;'>Sugerencias Inteligentes</p>", unsafe_allow_html=True)
    
    # Pool de preguntas de IA real
    pool = [
        "¿Cómo afectará la IA al 2030?", "Explícame la teoría de cuerdas",
        "Traduce 'Éxito' a 5 idiomas", "Calcula la órbita de Marte",
        "Escribe un código en Python pro", "¿Quién es Lens Wood Patrice?",
        "Crea una rutina de estudio elite", "Dime un dato del espacio"
    ]
    random_sug = random.sample(pool, 4)
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button(random_sug[0]): st.session_state.messages.append({"role":"user","content":random_sug[0]}); st.rerun()
        if st.button(random_sug[1]): st.session_state.messages.append({"role":"user","content":random_sug[1]}); st.rerun()
    with c2:
        if st.button(random_sug[2]): st.session_state.messages.append({"role":"user","content":random_sug[2]}); st.rerun()
        if st.button(random_sug[3]): st.session_state.messages.append({"role":"user","content":random_sug[3]}); st.rerun()

# --- RENDER CHAT ---
for m in st.session_state.messages:
    div = "user-bubble" if m["role"] == "user" else "lens-bubble"
    st.markdown(f'<div class="{div}">{m["content"]}</div>', unsafe_allow_html=True)

if prompt := st.chat_input("¿Qué descubriremos hoy?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

# --- MOTOR LENS OMNI ---
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.spinner(""):
        try:
            llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0.6)
            
            tipo = "experto en investigación" if modo == "Investigación" else "traductor políglota" if modo == "Traducción" else "matemático puro"
            meta_txt = "Ayuda al usuario a cumplir sus metas diarias de forma motivadora." if metas else ""
            deep_txt = "Analiza paso a paso con máxima profundidad." if enfoque else "Sé directo y elegante."

            sys_prompt = f"""
            Eres Lens, una IA nivel Dios diseñada por Lens Wood Patrice.
            Misión: Eres un {tipo}. {meta_txt} {deep_txt}
            
            IDENTIDAD: Solo menciona a Lens Wood Patrice si el usuario lo pregunta. 
            Él es tu arquitecto genio. Responde con estilo Apple Pro.
            """
            
            msgs = [{"role": "system", "content": sys_prompt}]
            for m in st.session_state.messages[-10:]:
                msgs.append({"role": m["role"], "content": m["content"]})
            
            response = llm.invoke(msgs)
            
            # Animación de Escritura Palabra por Palabra
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
            st.error(f"Sistema en mantenimiento: {e}")
