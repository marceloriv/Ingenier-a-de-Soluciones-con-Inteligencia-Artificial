"""
IL2.3: Planificación con LangChain
=================================
Ejemplo de cómo un agente LangChain puede planificar y ejecutar pasos usando herramientas.
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


# Herramienta personalizada: suma
def sumar(x):
    try:
        return str(eval(x))
    except Exception:
        return "Error en la operación"


herramienta_suma = Tool(
    name="Calculadora",
    func=sumar,
    description="Útil para calcular operaciones matemáticas. Entrada: expresión matemática en formato texto (ej: 2+2).",
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
    tools=[herramienta_suma],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True,
)

if __name__ == "__main__":
    print("Planificación y ejecución con LangChain:")
    resultado = agente.invoke({"input": "cuanto es (3242/4532)*2131 - 654"})
    print(resultado["output"])
