"""
IL2.3: Planificación Básica con LangChain
========================================
Ejemplo de cómo un agente LangChain puede planificar y ejecutar pasos simples usando una herramienta.
"""

# Requiere: pip install langchain langchain-classic langchain-openai openai python-dotenv
import os

from dotenv import load_dotenv
from langchain_classic.agents import AgentType, Tool, initialize_agent
from langchain_openai import ChatOpenAI

load_dotenv()

# Verificar que tenemos las bibliotecas correctas
print("OpenAI library version:", __import__("openai").__version__)
print("Python version:", __import__("sys").version)


# Herramienta personalizada: pasos para preparar café
def pasos_cafe(_):
    return "1. Calentar agua\n2. Añadir café al filtro\n3. Verter agua caliente\n4. Servir en una taza"


herramienta_cafe = Tool(
    name="PasosCafé",
    func=pasos_cafe,
    description="Devuelve los pasos para preparar café.",
)

# Configuración del cliente con variables de entorno para Groq Models
base_url = os.environ.get("GROQ_BASE_URL")
api_key = os.environ.get("GROQ_API_KEY")
model_name = "openai/gpt-oss-120b"

llm = ChatOpenAI(
    model=model_name,
    api_key=api_key,
    base_url=base_url,
    temperature=0,
)
agente = initialize_agent(
    tools=[herramienta_cafe],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True,
)

if __name__ == "__main__":
    print("Planificación con LangChain:")
    print(
        agente.invoke({"input": "¿Cuáles son los pasos para preparar café?"})["output"]
    )
