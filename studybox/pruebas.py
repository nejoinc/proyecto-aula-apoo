from google import genai
import os
from dotenv import load_dotenv # para cargar las variables de entorno desde el archivo .env

# Cargar variables de entorno desde archivo .env
load_dotenv()

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client() # se obtiene la API key desde el archivo .env

response = client.models.generate_content( # se genera el contenido con el modelo gemini-2.5-flash
    model="gemini-2.5-flash", contents=""
)
print(response.text) # se imprime el contenido generado