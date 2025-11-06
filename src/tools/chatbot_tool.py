import google.generativeai as genai
import os

class ChatbotTool:
    
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
                        print(f"Chatbot configurado con modelo: {model_name}")
                        break
                    except:
                        continue
                
                self.ai_available = bool(self.model)
            else:
                self.model = None
                self.ai_available = False
                print("API key no configurada. Chatbot en modo simulado.")
        except:
            print("Error configurando chatbot")
            self.model = None
            self.ai_available = False

    def start_chat_session(self, processed_texts):
        if not processed_texts:
            print("No hay contenido procesado. Procesa archivos primero.")
            return
        
        print("\n" + "-"*60)
        print("Chat de estudio")
        print("-"*60)
        print("Puedes preguntar sobre:")
        print("   - Conceptos del contenido")
        print("   - Explicaciones")
        print("   - Ejemplos")
        print("   - Resúmenes")
        print("\nComandos:")
        print("   - resumen")
        print("   - conceptos")
        print("   - ejemplos")
        print("   - salir")
        print("-"*60)
        
        context = self._prepare_context(processed_texts)
        self._chat_loop(context)

    def _prepare_context(self, texts):
        context_parts = []
        
        i = 1
        for text in texts:
            context_parts.append(f"--- CONTENIDO {i} ---\n{text}\n")
            i = i + 1
        
        return "\n".join(context_parts)

    def _chat_loop(self, context):
        conversation_history = []
        
        while True:
            print(f"\n{'-'*50}")
            user_input = input("Tu pregunta: ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ['salir', 'exit', 'quit', 'bye']:
                print("Hasta luego. Regresando al menu principal...")
                break
            
            if user_input.lower() == 'resumen':
                response = self._generate_summary(context)
            elif user_input.lower() == 'conceptos':
                response = self._extract_concepts(context)
            elif user_input.lower() == 'ejemplos':
                response = self._generate_examples(context)
            else:
                response = self._generate_response(user_input, context, conversation_history)
            
            print(f"\nRespuesta:")
            print(f"{response}")
            
            conversation_history.append({
                "user": user_input,
                "assistant": response
            })
            
            if len(conversation_history) > 10:
                conversation_history = conversation_history[-10:]

    def _generate_response(self, question, context, history):
        if not self.ai_available:
            return self._simulate_response(question)
        
        try:
            prompt = f"""
Eres un asistente de estudio.

CONTEXTO:
{context[:2000]}

PREGUNTA: {question}

Responde de manera clara.
"""
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except:
            print("Error generando respuesta")
            return self._simulate_response(question)

    def _format_history(self, history):
        if not history:
            return "No hay historial previo."
        
        formatted = []
        for entry in history[-3:]:
            formatted.append(f"Usuario: {entry['user']}")
            formatted.append(f"Asistente: {entry['assistant'][:100]}...")
        
        return "\n".join(formatted)

    def _generate_summary(self, context):
        if not self.ai_available:
            return "Resumen simulado: El contenido cubre temas importantes de programacion orientada a objetos."
        
        try:
            prompt = f"""
Genera un resumen del siguiente contenido:

{context[:1500]}

Usa viñetas y se claro.
"""
            response = self.model.generate_content(prompt)
            return response.text
        except:
            return "Error generando resumen"

    def _extract_concepts(self, context):
        if not self.ai_available:
            return "Conceptos principales: POO, Encapsulacion, Herencia, Polimorfismo, Abstraccion, Clases, Objetos, Metodos, Atributos."
        
        try:
            prompt = f"""
Extrae los conceptos principales del siguiente contenido:

{context[:1500]}

Lista los conceptos mas importantes.
"""
            response = self.model.generate_content(prompt)
            return response.text
        except:
            return "Error extrayendo conceptos"

    def _generate_examples(self, context):
        if not self.ai_available:
            return "Ejemplo simulado: Si tienes una clase 'Estudiante' con atributos como 'nombre' y 'edad', puedes crear objetos."
        
        try:
            prompt = f"""
Genera ejemplos practicos del siguiente contenido:

{context[:1500]}

Ejemplos faciles de entender.
"""
            response = self.model.generate_content(prompt)
            return response.text
        except:
            return "Error generando ejemplos"

    def _simulate_response(self, question):
        responses = [
            f"Respuesta simulada para: '{question}'. El contenido contiene informacion sobre POO.",
            f"Para una respuesta detallada sobre '{question}', activa la API de Gemini.",
        ]
        return responses[hash(question) % len(responses)]
