"""
IL2.3: Planificación Básica con LangChain
========================================
Ejemplo de cómo un agente react en LangChain puede planificar y ejecutar pasos simples usando una herramienta.
"""

# Requiere: pip install langchain langchain-openai python-dotenv
from langchain_openai import ChatOpenAI
from langchain_classic.agents import initialize_agent, Tool, AgentType
import os
from dotenv import load_dotenv

load_dotenv()  # Carga GROQ_BASE_URL y GROQ_API_KEY desde el archivo .env

# Herramienta personalizada: pasos para preparar café
def pasos_cafe(_):
    return "1. Calentar agua\n2. Añadir café al filtro\n3. Verter agua caliente\n4. Servir en una taza"

herramienta_cafe = Tool(
    name="PasosCafé",
    func=pasos_cafe,
    description="Devuelve los pasos para preparar café."
)

# Inicializa el LLM y el agente
llm = ChatOpenAI(
    model="openai/gpt-oss-120b",
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url=os.environ.get("GROQ_BASE_URL"),
    temperature=0
)
agente = initialize_agent(
    tools=[herramienta_cafe],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

if __name__ == "__main__": #si el archivo se ejecuta directamente, 
    print("Planificación con LangChain:")
    print(agente.run("¿Cuáles son los pasos para preparar café?")) 