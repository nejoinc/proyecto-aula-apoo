import os
import re
from typing import Optional
import google.generativeai as genai
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class ContentProcessor:
    
    def __init__(self):
        """Inicializa el procesador con cliente de IA"""
        try:
            api_key = os.getenv('GEMINI_API_KEY')
            if api_key and api_key != 'tu_api_key_aqui':
                genai.configure(api_key=api_key)
                
                # Intentar con diferentes modelos disponibles
                model_names = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
                self.model = None
                
                for model_name in model_names:
                    try:
                        self.model = genai.GenerativeModel(model_name)
                        print(f"✅ Modelo de IA configurado: {model_name}")
                        break
                    except Exception as model_error:
                        print(f"⚠️ Modelo {model_name} no disponible: {model_error}")
                        continue
                
                if self.model:
                    self.ai_available = True
                else:
                    self.ai_available = False
                    print("❌ Ningún modelo de Gemini disponible")
            else:
                self.model = None
                self.ai_available = False
                print("⚠️ API key de Gemini no configurada. Funcionando en modo simulado.")
        except Exception as e:
            print(f"⚠️ IA no disponible: {e}")
            self.model = None
            self.ai_available = False

    def process_audio(self, file_path: str) -> str:
        """
        Procesa archivos de audio usando IA para transcripción.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Archivo de audio no encontrado: {file_path}")
        
        if self.ai_available:
            try:
                # Simulación de transcripción con IA
                response = self.model.generate_content(
                    f"Transcribe este archivo de audio: {os.path.basename(file_path)}"
                )
                return response.text
            except Exception as e:
                print(f"❌ Error en transcripción IA: {e}")
                return f"Transcripción simulada del archivo de audio {file_path}"
        else:
            return f"Transcripción simulada del archivo de audio {file_path}"

    def process_text_with_ai(self, text: str) -> str:
        """
        Procesa texto usando IA para mejorarlo y estructurarlo.
        """
        if not self.ai_available or not text.strip():
            return text
        
        try:
            prompt = f"""
            Procesa y mejora este texto para estudio:
            - Corrige errores ortográficos
            - Mejora la estructura
            - Mantén el contenido original
            - Hazlo más claro para estudiantes
            
            Texto: {text[:1000]}
            """
            
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"❌ Error en procesamiento IA: {e}")
            return text

    def clean_text(self, text: str) -> str:
        """
        Limpia el texto eliminando caracteres innecesarios y mejorando formato.
        """
        if not text:
            return ""
        
        # Eliminar caracteres de control y espacios extra
        text = re.sub(r'\s+', ' ', text)
        
        # Eliminar caracteres especiales problemáticos
        text = re.sub(r'[^\w\s\.\,\;\:\!\?\-\(\)]', '', text)
        
        # Limpiar espacios al inicio y final
        text = text.strip()
        
        # Capitalizar primera letra
        if text:
            text = text[0].upper() + text[1:]
        
        return text

    def extract_key_concepts(self, text: str) -> list[str]:
        """
        Extrae conceptos clave del texto usando IA.
        """
        if not self.ai_available or not text.strip():
            return []
        
        try:
            prompt = f"""
            Extrae los conceptos clave más importantes de este texto para estudio.
            Devuelve solo una lista de conceptos, uno por línea:
            
            {text[:800]}
            """
            
            response = self.model.generate_content(prompt)
            
            # Dividir respuesta en líneas y limpiar
            concepts = [line.strip() for line in response.text.split('\n') if line.strip()]
            return concepts[:10]  # Máximo 10 conceptos
            
        except Exception as e:
            print(f"❌ Error extrayendo conceptos: {e}")
            return []
