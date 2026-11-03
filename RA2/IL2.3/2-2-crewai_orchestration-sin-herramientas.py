"""
IL2.3: Orquestación Multi-Agente con CrewAI (SIN herramientas)
=============================================================
Versión anterior, para comparar: el investigador no tiene herramientas,
así que "investiga" solo con lo que sabe el modelo y puede inventar datos.
Compárala con 2-3-crewai_orchestration.py, donde el investigador usa Wikipedia.
"""

# Requiere: pip install crewai python-dotenv
from crewai import Agent, Task, Crew
from crewai import LLM
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

# Agente 1: Investigador (sin herramientas)
investigador = Agent(
    role="Investigador",
    goal="Buscar información completa sobre una capital del mundo",
    backstory="Eres experto en encontrar datos rápidos.",
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
    description="Busca la informacion sobre la capital de Francia",
    expected_output="Toda la informacion encontrada sobre la capital de Francia",
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
    print("Orquestación multi-agente con CrewAI (sin herramientas):")
    print(crew.kickoff()) #iniciar la orquestación multi-agente desencadenando las tareas 
