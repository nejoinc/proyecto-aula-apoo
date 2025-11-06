import os
import re
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class ContentProcessor:
    
    def __init__(self):
        try:
            api_key = os.getenv('GEMINI_API_KEY')
            if api_key and api_key != 'tu_api_key_aqui':
                genai.configure(api_key=api_key)
                
                model_names = [
                    'models/gemini-flash-latest',
                    'models/gemini-2.5-flash',
                    'models/gemini-2.0-flash',
                    'models/gemini-pro-latest',
                    'models/gemini-2.5-pro'
                ]
                self.model = None
                
                for model_name in model_names:
                    try:
                        self.model = genai.GenerativeModel(model_name)
                        print(f"Modelo de IA configurado: {model_name}")
                        break
                    except:
                        continue
                
                if self.model:
                    self.ai_available = True
                else:
                    self.ai_available = False
                    print("Ningun modelo de Gemini disponible")
            else:
                self.model = None
                self.ai_available = False
                print("API key de Gemini no configurada.")
        except:
            print(f"IA no disponible")
            self.model = None
            self.ai_available = False

    def process_audio(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Archivo de audio no encontrado: {file_path}")
        
        if self.ai_available:
            try:
                response = self.model.generate_content(
                    f"Transcribe este archivo de audio: {os.path.basename(file_path)}"
                )
                return response.text
            except:
                print(f"Error en transcripcion IA")
                return f"Transcripcion simulada del archivo de audio {file_path}"
        else:
            return f"Transcripcion simulada del archivo de audio {file_path}"

    def process_text_with_ai(self, text):
        if not self.ai_available or not text.strip():
            return text
        
        try:
            prompt = f"""
            Procesa y mejora este texto para estudio:
            - Corrige errores ortograficos
            - Mejora la estructura
            - Manten el contenido original
            - Hazlo mas claro para estudiantes
            
            Texto: {text[:1000]}
            """
            
            response = self.model.generate_content(prompt)
            return response.text
        except:
            print(f"Error en procesamiento IA")
            return text

    def clean_text(self, text):
        if not text:
            return ""
        
        text = re.sub(r'\s+', ' ', text)
        
        text = re.sub(r'[^\w\s\.\,\;\:\!\?\-\(\)]', '', text)
        
        text = text.strip()
        
        if text:
            text = text[0].upper() + text[1:]
        
        return text

    def extract_key_concepts(self, text):
        if not self.ai_available or not text.strip():
            return []
        
        try:
            prompt = f"""
            Extrae los conceptos clave mas importantes de este texto para estudio.
            Devuelve solo una lista de conceptos, uno por linea:
            
            {text[:800]}
            """
            
            response = self.model.generate_content(prompt)
            
            concepts = []
            for line in response.text.split('\n'):
                if line.strip():
                    concepts.append(line.strip())
            
            resultado = []
            for i in range(len(concepts)):
                if i < 10:
                    resultado.append(concepts[i])
            return resultado
            
        except:
            print(f"Error extrayendo conceptos")
            return []
