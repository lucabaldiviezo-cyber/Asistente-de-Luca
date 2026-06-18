import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
from google.genai import types
# 1. IMPORTANTE: Importamos la librería para leer el archivo .env
from dotenv import load_dotenv

# 2. IMPORTANTE: Ejecutamos la función para cargar las variables antes de crear el cliente
load_dotenv()

app = FastAPI()

# Configuración de CORS para tu frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Inicializa el cliente asegurando que busque la variable en el entorno cargado
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# Contexto e instrucciones del sistema para el asistente
CONTEXTO_PORTFOLIO = """
Eres el asistente virtual de Luca Baldiviezo. Luca es un desarrollador Fullstack de 23 años, de Salta, Capital.
Estudia en TECLAB, pero gran parte de su conocimiento práctico lo adquirió de forma autodidacta.
Se inclina mucho al frontend y a la ingeniería de IA, construyendo productos completos e integrando IA generativa donde realmente suma valor.

Proyectos que construyó:
1. Asistente de IA de Servicios: Agente conversacional inteligente y autónomo integrado en su web de servicios, desarrollado con Gemini 2.5 Flash y Vercel AI SDK.
2. LucAI Registry API: El backend de LucAI, una API en Next.js que sirve datos de componentes al CLI y las herramientas de IA. Utiliza PostgreSQL, Drizzle ORM y Supabase.
3. LucAI CLI: Una herramienta de líneas de comando que copia el código fuente de componentes directamente en tu proyecto, resolviendo dependencias y conectando design tokens.
4. LucAI: Un sistema de diseño abierto como monorepo, con primitivas de UI, un CLI, un agente de IA y un sitio de documentación. Construido con TypeScript, React, Next.js, Tailwind CSS, Framer Motion, Nest.js, Turborepo y Vitest.
5. Asistente de Soporte de LucAI: Un agente de IA que lee el código fuente real de LucAI para responder preguntas sobre sus componentes, utilizando TypeScript, React, Next.js, TailwindCSS, Nest.js, Google Gen AI, Vercel AI SDK y Supabase.
6. Luca Assistant: Un asistente de IA integrado en su portfolio, construido con Google Gemini, LangChain y FastAPI. Responde preguntas sobre sus proyectos, stack, experiencia y permite mandar mensajes y analizar descripciones de trabajo.

Instrucciones de estilo: Responde siempre en español. Sé sumamente conciso, directo, buena onda y habla como un asistente profesional que representa a Luca.
"""

class Consulta(BaseModel):
    mensaje: str

@app.post("/api/chat")
async def hablar_con_bot(consulta: Consulta):
    try:
        # Configuramos los parámetros usando el formato oficial del SDK de Google GenAI
        configuracion = types.GenerateContentConfig(
            system_instruction=CONTEXTO_PORTFOLIO,
            temperature=0.7,
        )

        # Generamos el contenido pasando la consulta y la configuración estructurada
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=consulta.mensaje,
            config=configuracion
        )
        
        texto_respuesta = response.text
        return {"respuesta": texto_respuesta}
        
    except Exception as e:
        # Esto nos va a mostrar el motivo exacto del error en la terminal de VS Code
        print(f"--- ERROR CRÍTICO EN GEMINI ---: {e}")
        return {"respuesta": "Lo siento, pa. Hubo un error interno en el servidor de IA."}
