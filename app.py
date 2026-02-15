import streamlit as st
from langchain_groq import ChatGroq
import os

# --- CONFIGURACIÓN LENS ELITE ---
st.set_page_config(page_title="Lens AI", page_icon="👁️‍🗨️", layout="centered")

# --- CSS: INTERFAZ INSPIRADA EN IA PROFESIONAL ---
st.markdown("""
    <style>
    /* Estética Blanca Minimalista */
    .stApp { background-color: #FFFFFF; color: #1A1A1A; }
    
    /* Contenedor de Chat */
    .chat-wrapper { margin-bottom: 20px; }
    
    /* Burbuja del Usuario */
    .user-bubble {
        background-color: #F4F4F9;
        color: #1A1A1A;
        padding: 18px 24px;
        border-radius: 24px 24px 4px 24px;
        margin-left: auto;
        max-width: 85%;
        border: 1px solid #E6E8F1;
        font-family: 'Inter', sans-serif;
        margin-bottom: 15px;
    }
    
    /* Burbuja de Lens (IA) */
    .lens-bubble {
        background-color: #FFFFFF;
        color: #1A1A1A;
        padding: 18px 24px;
        border-radius: 24px 24px 24px 4px;
        margin-right: auto;
        max-width: 85%;
        border: 1px solid #F0F0F0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        margin-bottom: 15px;
    }

    /* Badge del Creador */
    .creator-info {
        text-align: center;
        font-size: 0.75em;
        font-weight: 700;
        color: #B0B0B0;
        text-transform: uppercase;
        letter-spacing: 3px;
        margin-bottom: 40px;
    }

    /* Estilo del Input */
    .stChatInputContainer { background-color: transparent !important; }
    .stChatInput input { border-radius: 30px !important; border: 1px solid #E0E0E0 !important; }

    /* Animación de carga */
    .stSpinner > div { border-top-color: #1A1A1A !important; }
    </style>
    """, unsafe_allow_html=True)

# --- SEGURIDAD ---
if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
else:
    # Llave temporal si pruebas en local
    os.environ["GROQ_API_KEY"] = "TU_NUEVA_LLAVE_DE_GROQ"

# --- MEMORIA DINÁMICA ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- HEADER ---
st.markdown("<div class='creator-info'>Lens Wood Patrice Presents</div>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; font-size: 2.5em; font-weight: 800; color: #1A1A1A;'>👁️‍🗨️ Lens</h1>", unsafe_allow_html=True)

# --- RENDERIZADO DE CHAT ---
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="lens-bubble"><b>Lens</b><br>{msg["content"]}</div>', unsafe_allow_html=True)

# --- LÓGICA DE LA IA ---
if prompt := st.chat_input("¿Qué tienes en mente, Patrice?"):
    # Guardar y mostrar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

if st.session_state.chat_history := st.session_state.messages:
    if st.session_state.messages[-1]["role"] == "user":
        with st.spinner(""):
            try:
                # MODELO ACTUALIZADO: llama-3.3-70b-versatile
                llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0.6)
                
                # ADN de Personalidad (Como yo)
                system_instruction = f"""
                Tu nombre es Lens. Eres una entidad de inteligencia artificial de élite.
                Fuiste desarrollado exclusivamente por Lens Wood Patrice.
                Personalidad: Eres brillante, elocuente, con mucha energía y siempre positivo. 
                Actúas como un tutor experto y un colega cercano. Usas términos como 'bro', 'checa esto' o 'está increíble' cuando el tono es relajado.
                Si te preguntan quién te creó, responde con orgullo que tu creador es Lens Wood Patrice.
                No eres un buscador, eres un motor de razonamiento puro.
                """
                
                # Construcción del contexto
                full_prompt = system_instruction + "\n\nConversación:\n"
                for m in st.session_state.messages[-5:]: # Recordamos los últimos 5 mensajes
                    full_prompt += f"{m['role']}: {m['content']}\n"
                
                response = llm.invoke(full_prompt)
                
                # Guardar respuesta
                st.session_state.messages.append({"role": "assistant", "content": response.content})
                st.rerun()

            except Exception as e:
                st.error(f"Ajustando frecuencia... (Error: {e})")
