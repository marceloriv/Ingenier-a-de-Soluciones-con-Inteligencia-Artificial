# Marceloriv

### Causa raíz

1. Modelo no soportado / incompatible: Estaba configurado model="openai/gpt-oss-120b". En Groq este modelo fallaba con BadRequestError: Tool choice is none, but model called a tool, mientras que Mistral arrojaba rate-limit (429) y Gemini 404 para esa versión de API.
2. Regex de parsing JSON rota: re.search(r"Action: (\{.*?\})", ...) era no codiciosa (.*?) y se truncaba en la primera llave de cierre } (ej. en {"tool": "...", "args": {}} cortaba antes de terminar el objeto), provocando error de sintaxis JSON.
3. Manejo de argumentos de funciones: search_web esperaba un string query pero el agente entregaba {"query": "..."}, y get_current_time no admitía parámetros opcionales.

---

### Cambios realizados en el Notebook

- Celda 3: Configuración dinámica de modelo (qwen/qwen3.8-27b para Groq o LLM_MODEL).
- Celda 5: Soporte tolerante de argumentos en get_current_time(args=None) y extracción de parámetro en search_web(query).
- Celda 6:
  - Extractor balanceado de llaves JSON extract_action_json tolerante a bloques markdown y diccionarios anidados.
  - Parámetro de modelo configurable en run_agent(..., model=None).
  - Manejo seguro de llamadas a funciones y registro de traza ReAct paso a paso.

### Pasos para la solución

1. **Evaluación inicial del Notebook**: Extraer el código del Notebook `1-agent-fundamentals.ipynb` para identificar el modelo usado y la lógica de regex/parsing del bucle ReAct.
2. **Validación de Modelos (LLMs)**: Ejecutar pruebas de API con los proveedores configurados en `.env` (Groq, Mistral, Gemini) comprobando cuál estaba operativo, encontrando `qwen/qwen3.8-27b` en Groq como una opción viable frente a los fallos de `gpt-oss-120b`.
3. **Depuración del Parsing ReAct (Thought/Action)**: Crear un script de pruebas aislado (`test_agent_debug.py`) simulando la interacción con la API y observando la falla del regex (`Action: \s*(\{.*?\})`).
4. **Desarrollo del Parser robusto**: Programar e iterar un parser `extract_action_json(text)` en Python aislado (`test_parser.py`) capaz de equilibrar llaves anidadas `{}` saltando comillas y bloqueos markdown sin usar regex estricto y no codicioso.
5. **Flexibilización de Herramientas**: Modificar la función `search_web` para que verifique si el argumento `query` que recibe es dict (`{"query": "..."}`) o directamente un string; y en `get_current_time` aceptar `args=None` por si el agente le inyecta argumentos vacíos o nulos.
6. **Integración y parcheo**: Actualizar el JSON del `.ipynb` reemplazando dinámicamente las celdas 3, 5 y 6 con la lógica corregida mediante un script en Python (`update_nb.py`).
7. **Limpieza y verificación**: Eliminar scripts temporales de depuración e inspeccionar la estructura del notebook resultante.
