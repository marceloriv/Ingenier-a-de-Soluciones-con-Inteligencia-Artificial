"""
IL2.3: Orquestación Multi-Agente con CrewAI
==========================================
Ejemplo de cómo dos agentes CrewAI colaboran para resolver una tarea.
"""

# Requiere: pip install crewai python-dotenv wikipedia
from crewai import Agent, Task, Crew
from crewai import LLM
from crewai.tools import tool
import wikipedia
import os
from dotenv import load_dotenv

load_dotenv()  # Carga GROQ_BASE_URL y GROQ_API_KEY desde el archivo .env

# LLM vía Groq, usando el proveedor "openai" de CrewAI con la URL de Groq.
# El primer "openai/" es el proveedor; "openai/gpt-oss-120b" es el modelo en Groq.
llm = LLM(
    model="openai/openai/gpt-oss-120b",
    api_key=os.environ["GROQ_API_KEY"],
    base_url=os.environ["GROQ_BASE_URL"],
    temperature=0
)

# Herramienta: búsqueda en Wikipedia (para que el investigador use datos reales y no invente)
wikipedia.set_lang("es")

@tool("Buscar en Wikipedia")
def buscar_wikipedia(tema: str) -> str:
    """Busca un tema en Wikipedia en español y devuelve un resumen. Usa nombres concretos."""
    try:
        return wikipedia.summary(tema, sentences=5)
    except Exception as e:
        return f"No se encontró información en Wikipedia: {e}"


# Agente 1: Investigador
investigador = Agent(
    role="Investigador",
    goal="Buscar información verificada sobre una capital del mundo",
    backstory="Eres experto en encontrar datos. Solo usas la información que obtienes con tu herramienta de Wikipedia; si no encuentras un dato, lo dices en vez de inventarlo.",
    tools=[buscar_wikipedia],
    llm=llm
)

# Agente 2: Redactor
redactor = Agent(
    role="Redactor",
    goal="Redactar una respuesta clara y breve",
    backstory="Eres especialista en explicar conceptos de forma sencilla.",
    llm=llm
)

# Tareas
tarea_investigar = Task(
    description="Busca en Wikipedia información sobre la capital de Francia",
    expected_output="5 datos clave sobre la capital de Francia, obtenidos de Wikipedia",
    agent=investigador
)

tarea_redactar = Task(
    description="Redacta una respuesta usando la información encontrada",
    expected_output="Una oracion con la informacion bien redactada",
    agent=redactor,
    context=[tarea_investigar]
)

# Crew (equipo)
crew = Crew(
    agents=[investigador, redactor],
    tasks=[tarea_investigar, tarea_redactar],
    verbose=True
)

if __name__ == "__main__":
    print("Orquestación multi-agente con CrewAI:")
    print(crew.kickoff()) #kickoff() metodo que pone a trabajar al equipo