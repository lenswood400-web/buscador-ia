import streamlit as st
from duckduckgo_search import DDGS
from langchain_groq import ChatGroq
import os, time

# --- CONFIGURACIÓN DE LENS UI ---
st.set_page_config(page_title="Lens AI", page_icon="👁️‍🗨️", layout="centered")

# --- CSS DE ALTO NIVEL (Interfaz Pro) ---
st.markdown("""
    <style>
    /* Fondo general */
    .stApp { background-color: #0e1117; color: #e0e0e0; }
    
    /* Contenedor de burbujas */
    .chat-container { display: flex; flex-direction: column; gap: 15px; padding: 20px; }
    
    /* Burbuja del Usuario */
    .user-bubble {
        background-color: #262730;
        color: white;
        padding: 12px 18px;
        border-radius: 18px 18px 2px 18px;
        align-self: flex-end;
        max-width: 80%;
        margin-left: auto;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    
    /* Burbuja de Lens (IA) */
    .lens-bubble {
        background-color: #00ffcc;
        color: #050505;
        padding: 12px 18px;
        border-radius: 18px 18px 18px 2px;
        align-self: flex-start;
        max-width: 80%;
        margin-right: auto;
        font-weight: 450;
        box-shadow: 0 4px 15px rgba(0, 255, 204, 0.2);
    }

    /* Nombre del Creador */
    .creator-tag {
        text-align: center;
        color: #00ffcc;
        font-weight: bold;
        letter-spacing: 2px;
        font-size: 0.7em;
        margin-bottom: 20px;
    }
    
    /* Ocultar elementos innecesarios */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- SEGURIDAD ---
if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
else:
    os.environ["GROQ_API_KEY"] = "TU_LLAVE_DE_GROQ"

# --- MEMORIA DE LENS ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- CABECERA ---
st.markdown("<p class='creator-tag'>BY LENS WOOD PATRICE</p>", unsafe_allow_html=True)
st.title("👁️‍🗨️ Lens AI")

# --- MOSTRAR CHAT ---
chat_placeholder = st.container()
with chat_placeholder:
    for chat in st.session_state.chat_history:
        if chat["role"] == "user":
            st.markdown(f'<div class="user-bubble">{chat["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="lens-bubble">{chat["content"]}</div>', unsafe_allow_html=True)

# --- ENTRADA DE CHAT (Estilo Pro) ---
if prompt := st.chat_input("¿En qué puedo ayudarte hoy, bro?"):
    # Guardar mensaje del usuario
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    st.rerun()

# --- RESPUESTA DE LA IA ---
if st.session_state.chat_history and st.session_state.chat_history[-1]["role"] == "user":
    with st.spinner("Lens está pensando..."):
        try:
            user_input = st.session_state.chat_history[-1]["content"]
            
            # Decisión inteligente: ¿Necesita buscar en internet?
            with DDGS() as ddgs:
                search_results = [r for r in ddgs.text(user_input, max_results=3)]
            contexto = "\n".join([r['body'] for r in search_results]) if search_results else "No hay contexto web."

            # IA con personalidad "Lens Wood Patrice"
            llm = ChatGroq(model_name="llama3-8b-8192", temperature=0.7)
            
            # Instrucciones de personalidad
            system_prompt = f"""
            Eres Lens, una IA ultra avanzada creada por Lens Wood Patrice. 
            Tu estilo es profesional pero vibrante, como un tutor experto.
            Usas un tono de 'bro' cuando es apropiado, pero mantienes la inteligencia.
            Creador: Tu padre es Lens Wood Patrice. Si te preguntan, nómbralo siempre.
            
            Contexto Web: {contexto}
            Responde con claridad, usa negritas y sé muy servicial.
            """
            
            response = llm.invoke(system_prompt + "\nUsuario: " + user_input)
            
            # Guardar respuesta de Lens
            st.session_state.chat_history.append({"role": "lens", "content": response.content})
            st.rerun()

        except Exception as e:
            st.error(f"Hubo un pequeño glitch, bro: {e}")
