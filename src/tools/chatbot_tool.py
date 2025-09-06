import google.generativeai as genai
import os
from typing import List, Dict, Any

class ChatbotTool:
    
    def __init__(self):
        try:
            api_key = os.getenv('GEMINI_API_KEY')
            if api_key and api_key != 'tu_api_key_aqui':
                genai.configure(api_key=api_key)
                
                model_names = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
                self.model = None
                
                for model_name in model_names:
                    try:
                        self.model = genai.GenerativeModel(model_name)
                        print(f"✅ Chatbot configurado con modelo: {model_name}")
                        break
                    except Exception as model_error:
                        continue
                
                self.ai_available = bool(self.model)
            else:
                self.model = None
                self.ai_available = False
                print("⚠️ API key no configurada. Chatbot funcionará en modo simulado.")
        except Exception as e:
            print(f"⚠️ Error configurando chatbot: {e}")
            self.model = None
            self.ai_available = False

    def start_chat_session(self, processed_texts: List[str]) -> None:
        if not processed_texts:
            print("❌ No hay contenido procesado. Procesa archivos primero.")
            return
        
        print("\n" + "="*60)
        print("🤖 CHATBOT DE ESTUDIO - StudyBox AI")
        print("="*60)
        print("💡 Puedes preguntar sobre:")
        print("   • Conceptos específicos del contenido")
        print("   • Explicaciones más detalladas")
        print("   • Ejemplos prácticos")
        print("   • Resúmenes de temas")
        print("   • Comparaciones entre conceptos")
        print("\n📝 Comandos especiales:")
        print("   • 'resumen' - Genera un resumen del contenido")
        print("   • 'conceptos' - Lista los conceptos principales")
        print("   • 'ejemplos' - Pide ejemplos del contenido")
        print("   • 'salir' - Termina la sesión de chat")
        print("="*60)
        
        context = self._prepare_context(processed_texts)
        self._chat_loop(context)

    def _prepare_context(self, texts: List[str]) -> str:
        context_parts: List[str] = []
        
        for i, text in enumerate(texts, 1):
            context_parts.append(f"--- CONTENIDO {i} ---\n{text}\n")
        
        return "\n".join(context_parts)

    def _chat_loop(self, context: str) -> None:
        conversation_history: List[Dict[str, str]] = []
        
        while True:
            print(f"\n{'─'*50}")
            user_input: str = input("🧑 Tu pregunta: ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ['salir', 'exit', 'quit', 'bye']:
                print("👋 ¡Hasta luego! Regresando al menú principal...")
                break
            
            response: str
            if user_input.lower() == 'resumen':
                response = self._generate_summary(context)
            elif user_input.lower() == 'conceptos':
                response = self._extract_concepts(context)
            elif user_input.lower() == 'ejemplos':
                response = self._generate_examples(context)
            else:
                response = self._generate_response(user_input, context, conversation_history)
            
            print(f"\n🤖 StudyBox AI:")
            print(f"{response}")
            
            conversation_history.append({
                "user": user_input,
                "assistant": response
            })
            
            if len(conversation_history) > 10:
                conversation_history = conversation_history[-10:]

    def _generate_response(self, question: str, context: str, history: List[Dict]) -> str:
        if not self.ai_available:
            return self._simulate_response(question)
        
        try:
            prompt: str = f"""
Eres un asistente de estudio inteligente especializado en ayudar estudiantes a entender y aprender contenido académico.

CONTEXTO DEL MATERIAL DE ESTUDIO:
{context[:2000]}

HISTORIAL DE CONVERSACIÓN RECIENTE:
{self._format_history(history)}

PREGUNTA ACTUAL: {question}

INSTRUCCIONES:
- Responde de manera clara y educativa
- Usa ejemplos cuando sea apropiado
- Mantén un tono amigable y motivador
- Si la pregunta no está relacionada con el contenido, explica que solo puedes ayudar con el material de estudio disponible
- Si no tienes suficiente información, dilo honestamente
- Usa emojis ocasionalmente para hacer la respuesta más amigable

Responde en español:
"""
            
            response: Any = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            print(f"❌ Error generando respuesta: {e}")
            return self._simulate_response(question)

    def _format_history(self, history: List[Dict]) -> str:
        if not history:
            return "No hay historial previo."
        
        formatted: List[str] = []
        for entry in history[-3:]:
            formatted.append(f"Usuario: {entry['user']}")
            formatted.append(f"Asistente: {entry['assistant'][:100]}...")
        
        return "\n".join(formatted)

    def _generate_summary(self, context: str) -> str:
        if not self.ai_available:
            return "📝 Resumen simulado: El contenido cubre temas importantes de programación orientada a objetos, incluyendo conceptos fundamentales, principios básicos y ejemplos prácticos."
        
        try:
            prompt: str = f"""
Genera un resumen conciso y estructurado del siguiente contenido de estudio:

{context[:1500]}

El resumen debe incluir:
- Los temas principales
- Los conceptos clave
- Los puntos más importantes para recordar

Formato: Usa viñetas y sé claro y directo.
"""
            response: Any = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"❌ Error generando resumen: {e}"

    def _extract_concepts(self, context: str) -> str:
        if not self.ai_available:
            return "🎯 Conceptos principales: Programación Orientada a Objetos, Encapsulación, Herencia, Polimorfismo, Abstracción, Clases, Objetos, Métodos, Atributos."
        
        try:
            prompt: str = f"""
Extrae los conceptos principales y términos clave del siguiente contenido de estudio:

{context[:1500]}

Formato: Lista los conceptos más importantes, uno por línea, con una breve explicación de cada uno.
"""
            response: Any = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"❌ Error extrayendo conceptos: {e}"

    def _generate_examples(self, context: str) -> str:
        if not self.ai_available:
            return "💡 Ejemplo simulado: Si tienes una clase 'Estudiante' con atributos como 'nombre' y 'edad', puedes crear objetos como 'estudiante1 = Estudiante(\"María\", 20)' para representar estudiantes específicos."
        
        try:
            prompt: str = f"""
Basándote en el siguiente contenido de estudio, genera ejemplos prácticos y claros:

{context[:1500]}

Los ejemplos deben ser:
- Fáciles de entender
- Relevantes al contenido
- Útiles para el aprendizaje

Formato: Explica cada ejemplo paso a paso.
"""
            response: Any = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"❌ Error generando ejemplos: {e}"

    def _simulate_response(self, question: str) -> str:
        responses: List[str] = [
            f"🤖 Respuesta simulada para: '{question}'. El contenido procesado contiene información valiosa sobre programación orientada a objetos.",
            f"💡 Basándome en el contenido disponible, puedo ayudarte con conceptos de POO, pero necesitaría la IA real para una respuesta más específica.",
            f"📚 El material procesado incluye temas importantes. Para una respuesta detallada sobre '{question}', activa la API de Gemini.",
        ]
        return responses[hash(question) % len(responses)]
