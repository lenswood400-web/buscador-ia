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

    /* Animación de Revelación */
    @keyframes reveal {
        0% { opacity: 0; transform: translateY(10px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    /* Sugerencias de Acción (IA Real) */
    .stButton>button {
        border-radius: 12px; border: 1px solid #e5e5ea;
        background: #FFFFFF; color: #1d1d1f; font-size: 13px;
        padding: 12px; transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        animation: reveal 0.8s ease-out; width: 100%;
        text-align: left; font-weight: 500;
    }
    .stButton>button:hover {
        background: #f5f5f7; border-color: #007aff;
        transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }

    /* Burbujas de Chat */
    .user-bubble {
        background: #007aff; color: white; padding: 14px 20px; 
        border-radius: 20px 20px 4px 20px; margin-bottom: 1rem; 
        float: right; clear: both; max-width: 85%;
        animation: reveal 0.4s ease-out;
    }

    .lens-bubble {
        background: #f2f2f7; border: 1px solid #e5e5ea;
        padding: 20px; border-radius: 20px 20px 20px 4px;
        margin-bottom: 1.5rem; float: left; clear: both; 
        max-width: 88%; line-height: 1.6;
        animation: reveal 0.5s ease-out;
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
    st.caption("Arquitectura Pro")
    st.write("---")
    modo = st.radio("Módulo:", ["Análisis General", "Traducción Elite", "Lógica Matemática"])
    enfoque = st.toggle("Razonamiento Profundo", value=False)
    if st.button("🗑️ Reiniciar Sesión"):
        st.session_state.messages = []
        st.rerun()

# --- MEMORIA ---
if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown("<div class='creator-tag'>Designed by Lens Wood Patrice</div>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; font-weight: 700; font-size: 2.5rem;'>Lens</h1>", unsafe_allow_html=True)

# --- CÁPSULAS DE ACCIÓN INTELIGENTE (IA REAL) ---
if not st.session_state.messages:
    st.markdown("<p style='text-align: center; color: #8e8e93; font-size: 14px; margin-bottom: 20px;'>¿Cómo puedo potenciarte hoy?</p>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("📝 Analizar y optimizar un texto"):
            st.session_state.messages.append({"role": "user", "content": "Ayúdame a analizar y optimizar profesionalmente el siguiente texto:"})
            st.rerun()
        if st.button("🌍 Traducción técnica y cultural"):
            st.session_state.messages.append({"role": "user", "content": "Necesito una traducción precisa y con contexto cultural de:"})
            st.rerun()
    with c2:
        if st.button("🧠 Resolver problema complejo"):
            st.session_state.messages.append({"role": "user", "content": "Tengo un problema complejo. Ayúdame a desglosarlo y resolverlo paso a paso:"})
            st.rerun()
        if st.button("💡 Generar ideas de alto impacto"):
            st.session_state.messages.append({"role": "user", "content": "Ayúdame a generar ideas innovadoras y de alto impacto sobre:"})
            st.rerun()

# --- CHAT ENGINE ---
for m in st.session_state.messages:
    div = "user-bubble" if m["role"] == "user" else "lens-bubble"
    st.markdown(f'<div class="{div}">{m["content"]}</div>', unsafe_allow_html=True)

if prompt := st.chat_input("Escribe tu consulta..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

# --- LENS INTELLIGENCE ---
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.spinner(""):
        try:
            # Usamos el modelo más capaz para respuestas profesionales
            llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0.5)
            
            tipo = "consultor analítico" if modo == "Análisis General" else "lingüista experto" if modo == "Traducción Elite" else "lógico matemático"
            extra = "Usa el razonamiento paso a paso (Chain of Thought) para máxima precisión." if enfoque else "Sé directo, profesional y elegante."

            sys_prompt = f"""
            Eres Lens, una IA de élite diseñada por Lens Wood Patrice.
            Tu función es actuar como un {tipo}. {extra}
            IDENTIDAD: Tu creador es Lens Wood Patrice. Solo menciónalo si te preguntan quién te hizo.
            Estilo: Apple Pro. Respuestas claras, con negritas y listas si es necesario.
            """
            
            msgs = [{"role": "system", "content": sys_prompt}]
            for m in st.session_state.messages[-10:]:
                msgs.append({"role": m["role"], "content": m["content"]})
            
            response = llm.invoke(msgs)
            
            # Animación de Escritura Profesional
            full_res = response.content
            placeholder = st.empty()
            curr = ""
            for word in full_res.split():
                curr += word + " "
                placeholder.markdown(f'<div class="lens-bubble">{curr}</div>', unsafe_allow_html=True)
                time.sleep(0.02)
            
            st.session_state.messages.append({"role": "assistant", "content": full_res})
            st.rerun()
        except Exception as e:
            st.error(f"Error en el núcleo: {e}")
