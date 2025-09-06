import os
import json
import requests
import base64
from typing import List, Dict, Any, Optional
import google.generativeai as genai
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class AudioGeneratorTool:
    
    def __init__(self):
        """Inicializa el generador de audio con IA"""
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
                        print(f"✅ Generador de audio configurado con modelo: {model_name}")
                        break
                    except Exception as model_error:
                        continue
                
                self.ai_available = bool(self.model)
            else:
                self.model = None
                self.ai_available = False
                print("⚠️ API key no configurada. Generador funcionará en modo simulado.")
        except Exception as e:
            print(f"⚠️ Error configurando generador de audio: {e}")
            self.model = None
            self.ai_available = False

    def generate_audio_content(self, processed_texts: List[str]) -> None:
        """
        Genera contenido de audio educativo basado en el contenido procesado
        """
        if not processed_texts:
            print("❌ No hay contenido procesado. Procesa archivos primero.")
            return
        
        print("\n" + "="*60)
        print("🎵 GENERADOR DE AUDIO EDUCATIVO - StudyBox AI")
        print("="*60)
        print("💡 Tipos de audio disponibles:")
        print("   1. 📚 Resumen narrado")
        print("   2. 🎯 Explicación de conceptos clave")
        print("   3. 📖 Lectura completa del contenido")
        print("   4. 🧠 Preguntas y respuestas")
        print("   5. 🎭 Historia/conversación educativa")
        print("   6. 📝 Guía de estudio paso a paso")
        print("   7. 🔄 Generar todos los tipos")
        print("   0. Volver al menú principal")
        print("="*60)
        
        # Preparar contexto
        context = self._prepare_context(processed_texts)
        
        while True:
            try:
                opcion = input("\nSelecciona el tipo de audio (0-7): ").strip()
                
                if opcion == "0":
                    print("👋 Regresando al menú principal...")
                    break
                elif opcion == "1":
                    self._generate_summary_audio(context)
                elif opcion == "2":
                    self._generate_concepts_audio(context)
                elif opcion == "3":
                    self._generate_full_reading_audio(context)
                elif opcion == "4":
                    self._generate_qa_audio(context)
                elif opcion == "5":
                    self._generate_story_audio(context)
                elif opcion == "6":
                    self._generate_study_guide_audio(context)
                elif opcion == "7":
                    self._generate_all_audio_types(context)
                else:
                    print("❌ Opción no válida. Selecciona un número del 0 al 7.")
                    
            except KeyboardInterrupt:
                print("\n👋 Regresando al menú principal...")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

    def _prepare_context(self, texts: List[str]) -> str:
        """Prepara el contexto combinando todos los textos procesados"""
        context_parts = []
        
        for i, text in enumerate(texts, 1):
            context_parts.append(f"--- CONTENIDO {i} ---\n{text}\n")
        
        return "\n".join(context_parts)

    def _generate_summary_audio(self, context: str) -> None:
        """Genera script de audio para resumen narrado"""
        print("\n📚 Generando resumen narrado...")
        
        if not self.ai_available:
            script = self._simulate_summary_script(context)
        else:
            try:
                prompt = f"""
Crea un script de audio para un resumen narrado educativo del siguiente contenido:

{context[:2000]}

El script debe ser:
- Conversacional y amigable
- Fácil de seguir auditivamente
- Incluir introducción y conclusión
- Duración aproximada: 3-5 minutos
- Usar lenguaje claro y directo
- Incluir pausas naturales marcadas con [PAUSA]

Formato:
[INTRODUCCIÓN]
Hola, soy tu asistente de estudio. Hoy vamos a repasar los conceptos más importantes de...

[CONTENIDO PRINCIPAL]
Los puntos clave que debes recordar son...

[CONCLUSIÓN]
Para resumir, hemos cubierto...

Genera el script completo:
"""
                response = self.model.generate_content(prompt)
                script = response.text
            except Exception as e:
                print(f"❌ Error generando resumen: {e}")
                script = self._simulate_summary_script(context)
        
        self._save_audio_script("resumen_narrado", script)
        self._display_audio_instructions("Resumen Narrado", script)

    def _generate_concepts_audio(self, context: str) -> None:
        """Genera script de audio para explicación de conceptos"""
        print("\n🎯 Generando explicación de conceptos...")
        
        if not self.ai_available:
            script = self._simulate_concepts_script(context)
        else:
            try:
                prompt = f"""
Crea un script de audio educativo que explique los conceptos clave del siguiente contenido:

{context[:2000]}

El script debe:
- Explicar cada concepto de manera clara
- Usar analogías y ejemplos simples
- Tener un ritmo pausado para facilitar comprensión
- Incluir repeticiones importantes
- Duración: 5-7 minutos
- Formato conversacional

Estructura:
[INTRODUCCIÓN]
Hoy vamos a entender los conceptos fundamentales...

[CONCEPTO 1]
El primer concepto es... [explicación detallada]

[CONCEPTO 2]
Ahora hablemos de... [explicación detallada]

[REPASO]
Para asegurarnos de que entendiste...

Genera el script completo:
"""
                response = self.model.generate_content(prompt)
                script = response.text
            except Exception as e:
                print(f"❌ Error generando conceptos: {e}")
                script = self._simulate_concepts_script(context)
        
        self._save_audio_script("explicacion_conceptos", script)
        self._display_audio_instructions("Explicación de Conceptos", script)

    def _generate_full_reading_audio(self, context: str) -> None:
        """Genera script de audio para lectura completa"""
        print("\n📖 Generando lectura completa...")
        
        if not self.ai_available:
            script = self._simulate_reading_script(context)
        else:
            try:
                prompt = f"""
Crea un script de audio para una lectura completa y educativa del siguiente contenido:

{context[:2000]}

El script debe:
- Ser una lectura fluida y natural
- Incluir énfasis en puntos importantes
- Tener pausas estratégicas para reflexión
- Mantener el interés del oyente
- Duración: 8-12 minutos
- Formato de narración profesional

Estructura:
[INTRODUCCIÓN]
Bienvenido a esta sesión de estudio. Vamos a explorar...

[LECTURA PRINCIPAL]
[Contenido adaptado para audio con énfasis y pausas]

[CONCLUSIÓN]
Hemos completado el repaso de...

Genera el script completo:
"""
                response = self.model.generate_content(prompt)
                script = response.text
            except Exception as e:
                print(f"❌ Error generando lectura: {e}")
                script = self._simulate_reading_script(context)
        
        self._save_audio_script("lectura_completa", script)
        self._display_audio_instructions("Lectura Completa", script)

    def _generate_qa_audio(self, context: str) -> None:
        """Genera script de audio de preguntas y respuestas"""
        print("\n🧠 Generando preguntas y respuestas...")
        
        if not self.ai_available:
            script = self._simulate_qa_script(context)
        else:
            try:
                prompt = f"""
Crea un script de audio educativo en formato de preguntas y respuestas basado en:

{context[:2000]}

El script debe:
- Incluir 5-7 preguntas importantes
- Dar respuestas claras y completas
- Usar formato de entrevista/conversación
- Duración: 6-8 minutos
- Ser interactivo y dinámico

Estructura:
[INTRODUCCIÓN]
Hoy vamos a resolver algunas preguntas importantes sobre...

[PREGUNTA 1]
P: ¿Qué es...?
R: Excelente pregunta. [Explicación detallada]

[PREGUNTA 2]
P: ¿Cómo funciona...?
R: Te explico paso a paso...

[CONCLUSIÓN]
Espero que estas respuestas te hayan ayudado...

Genera el script completo:
"""
                response = self.model.generate_content(prompt)
                script = response.text
            except Exception as e:
                print(f"❌ Error generando Q&A: {e}")
                script = self._simulate_qa_script(context)
        
        self._save_audio_script("preguntas_respuestas", script)
        self._display_audio_instructions("Preguntas y Respuestas", script)

    def _generate_story_audio(self, context: str) -> None:
        """Genera script de audio como historia/conversación"""
        print("\n🎭 Generando historia educativa...")
        
        if not self.ai_available:
            script = self._simulate_story_script(context)
        else:
            try:
                prompt = f"""
Crea un script de audio educativo en formato de historia o conversación basado en:

{context[:2000]}

El script debe:
- Usar personajes o situaciones narrativas
- Ser entretenido pero educativo
- Incluir diálogos naturales
- Duración: 7-10 minutos
- Mantener el interés con storytelling

Estructura:
[ESCENA 1]
[Personaje 1]: "¿Sabías que...?"
[Personaje 2]: "No, cuéntame más..."

[ESCENA 2]
[Desarrollo de la historia con conceptos educativos]

[CONCLUSIÓN]
[Resumen de lo aprendido a través de la historia]

Genera el script completo:
"""
                response = self.model.generate_content(prompt)
                script = response.text
            except Exception as e:
                print(f"❌ Error generando historia: {e}")
                script = self._simulate_story_script(context)
        
        self._save_audio_script("historia_educativa", script)
        self._display_audio_instructions("Historia Educativa", script)

    def _generate_study_guide_audio(self, context: str) -> None:
        """Genera script de audio de guía de estudio"""
        print("\n📝 Generando guía de estudio...")
        
        if not self.ai_available:
            script = self._simulate_study_guide_script(context)
        else:
            try:
                prompt = f"""
Crea un script de audio de guía de estudio paso a paso basado en:

{context[:2000]}

El script debe:
- Ser una guía práctica de estudio
- Incluir pasos claros y organizados
- Dar consejos de memorización
- Duración: 5-7 minutos
- Formato de tutor personal

Estructura:
[INTRODUCCIÓN]
Hola, soy tu tutor de estudio. Te voy a guiar paso a paso...

[PASO 1]
Primero, vamos a identificar los conceptos clave...

[PASO 2]
Ahora, vamos a crear conexiones entre ideas...

[PASO 3]
Para memorizar mejor, usa esta técnica...

[CONCLUSIÓN]
Con estos pasos, estarás listo para...

Genera el script completo:
"""
                response = self.model.generate_content(prompt)
                script = response.text
            except Exception as e:
                print(f"❌ Error generando guía: {e}")
                script = self._simulate_study_guide_script(context)
        
        self._save_audio_script("guia_estudio", script)
        self._display_audio_instructions("Guía de Estudio", script)

    def _generate_all_audio_types(self, context: str) -> None:
        """Genera todos los tipos de audio"""
        print("\n🔄 Generando todos los tipos de audio...")
        
        audio_types = [
            ("Resumen Narrado", self._generate_summary_audio),
            ("Explicación de Conceptos", self._generate_concepts_audio),
            ("Lectura Completa", self._generate_full_reading_audio),
            ("Preguntas y Respuestas", self._generate_qa_audio),
            ("Historia Educativa", self._generate_story_audio),
            ("Guía de Estudio", self._generate_study_guide_audio)
        ]
        
        for name, generator_func in audio_types:
            print(f"\n📝 Generando: {name}")
            try:
                generator_func(context)
                print(f"✅ {name} generado exitosamente")
            except Exception as e:
                print(f"❌ Error generando {name}: {e}")
        
        print("\n🎉 ¡Todos los audios han sido generados!")

    def _save_audio_script(self, filename: str, script: str) -> None:
        """Guarda el script de audio en un archivo"""
        try:
            # Crear directorio de scripts si no existe
            scripts_dir = os.path.join(os.path.dirname(__file__), "..", "storage", "audio_scripts")
            os.makedirs(scripts_dir, exist_ok=True)
            
            # Guardar script
            filepath = os.path.join(scripts_dir, f"{filename}.txt")
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(script)
            
            print(f"💾 Script guardado en: {filepath}")
        except Exception as e:
            print(f"❌ Error guardando script: {e}")

    def _display_audio_instructions(self, audio_type: str, script: str) -> None:
        """Muestra instrucciones y opciones para generar audio"""
        print(f"\n🎵 {audio_type} - Script Generado")
        print("="*50)
        print("📋 Script generado:")
        print("-" * 30)
        print(script[:500] + "..." if len(script) > 500 else script)
        print("-" * 30)
        
        print("\n🔊 Opciones para generar audio:")
        print("1. 🎤 Generar audio con Google TTS (gratis)")
        print("2. 🤖 Generar audio con ElevenLabs (premium)")
        print("3. 📱 Usar servicios online")
        print("4. 💾 Solo guardar script")
        
        while True:
            try:
                opcion = input("\nSelecciona una opción (1-4): ").strip()
                
                if opcion == "1":
                    self._generate_google_tts_audio(script, audio_type)
                    break
                elif opcion == "2":
                    self._generate_elevenlabs_audio(script, audio_type)
                    break
                elif opcion == "3":
                    self._show_online_services_info()
                    break
                elif opcion == "4":
                    print("✅ Script guardado. Puedes convertirlo a audio más tarde.")
                    break
                else:
                    print("❌ Opción no válida. Selecciona 1-4.")
            except KeyboardInterrupt:
                print("\n👋 Regresando...")
                break

    def _generate_google_tts_audio(self, script: str, audio_type: str) -> None:
        """Genera audio usando Google Text-to-Speech"""
        print("\n🎤 Generando audio con Google TTS...")
        
        try:
            # Limpiar script para TTS
            clean_script = self._clean_script_for_tts(script)
            
            # Usar Google TTS API
            audio_data = self._call_google_tts(clean_script)
            
            if audio_data:
                # Guardar archivo de audio
                filename = f"{audio_type.lower().replace(' ', '_')}_local_tts.wav"
                audio_path = self._save_audio_file(filename, audio_data)
                
                if audio_path:
                    print(f"✅ Audio generado exitosamente: {audio_path}")
                    print(f"📁 Ubicación: {os.path.abspath(audio_path)}")
                    self._play_audio_instructions(audio_path)
                else:
                    print("❌ Error guardando archivo de audio")
            else:
                print("❌ Error generando audio con Google TTS")
                self._show_manual_tts_instructions(clean_script)
                
        except Exception as e:
            print(f"❌ Error en Google TTS: {e}")
            self._show_manual_tts_instructions(script)

    def _generate_elevenlabs_audio(self, script: str, audio_type: str) -> None:
        """Genera audio usando ElevenLabs (requiere API key)"""
        print("\n🤖 Generando audio con ElevenLabs...")
        
        api_key = os.getenv('ELEVENLABS_API_KEY')
        if not api_key or api_key == 'tu_api_key_aqui':
            print("⚠️ API key de ElevenLabs no configurada.")
            print("💡 Para usar ElevenLabs:")
            print("   1. Ve a https://elevenlabs.io")
            print("   2. Crea una cuenta y obtén tu API key")
            print("   3. Agrega ELEVENLABS_API_KEY=tu_key en tu archivo .env")
            return
        
        try:
            # Limpiar script para TTS
            clean_script = self._clean_script_for_tts(script)
            
            # Usar ElevenLabs API
            audio_data = self._call_elevenlabs_tts(clean_script, api_key)
            
            if audio_data:
                # Guardar archivo de audio
                filename = f"{audio_type.lower().replace(' ', '_')}_elevenlabs.mp3"
                audio_path = self._save_audio_file(filename, audio_data)
                
                if audio_path:
                    print(f"✅ Audio generado exitosamente: {audio_path}")
                    print(f"📁 Ubicación: {os.path.abspath(audio_path)}")
                    self._play_audio_instructions(audio_path)
                else:
                    print("❌ Error guardando archivo de audio")
            else:
                print("❌ Error generando audio con ElevenLabs")
                
        except Exception as e:
            print(f"❌ Error en ElevenLabs: {e}")

    def _clean_script_for_tts(self, script: str) -> str:
        """Limpia el script para optimizar la conversión a audio"""
        # Remover marcadores de formato
        clean_script = script.replace('[INTRODUCCIÓN]', '')
        clean_script = clean_script.replace('[CONTENIDO PRINCIPAL]', '')
        clean_script = clean_script.replace('[CONCLUSIÓN]', '')
        clean_script = clean_script.replace('[PAUSA]', '. ')
        clean_script = clean_script.replace('[ESCENA 1]', '')
        clean_script = clean_script.replace('[ESCENA 2]', '')
        clean_script = clean_script.replace('[PASO 1]', 'Primero,')
        clean_script = clean_script.replace('[PASO 2]', 'Segundo,')
        clean_script = clean_script.replace('[PASO 3]', 'Tercero,')
        
        # Limpiar espacios extra
        clean_script = ' '.join(clean_script.split())
        
        # Limitar longitud para APIs
        if len(clean_script) > 4000:
            clean_script = clean_script[:4000] + "..."
        
        return clean_script

    def _call_google_tts(self, text: str) -> Optional[bytes]:
        """Genera audio MP3 directamente usando pyttsx3"""
        try:
            # Usar pyttsx3 - librería local que no requiere internet
            import pyttsx3
            import tempfile
            import os
            
            # Configurar motor TTS
            engine = pyttsx3.init()
            
            # Configurar propiedades de voz
            voices = engine.getProperty('voices')
            for voice in voices:
                if 'spanish' in voice.name.lower() or 'es' in voice.id.lower():
                    engine.setProperty('voice', voice.id)
                    break
            
            # Configurar velocidad y volumen
            engine.setProperty('rate', 150)  # Velocidad de habla
            engine.setProperty('volume', 0.9)  # Volumen
            
            # Crear archivo temporal
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_path = temp_file.name
            
            # Generar audio
            engine.save_to_file(text, temp_path)
            engine.runAndWait()
            
            # Leer archivo generado
            with open(temp_path, 'rb') as f:
                audio_data = f.read()
            
            # Limpiar archivo temporal
            os.unlink(temp_path)
            
            return audio_data
                
        except ImportError:
            print("⚠️ pyttsx3 no está instalado. Instalando...")
            try:
                import subprocess
                subprocess.check_call(['py', '-m', 'pip', 'install', 'pyttsx3'])
                print("✅ pyttsx3 instalado. Reintentando...")
                return self._call_google_tts(text)
            except Exception as install_error:
                print(f"❌ Error instalando pyttsx3: {install_error}")
                return self._fallback_google_tts(text)
        except Exception as e:
            print(f"❌ Error con pyttsx3: {e}")
            return self._fallback_google_tts(text)

    def _fallback_google_tts(self, text: str) -> Optional[bytes]:
        """Método alternativo usando requests directo"""
        try:
            # Dividir texto en chunks si es muy largo
            if len(text) > 200:
                chunks = [text[i:i+200] for i in range(0, len(text), 200)]
                audio_data = b''
                
                for chunk in chunks:
                    chunk_audio = self._get_single_chunk_audio(chunk)
                    if chunk_audio:
                        audio_data += chunk_audio
                
                return audio_data if audio_data else None
            else:
                return self._get_single_chunk_audio(text)
                
        except Exception as e:
            print(f"❌ Error en fallback TTS: {e}")
            return None

    def _get_single_chunk_audio(self, text: str) -> Optional[bytes]:
        """Obtiene audio para un chunk de texto"""
        try:
            import urllib.parse
            
            # URL de Google TTS
            url = "https://translate.google.com/translate_tts"
            
            params = {
                'ie': 'UTF-8',
                'q': text,
                'tl': 'es',
                'client': 'tw-ob',
                'idx': '0',
                'total': '1'
            }
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Referer': 'https://translate.google.com/',
                'Accept': 'audio/mpeg,audio/*,*/*;q=0.9'
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            
            if response.status_code == 200 and response.content:
                return response.content
            else:
                print(f"❌ Error en Google TTS: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error obteniendo audio: {e}")
            return None

    def _call_elevenlabs_tts(self, text: str, api_key: str) -> Optional[bytes]:
        """Llama a ElevenLabs Text-to-Speech API"""
        try:
            url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM"
            
            headers = {
                'Accept': 'audio/mpeg',
                'Content-Type': 'application/json',
                'xi-api-key': api_key
            }
            
            data = {
                'text': text,
                'model_id': 'eleven_monolingual_v1',
                'voice_settings': {
                    'stability': 0.5,
                    'similarity_boost': 0.5
                }
            }
            
            response = requests.post(url, json=data, headers=headers)
            
            if response.status_code == 200:
                return response.content
            else:
                print(f"❌ Error en ElevenLabs: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error llamando ElevenLabs: {e}")
            return None

    def _save_audio_file(self, filename: str, audio_data: bytes) -> Optional[str]:
        """Guarda el archivo de audio"""
        try:
            # Crear directorio de audios si no existe
            audio_dir = os.path.join(os.path.dirname(__file__), "..", "storage", "generated_audio")
            os.makedirs(audio_dir, exist_ok=True)
            
            # Guardar archivo
            filepath = os.path.join(audio_dir, filename)
            with open(filepath, 'wb') as f:
                f.write(audio_data)
            
            return filepath
            
        except Exception as e:
            print(f"❌ Error guardando audio: {e}")
            return None

    def _play_audio_instructions(self, audio_path: str) -> None:
        """Muestra instrucciones y abre el reproductor de consola"""
        print(f"\n🎧 Audio generado exitosamente!")
        print(f"📁 Ubicación: {audio_path}")
        
        print(f"\n🎵 Abriendo reproductor de consola...")
        print(f"🔊 El audio se reproducirá directamente aquí")
        
        # Importar y usar el reproductor de consola
        try:
            from .audio_player_tool import AudioPlayerTool
            player = AudioPlayerTool()
            
            # Reproducir el archivo específico
            if player.play_audio_file(audio_path):
                print("✅ Audio reproducido exitosamente")
            else:
                print("❌ Error reproduciendo el audio")
                self._show_manual_options(audio_path)
                
        except Exception as e:
            print(f"❌ Error abriendo reproductor: {e}")
            self._show_manual_options(audio_path)

    def _show_manual_options(self, audio_path: str) -> None:
        """Muestra opciones manuales si falla el reproductor automático"""
        print(f"\n🎵 Opciones alternativas:")
        print(f"• 🎧 Usa el Reproductor de Audio integrado (Opción 5 del menú)")
        print(f"• 🖱️ Doble clic en el archivo para abrir con reproductor externo")
        print(f"• ⌨️ Comando rápido: py -c \"import os; os.startfile('{audio_path}')\"")

    def _show_online_services_info(self) -> None:
        """Muestra información sobre servicios TTS online"""
        print("\n🌐 Servicios TTS Online Gratuitos:")
        print("1. 🟢 Google Translate TTS:")
        print("   • Ve a translate.google.com")
        print("   • Pega tu texto")
        print("   • Haz clic en el ícono de audio")
        print("   • Descarga el audio")
        
        print("\n2. 🔵 Microsoft Edge TTS:")
        print("   • Abre Edge")
        print("   • Ve a edge://flags/#edge-read-aloud")
        print("   • Habilita la función")
        
        print("\n3. 🟡 Natural Reader Online:")
        print("   • Ve a naturalreaders.com")
        print("   • Pega tu texto")
        print("   • Selecciona voz en español")
        print("   • Descarga el audio")

    def _show_manual_tts_instructions(self, script: str) -> None:
        """Muestra instrucciones manuales para TTS"""
        print("\n📋 Script limpio para TTS:")
        print("-" * 40)
        print(script)
        print("-" * 40)
        
        print("\n💡 Instrucciones:")
        print("1. Copia el texto de arriba")
        print("2. Ve a translate.google.com")
        print("3. Pega el texto")
        print("4. Haz clic en 🔊 para escuchar")
        print("5. Usa herramientas de captura de audio para grabar")

    # Métodos de simulación para cuando no hay IA disponible
    def _simulate_summary_script(self, context: str) -> str:
        return f"""[INTRODUCCIÓN]
Hola, soy tu asistente de estudio. Hoy vamos a repasar los conceptos más importantes del contenido que has estudiado.

[CONTENIDO PRINCIPAL]
Los puntos clave que debes recordar son: {context[:200]}...

[CONCLUSIÓN]
Para resumir, hemos cubierto los conceptos fundamentales. Recuerda repasar estos puntos regularmente para una mejor retención."""

    def _simulate_concepts_script(self, context: str) -> str:
        return f"""[INTRODUCCIÓN]
Hoy vamos a entender los conceptos fundamentales paso a paso.

[CONCEPTO 1]
El primer concepto importante es... {context[:150]}

[CONCEPTO 2]
Ahora hablemos de... {context[150:300]}

[REPASO]
Para asegurarnos de que entendiste, repasemos los puntos clave."""

    def _simulate_reading_script(self, context: str) -> str:
        return f"""[INTRODUCCIÓN]
Bienvenido a esta sesión de estudio. Vamos a explorar el contenido completo.

[LECTURA PRINCIPAL]
{context[:400]}

[CONCLUSIÓN]
Hemos completado el repaso del contenido. Espero que haya sido útil para tu aprendizaje."""

    def _simulate_qa_script(self, context: str) -> str:
        return f"""[INTRODUCCIÓN]
Hoy vamos a resolver algunas preguntas importantes sobre el contenido.

[PREGUNTA 1]
P: ¿Cuál es el concepto principal?
R: El concepto principal es... {context[:100]}

[PREGUNTA 2]
P: ¿Cómo se aplica esto?
R: Se aplica de la siguiente manera... {context[100:200]}

[CONCLUSIÓN]
Espero que estas respuestas te hayan ayudado a entender mejor el contenido."""

    def _simulate_story_script(self, context: str) -> str:
        return f"""[ESCENA 1]
[Estudiante]: "¿Puedes explicarme este concepto de manera simple?"
[Tutor]: "¡Por supuesto! Imagina que... {context[:150]}"

[ESCENA 2]
[Desarrollo de la historia con conceptos educativos]

[CONCLUSIÓN]
[Resumen de lo aprendido a través de la historia]"""

    def _simulate_study_guide_script(self, context: str) -> str:
        return f"""[INTRODUCCIÓN]
Hola, soy tu tutor de estudio. Te voy a guiar paso a paso.

[PASO 1]
Primero, identifica los conceptos clave: {context[:100]}

[PASO 2]
Ahora, crea conexiones entre ideas: {context[100:200]}

[PASO 3]
Para memorizar mejor, usa técnicas de repetición espaciada.

[CONCLUSIÓN]
Con estos pasos, estarás listo para dominar el contenido."""
