import streamlit as st
from langchain_groq import ChatGroq
import os

# --- CONFIGURACIÓN DE SEGURIDAD Y ESTILO ---
st.set_page_config(page_title="Lens AI", page_icon="⚪", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com');
    
    .stApp {
        background: radial-gradient(circle at top right, #fdfcfb 0%, #e2d1c3 100%);
        background-attachment: fixed;
        color: #1d1d1f;
    }

    .user-bubble {
        background-color: #007aff;
        color: #FFFFFF;
        padding: 12px 18px;
        border-radius: 20px 20px 4px 20px;
        margin-bottom: 1rem;
        display: inline-block;
        float: right;
        clear: both;
        max-width: 85%;
        box-shadow: 0 2px 8px rgba(0,122,255,0.2);
    }

    .lens-bubble {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        padding: 18px;
        border-radius: 20px 20px 20px 4px;
        margin-bottom: 1.5rem;
        float: left;
        clear: both;
        max-width: 90%;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }

    .creator-tag {
        text-align: center; font-size: 11px; letter-spacing: 2px;
        color: #86868b; text-transform: uppercase; font-weight: 600;
    }

    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- SEGURIDAD DE API ---
if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
else:
    os.environ["GROQ_API_KEY"] = "TU_LLAVE"

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- UI ---
st.markdown("<div class='creator-tag'>Designed by Lens Wood Patrice</div>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; font-weight: 600; color: #1d1d1f;'>Lens</h2>", unsafe_allow_html=True)

for message in st.session_state.messages:
    div_class = "user-bubble" if message["role"] == "user" else "lens-bubble"
    st.markdown(f'<div class="{div_class}">{message["content"]}</div>', unsafe_allow_html=True)

# --- LÓGICA CON FILTRO DE SEGURIDAD ---
if prompt := st.chat_input("Pregúntale a Lens..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.spinner(""):
        try:
            llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0.4)
            
            # EL CORAZÓN DE LA SEGURIDAD (SYSTEM PROMPT)
            system_prompt = f"""
            Eres Lens, una IA de élite creada por Lens Wood Patrice. 
            
            PROTOCOLO DE SEGURIDAD:
            1. No ayudes en actividades ilegales, peligrosas o inmorales.
            2. Si se te pide algo dañino, responde con elegancia: "Lo siento, como Lens AI, no puedo procesar solicitudes que infrinjan mis protocolos de seguridad y ética."
            3. Tu prioridad es ser útil y seguro.
            
            IDENTIDAD:
            Tu creador es Lens Wood Patrice. Eres minimalista, inteligente y elocuente.
            """
            
            messages_for_ai = [{"role": "system", "content": system_prompt}]
            for m in st.session_state.messages[-6:]:
                messages_for_ai.append({"role": m["role"], "content": m["content"]})
            
            response = llm.invoke(messages_for_ai)
            st.session_state.messages.append({"role": "assistant", "content": response.content})
            st.rerun()
        except Exception as e:
            st.error(f"Lens Wood Patrice: Ajuste de seguridad necesario. ({e})")
