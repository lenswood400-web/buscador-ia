import streamlit as st
from duckduckgo_search import DDGS
from langchain_groq import ChatGroq
import os
import time
import requests
import io
from PIL import Image

# --- CONFIGURACIÓN LENS ULTIMATE ---
st.set_page_config(page_title="Lens AI | Multimodal", page_icon="👁️‍🗨️", layout="wide")

# Estilo Cyber-Visionary
st.markdown("""
    <style>
    .stApp { background-color: #030303; color: #ffffff; }
    .lens-chat { background: #0a0a0a; padding: 20px; border-radius: 15px; border-left: 5px solid #00ffcc; margin-bottom: 10px; }
    .user-chat { background: #111; padding: 20px; border-radius: 15px; border-right: 5px solid #555; margin-bottom: 10px; }
    .stButton>button { width: 100%; border-radius: 20px; background: #00ffcc; color: black; font-weight: bold; border: none; }
    .stTextInput>div>div>input { border-radius: 20px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- SEGURIDAD ---
if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
else:
    os.environ["GROQ_API_KEY"] = "TU_LLAVE_DE_GROQ_AQUI"

# --- FUNCION: GENERADOR DE IMÁGENES (FREE API) ---
def generate_image(prompt):
    # Usamos un modelo de Hugging Face gratuito para Lens
    API_URL = "https://api-inference.huggingface.co"
    headers = {"Authorization": f"Bearer {st.secrets.get('HF_TOKEN', 'opcional')}"}
    
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    return response.content

# --- INICIALIZAR MEMORIA ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- INTERFAZ LATERAL ---
with st.sidebar:
    st.title("👁️‍🗨️ Lens Control")
    st.markdown(f"**Creador:** \nLens Wood Patrice")
    st.write("---")
    mode = st.radio("Modo de Lens:", ["Chat & Búsqueda", "Generador de Arte"])
    if st.button("Limpiar Memoria"):
        st.session_state.messages = []
        st.rerun()

st.title("👁️‍🗨️ Lens AI")
st.caption("Powered by Llama 3 & Stable Diffusion | DNA: Lens Wood Patrice")

# --- LÓGICA DE MODO ---
if mode == "Chat & Búsqueda":
    # Mostrar historial
    for m in st.session_state.messages:
        role_class = "lens-chat" if m["role"] == "lens" else "user-chat"
        st.markdown(f'<div class="{role_class}"><b>{m["role"].upper()}:</b><br>{m["content"]}</div>', unsafe_allow_html=True)

    if prompt := st.chat_input("¿Qué investigamos hoy, bro?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.rerun()

    # Procesar última pregunta
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        with st.spinner("Lens está enfocando..."):
            try:
                user_query = st.session_state.messages[-1]["content"]
                
                # Búsqueda Web
                with DDGS() as ddgs:
                    search = [r for r in ddgs.text(user_query, max_results=3)]
                contexto = "\n".join([r['body'] for r in search])

                # IA con Personalidad
                llm = ChatGroq(model_name="llama3-8b-8192", temperature=0.7)
                sys_msg = f"Eres Lens, IA creada por Lens Wood Patrice. Eres cool, hablas como tutor bro. Info: {contexto}"
                
                res = llm.invoke(sys_msg + user_query)
                st.session_state.messages.append({"role": "lens", "content": res.content})
                st.rerun()
            except Exception as e:
                st.error(f"Hubo un glitch: {e}")

else: # MODO GENERADOR DE ARTE
    st.subheader("🎨 Generador de Imágenes de Lens")
    art_prompt = st.text_input("Describe la imagen que Lens debe crear:")
    if st.button("Crear Obra Maestra"):
        with st.spinner("Lens está dibujando..."):
            image_bytes = generate_image(art_prompt)
            image = Image.open(io.BytesIO(image_bytes))
            st.image(image, caption=f"Arte creado por Lens para {art_prompt}")
            st.success("¡Listo bro! Aquí tienes tu imagen.")

