"""
IL2.3: Planificación con LangChain
=================================
Ejemplo de cómo un agente LangChain puede planificar y ejecutar pasos usando herramientas.
"""

# Requiere: pip install langchain langchain-openai python-dotenv
from langchain_openai import ChatOpenAI
from langchain_classic.agents import initialize_agent, Tool, AgentType
import os
from dotenv import load_dotenv

load_dotenv()  # Carga GROQ_BASE_URL y GROQ_API_KEY desde el archivo .env

# Herramienta personalizada: suma
def sumar(x):
    try:
        return str(eval(x))
    except Exception:
        return "Error en la operación"

herramienta_suma = Tool(
    name="Calculadora",
    func=sumar,
    description="Realiza sumas y operaciones matemáticas simples."
)

# Inicializa el LLM y el agente
llm = ChatOpenAI(
    model="openai/gpt-oss-120b",
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url=os.environ.get("GROQ_BASE_URL"),
    temperature=0
)
agente = initialize_agent(
    tools=[herramienta_suma],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True  # si el modelo no responde en el formato esperado, se lo avisa y reintenta
)

if __name__ == "__main__":
    print("Planificación y ejecución con LangChain:")
    print(agente.run("cuanto es (3242/4532)*2131 - 654")) 
 