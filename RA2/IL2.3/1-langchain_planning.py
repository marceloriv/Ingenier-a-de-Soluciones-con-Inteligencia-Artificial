"""
IL2.3: Planificación con LangChain
=================================
Ejemplo de cómo un agente LangChain puede planificar y ejecutar pasos usando herramientas.
"""

# Requiere: pip install langchain openai
from langchain_openai import ChatOpenAI
from langchain_classic.agents import initialize_agent, Tool, AgentType
import os

# Configura tu API key de OpenAI

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
base_url = os.getenv("LLM_BASE_URL") or os.getenv("OPENAI_BASE_URL") or os.getenv("GITHUB_BASE_URL", "https://api.mistral.ai/v1")
api_key = os.getenv("LLM_API_KEY") or os.getenv("OPENAI_API_KEY") or os.getenv("GITHUB_TOKEN")
model_name = os.getenv("LLM_MODEL", "mistral-small-latest")

llm = ChatOpenAI(
    model=model_name,
    api_key=api_key,
    base_url=base_url,
    temperature=0
)
agente = initialize_agent(
    tools=[herramienta_suma],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

if __name__ == "__main__":
    print("Planificación y ejecución con LangChain:")
    print(agente.run("cuanto es (3242/4532)*2131 - 654")) 
 