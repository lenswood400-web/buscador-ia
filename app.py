import streamlit as st
from duckduckgo_search import DDGS
from langchain_groq import ChatGroq
import os

# --- DISEÑO ---
st.set_page_config(page_title="Seeke AI", page_icon="🚀")

# --- SEGURIDAD ---
if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
else:
    os.environ["GROQ_API_KEY"] = "TU_LLAVE_DE_GROQ_AQUI"

st.title("🚀 Seeke AI: Buscador Directo")

query = st.text_input("¿Qué quieres investigar?", placeholder="Ej: Avances en robótica 2025")

if query:
    with st.spinner("Buscando en la web..."):
        try:
            # MÉTODO DIRECTO (Sin pasar por LangChain para buscar)
            with DDGS() as ddgs:
                # Buscamos los 5 mejores resultados
                search_results = [r for r in ddgs.text(query, max_results=5)]
            
            # Convertimos los resultados en un texto que la IA entienda
            contexto = ""
            for res in search_results:
                contexto += f"Título: {res['title']}\nCuerpo: {res['body']}\n\n"

            # CONEXIÓN CON IA
            llm = ChatGroq(model_name="llama3-8b-8192", temperature=0.3)
            
            prompt = f"""
            Eres un buscador profesional. Responde a la pregunta: {query}
            Usando esta información real encontrada en internet:
            {contexto}
            
            Da una respuesta estructurada y profesional.
            """
            
            respuesta = llm.invoke(prompt)
            
            # MOSTRAR RESULTADOS
            st.markdown("### 📝 Resultado del Análisis")
            st.info(respuesta.content)
            
            with st.expander("🌐 Ver fuentes encontradas"):
                for r in search_results:
                    st.write(f"**[{r['title']}]({r['href']})**")
                    st.write(r['body'])
                    st.write("---")
                
        except Exception as e:
            st.error(f"Error detectado: {e}")
            st.write("Intenta refrescar la página o revisar tu conexión.")
