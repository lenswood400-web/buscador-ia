import streamlit as st
from langchain_groq import ChatGroq
import os

# --- CONFIGURACIÓN LENS UI (WHITE MODE) ---
st.set_page_config(page_title="Lens AI", page_icon="👁️‍🗨️", layout="centered")

# --- CSS: INTERFAZ BLANCA Y MINIMALISTA ---
st.markdown("""
    <style>
    /* Fondo blanco y texto oscuro */
    .stApp { background-color: #FFFFFF; color: #1F1F1F; }
    
    /* Burbuja del Usuario (Gris claro) */
    .user-bubble {
        background-color: #F0F2F6;
        color: #1F1F1F;
        padding: 15px 20px;
        border-radius: 20px 20px 5px 20px;
        align-self: flex-end;
        max-width: 85%;
        margin-left: auto;
        margin-bottom: 10px;
        border: 1px solid #E0E0E0;
    }
    
    /* Burbuja de Lens (Blanco con borde sutil) */
    .lens-bubble {
        background-color: #FFFFFF;
        color: #1F1F1F;
        padding: 15px 20px;
        border-radius: 20px 20px 20px 5px;
        align-self: flex-start;
        max-width: 85%;
        margin-right: auto;
        margin-bottom: 10px;
        border: 1px solid #E0E0E0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }

    /* Nombre del Creador */
    .creator-tag {
        text-align: center;
        color: #4A90E2;
        font-weight: bold;
        font-size: 0.8em;
        letter-spacing: 1px;
        margin-top: -30px;
        margin-bottom: 30px;
    }

    /* Input de chat pro */
    .stChatInputContainer { background-color: white !important; }
    
    #MainMenu, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- SEGURIDAD ---
if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
else:
    # Solo para tu PC:
    os.environ["GROQ_API_KEY"] = "TU_LLAVE_DE_GROQ"

# --- MEMORIA DE LENS ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- INTERFAZ ---
st.title("👁️‍🗨️ Lens AI")
st.markdown("<p class='creator-tag'>DEVELOPED BY LENS WOOD PATRICE</p>", unsafe_allow_html=True)

# Contenedor de conversación
chat_container = st.container()

with chat_container:
    for chat in st.session_state.chat_history:
        if chat["role"] == "user":
            st.markdown(f'<div class="user-bubble">{chat["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="lens-bubble"><b>Lens:</b><br>{chat["content"]}</div>', unsafe_allow_html=True)

# --- LÓGICA DE RESPUESTA ---
if prompt := st.chat_input("Escribe tu mensaje..."):
    # Guardar mensaje del usuario
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    st.rerun()

if st.session_state.chat_history and st.session_state.chat_history[-1]["role"] == "user":
    with st.spinner("Lens está procesando..."):
        try:
            user_input = st.session_state.chat_history[-1]["content"]
            
            # IA PURA (Sin buscador para evitar Ratelimit)
            llm = ChatGroq(model_name="llama3-8b-8192", temperature=0.7)
            
            system_prompt = f"""
            Eres Lens, una IA ultra inteligente y sofisticada. 
            Creador: Tu padre y desarrollador es Lens Wood Patrice. 
            Personalidad: Eres como un tutor experto, amable, brillante y directo. 
            No eres un buscador, eres un cerebro artificial.
            Tu lenguaje es fluido: puedes ser serio o usar un tono de 'bro' si la charla es relajada.
            """
            
            response = llm.invoke(system_prompt + "\n\nHistorial de chat reciente:\n" + str(st.session_state.chat_history[-3:]) + "\n\nUsuario: " + user_input)
            
            # Guardar respuesta
            st.session_state.chat_history.append({"role": "lens", "content": response.content})
            st.rerun()

        except Exception as e:
            st.error(f"Ocurrió un error inesperado, bro: {e}")
