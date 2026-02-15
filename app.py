import streamlit as st
from duckduckgo_search import DDGS
from langchain_groq import ChatGroq
import os
import time

st.set_page_config(page_title="Seeke AI", page_icon="🚀")

# --- SEGURIDAD ---
if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
else:
    os.environ["GROQ_API_KEY"] = "TU_LLAVE_DE_GROQ_AQUI"

st.title("🚀 Mi Buscador IA (Anti-Bloqueo)")

query = st.text_input("¿Qué quieres investigar?", placeholder="Escribe aquí...")

if query:
    with st.spinner("Buscando con cuidado para no ser bloqueado..."):
        try:
            # Esperamos 1 segundo para que DuckDuckGo no se enoje
            time.sleep(1) 
            
            with DDGS() as ddgs:
                # Bajamos a 3 resultados para ser más discretos
                search_results = [r for r in ddgs.text(query, max_results=3)]
            
            if not search_results:
                st.warning("No encontré resultados. Intenta con otra palabra.")
            else:
                contexto = "\n".join([f"Título: {r['title']}\nInfo: {r['body']}" for r in search_results])

                llm = ChatGroq(model_name="llama3-8b-8192", temperature=0.3)
                prompt = f"Eres un buscador profesional. Responde a: {query} usando: {contexto}"
                
                respuesta = llm.invoke(prompt)
                
                st.markdown("### 📝 Respuesta")
                st.info(respuesta.content)

        except Exception as e:
            if "Ratelimit" in str(e):
                st.error("⚠️ ¡DuckDuckGo nos pidió un respiro! Espera 30 segundos y vuelve a intentar.")
            else:
                st.error(f"Error: {e}")
