import os
import json
import random
from typing import List, Dict, Any, Optional
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class QuizTool:
    def __init__(self):
        """Inicializa el generador de quiz con IA"""
        try:
            api_key = os.getenv('GEMINI_API_KEY')
            if api_key and api_key != 'tu_api_key_aqui':
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel('gemini-1.5-flash')
                self.ai_available = True
            else:
                self.model = None
                self.ai_available = False
                print("⚠️ API key de Gemini no configurada para Quiz. Funcionando en modo simulado.")
        except Exception as e:
            print(f"⚠️ IA no disponible para Quiz: {e}")
            self.model = None
            self.ai_available = False
        
        # Directorio para almacenar quizzes
        self.storage_dir = os.path.join(os.path.dirname(__file__), "..", "storage", "quizzes")
        os.makedirs(self.storage_dir, exist_ok=True)

    def generate_quiz(self, processed_texts: List[str]) -> None:
        """Genera quizzes inteligentes usando IA"""
        print("\nGenerador de quiz")
        print("-"*60)
        
        if not processed_texts:
            print("❌ No hay contenido procesado disponible.")
            print("💡 Procesa algunos archivos primero para generar quizzes.")
            return
        
        print("Contenido disponible para el quiz:")
        for i, text in enumerate(processed_texts, 1):
            preview = text[:100] + "..." if len(text) > 100 else text
            print(f"{i}. {preview}")
        
        print("\nOpciones:")
        print("1. Opción múltiple")
        print("2. Verdadero/Falso")
        print("3. Completar espacios")
        print("4. Preguntas abiertas")
        print("5. Mixto")
        print("6. Por tema específico")
        print("0. Volver")
        
        while True:
            try:
                choice = input("\nSelecciona opción: ").strip()
                
                if choice == "0":
                    print("👋 Regresando al menú principal...")
                    break
                elif choice == "1":
                    self._generate_multiple_choice_quiz(processed_texts)
                    break
                elif choice == "2":
                    self._generate_true_false_quiz(processed_texts)
                    break
                elif choice == "3":
                    self._generate_fill_blank_quiz(processed_texts)
                    break
                elif choice == "4":
                    self._generate_open_questions_quiz(processed_texts)
                    break
                elif choice == "5":
                    self._generate_mixed_quiz(processed_texts)
                    break
                elif choice == "6":
                    self._generate_topic_quiz(processed_texts)
                    break
                else:
                    print("Opción inválida. Selecciona 1-6 o 0.")
                    
            except KeyboardInterrupt:
                print("\n👋 Regresando al menú principal...")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

    def _generate_multiple_choice_quiz(self, texts: List[str]) -> None:
        """Genera quiz de opción múltiple usando IA"""
        print("\nGenerando quiz de opción múltiple...")
        
        num_questions = self._get_quiz_length()
        combined_text = "\n\n".join(texts)
        context = combined_text[:8000]
        
        if not self.ai_available:
            quiz = self._generate_simple_multiple_choice(context, num_questions)
        else:
            quiz = self._generate_ai_multiple_choice(context, num_questions)
        
        if quiz:
            self._save_and_display_quiz(quiz, "opcion_multiple")
        else:
            print("No se pudo generar el quiz.")

    def _generate_true_false_quiz(self, texts: List[str]) -> None:
        """Genera quiz de verdadero/falso"""
        print("\nGenerando quiz de verdadero/falso...")
        
        num_questions = self._get_quiz_length()
        combined_text = "\n\n".join(texts)
        context = combined_text[:8000]
        
        if not self.ai_available:
            quiz = self._generate_simple_true_false(context, num_questions)
        else:
            quiz = self._generate_ai_true_false(context, num_questions)
        
        if quiz:
            self._save_and_display_quiz(quiz, "verdadero_falso")
        else:
            print("No se pudo generar el quiz.")

    def _generate_fill_blank_quiz(self, texts: List[str]) -> None:
        """Genera quiz de completar espacios"""
        print("\nGenerando quiz de completar espacios...")
        
        num_questions = self._get_quiz_length()
        combined_text = "\n\n".join(texts)
        context = combined_text[:8000]
        
        if not self.ai_available:
            quiz = self._generate_simple_fill_blank(context, num_questions)
        else:
            quiz = self._generate_ai_fill_blank(context, num_questions)
        
        if quiz:
            self._save_and_display_quiz(quiz, "completar_espacios")
        else:
            print("No se pudo generar el quiz.")

    def _generate_open_questions_quiz(self, texts: List[str]) -> None:
        """Genera quiz de preguntas abiertas"""
        print("\nGenerando quiz de preguntas abiertas...")
        
        num_questions = self._get_quiz_length()
        combined_text = "\n\n".join(texts)
        context = combined_text[:8000]
        
        if not self.ai_available:
            quiz = self._generate_simple_open_questions(context, num_questions)
        else:
            quiz = self._generate_ai_open_questions(context, num_questions)
        
        if quiz:
            self._save_and_display_quiz(quiz, "preguntas_abiertas")
        else:
            print("No se pudo generar el quiz.")

    def _generate_mixed_quiz(self, texts: List[str]) -> None:
        """Genera quiz mixto con diferentes tipos de preguntas"""
        print("\nGenerando quiz mixto...")
        
        num_questions = self._get_quiz_length()
        combined_text = "\n\n".join(texts)
        context = combined_text[:8000]
        
        if not self.ai_available:
            quiz = self._generate_simple_mixed(context, num_questions)
        else:
            quiz = self._generate_ai_mixed(context, num_questions)
        
        if quiz:
            self._save_and_display_quiz(quiz, "mixto")
        else:
            print("No se pudo generar el quiz.")

    def _generate_topic_quiz(self, texts: List[str]) -> None:
        """Genera quiz sobre un tema específico"""
        topic = input("\nTema específico para el quiz: ").strip()
        if not topic:
            print("❌ Tema no válido.")
            return
        
        print(f"\nGenerando quiz sobre: {topic}")
        
        num_questions = self._get_quiz_length()
        combined_text = "\n\n".join(texts)
        context = combined_text[:8000]
        
        if not self.ai_available:
            quiz = self._generate_simple_topic(context, num_questions, topic)
        else:
            quiz = self._generate_ai_topic(context, num_questions, topic)
        
        if quiz:
            self._save_and_display_quiz(quiz, f"tema_{topic.replace(' ', '_')}")
        else:
            print("No se pudo generar el quiz.")

    def _get_quiz_length(self) -> int:
        """Obtiene el número de preguntas para el quiz"""
        while True:
            try:
                num = input("\n📊 ¿Cuántas preguntas quieres? (5-20): ").strip()
                if num == "":
                    return 10  # Default
                
                num_questions = int(num)
                if 5 <= num_questions <= 20:
                    return num_questions
                else:
                    print("❌ El número debe estar entre 5 y 20.")
            except ValueError:
                print("❌ Ingresa un número válido.")

    def _generate_ai_multiple_choice(self, text: str, num_questions: int) -> List[Dict[str, Any]]:
        """Genera quiz de opción múltiple usando IA"""
        try:
            prompt = f"""
            Genera {num_questions} preguntas de opción múltiple de alta calidad basadas en el siguiente contenido:
            
            CONTENIDO:
            {text}
            
            FORMATO REQUERIDO:
            - Cada pregunta debe tener 4 opciones (A, B, C, D)
            - Solo una respuesta debe ser correcta
            - Las opciones incorrectas deben ser plausibles pero incorrectas
            - Las preguntas deben cubrir conceptos importantes del contenido
            - Usa un lenguaje claro y académico
            
            RESPONDE SOLO EN FORMATO JSON:
            [
                {{
                    "Q": "Pregunta 1",
                    "Options": ["Opción A", "Opción B", "Opción C", "Opción D"],
                    "Answer": "A",
                    "Explanation": "Explicación de por qué es correcta"
                }},
                ...
            ]
            
            IMPORTANTE: Responde únicamente con el JSON, sin texto adicional.
            """
            
            response = self.model.generate_content(prompt)
            ai_text = response.text.strip()
            
            # Limpiar respuesta si tiene markdown
            if ai_text.startswith("```json"):
                ai_text = ai_text[7:]
            if ai_text.endswith("```"):
                ai_text = ai_text[:-3]
            
            quiz = json.loads(ai_text)
            
            # Validar formato
            if isinstance(quiz, list) and all(
                isinstance(q, dict) and "Q" in q and "Options" in q and "Answer" in q
                for q in quiz
            ):
                return quiz
            else:
                print("⚠️ Formato de respuesta de IA inválido.")
                return self._generate_simple_multiple_choice(text, num_questions)
                
        except json.JSONDecodeError as e:
            print(f"⚠️ Error parseando respuesta de IA: {e}")
            return self._generate_simple_multiple_choice(text, num_questions)
        except Exception as e:
            print(f"❌ Error generando quiz con IA: {e}")
            return self._generate_simple_multiple_choice(text, num_questions)

    def _generate_simple_multiple_choice(self, text: str, num_questions: int) -> List[Dict[str, Any]]:
        """Genera quiz simple de opción múltiple como fallback"""
        print("📝 Generando quiz básico de opción múltiple...")
        
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        quiz = []
        
        for i in range(min(num_questions, len(sentences))):
            if i < len(sentences):
                sentence = sentences[i]
                if len(sentence) > 20:
                    quiz.append({
                        "Q": f"¿Qué información importante se menciona en: '{sentence[:50]}...'?",
                        "Options": [
                            sentence[:30] + "...",
                            "Información relacionada",
                            "Datos complementarios", 
                            "Información adicional"
                        ],
                        "Answer": "A",
                        "Explanation": f"La respuesta correcta es la primera opción basada en el contenido."
                    })
        
        # Completar con preguntas genéricas si no hay suficientes
        while len(quiz) < num_questions:
            quiz.append({
                "Q": f"¿Cuál es un concepto importante del contenido estudiado?",
                "Options": [
                    "Concepto clave del material",
                    "Información secundaria",
                    "Datos irrelevantes",
                    "Información desactualizada"
                ],
                "Answer": "A",
                "Explanation": "La primera opción representa un concepto clave del material."
            })
        
        return quiz

    def _save_and_display_quiz(self, quiz: List[Dict[str, Any]], filename_prefix: str) -> None:
        """Guarda y muestra el quiz generado"""
        import datetime
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"quiz_{filename_prefix}_{timestamp}.json"
        filepath = os.path.join(self.storage_dir, filename)
        
        # Guardar quiz
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(quiz, f, ensure_ascii=False, indent=2)
            print(f"\n💾 Quiz guardado en: {filepath}")
        except Exception as e:
            print(f"❌ Error guardando quiz: {e}")
        
        # Mostrar quiz
        print(f"\n🎯 QUIZ GENERADO ({len(quiz)} preguntas):")
        print("="*60)
        
        for i, question in enumerate(quiz, 1):
            print(f"\n📋 Pregunta {i}:")
            print(f"❓ {question['Q']}")
            
            if 'Options' in question:
                for j, option in enumerate(question['Options']):
                    letter = chr(65 + j)  # A, B, C, D
                    print(f"   {letter}. {option}")
            
            print(f"✅ Respuesta correcta: {question['Answer']}")
            if 'Explanation' in question:
                print(f"💡 Explicación: {question['Explanation']}")
            print("-" * 40)
        
        # Opciones adicionales
        self._show_quiz_options(filepath, quiz)

    def _show_quiz_options(self, filepath: str, quiz: List[Dict[str, Any]]) -> None:
        """Muestra opciones adicionales para el quiz"""
        print(f"\n🎯 OPCIONES ADICIONALES:")
        print("1. 🎮 Tomar el quiz ahora")
        print("2. 🔄 Generar otro quiz")
        print("3. 📝 Modificar preguntas")
        print("4. 📤 Exportar quiz")
        print("0. ✅ Finalizar")
        
        while True:
            try:
                choice = input("\nSelecciona opción: ").strip()
                
                if choice == "0":
                    print("✅ Generación de quiz completada.")
                    break
                elif choice == "1":
                    self._take_quiz_interactive(quiz)
                    break
                elif choice == "2":
                    print("🔄 Redirigiendo a generación de otro quiz...")
                    return
                elif choice == "3":
                    self._modify_quiz(filepath, quiz)
                    break
                elif choice == "4":
                    self._export_quiz(filepath, quiz)
                    break
                else:
                    print("❌ Opción inválida.")
                    
            except KeyboardInterrupt:
                print("\n👋 Finalizando...")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

    def _take_quiz_interactive(self, quiz: List[Dict[str, Any]]) -> None:
        """Permite tomar el quiz de forma interactiva"""
        print(f"\nTomando quiz interactivo")
        print("-"*50)
        print("📚 Responde las preguntas del quiz")
        print("• Ingresa tu respuesta (A, B, C, D, etc.)")
        print("• Escribe 'salir' para terminar")
        print("="*50)
        
        correct_answers = 0
        total_questions = len(quiz)
        
        for i, question in enumerate(quiz, 1):
            print(f"\n📋 Pregunta {i}/{total_questions}")
            print(f"❓ {question['Q']}")
            
            if 'Options' in question:
                for j, option in enumerate(question['Options']):
                    letter = chr(65 + j)
                    print(f"   {letter}. {option}")
            
            user_answer = input("\nTu respuesta: ").strip().upper()
            
            if user_answer == "SALIR":
                print("Terminando quiz...")
                break
            
            correct_answer = question['Answer'].upper()
            
            if user_answer == correct_answer:
                correct_answers += 1
                print("🎉 ¡Correcto!")
            else:
                print(f"❌ Incorrecto. La respuesta correcta es: {correct_answer}")
            
            if 'Explanation' in question:
                print(f"💡 Explicación: {question['Explanation']}")
            
            print("-" * 30)
        
        # Mostrar resultados
        if total_questions > 0:
            percentage = (correct_answers / total_questions) * 100
            print(f"\n📊 RESULTADOS DEL QUIZ:")
            print(f"✅ Respuestas correctas: {correct_answers}/{total_questions}")
            print(f"📈 Porcentaje: {percentage:.1f}%")
            
            if percentage >= 90:
                print("🏆 ¡Excelente! Dominas el tema.")
            elif percentage >= 70:
                print("👍 Buen trabajo, sigue practicando.")
            elif percentage >= 50:
                print("📚 Necesitas repasar más.")
            else:
                print("📖 Te recomiendo estudiar más el material.")

    def list_saved_quizzes(self) -> None:
        """Lista todos los quizzes guardados"""
        print("\n📚 QUIZZES GUARDADOS:")
        print("="*40)
        
        if not os.path.exists(self.storage_dir):
            print("❌ No hay quizzes guardados.")
            return
        
        files = [f for f in os.listdir(self.storage_dir) if f.endswith('.json')]
        
        if not files:
            print("❌ No hay quizzes guardados.")
            return
        
        for i, filename in enumerate(files, 1):
            filepath = os.path.join(self.storage_dir, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    quiz = json.load(f)
                print(f"{i}. {filename} ({len(quiz)} preguntas)")
            except Exception as e:
                print(f"{i}. {filename} (error leyendo)")
        
        print(f"\nTotal: {len(files)} archivos de quiz")

    # Métodos para generar otros tipos de quiz
    def _generate_ai_true_false(self, text: str, num_questions: int) -> List[Dict[str, Any]]:
        """Genera quiz de verdadero/falso usando IA"""
        try:
            prompt = f"""
            Genera {num_questions} preguntas de verdadero/falso basadas en el siguiente contenido:
            
            CONTENIDO:
            {text}
            
            FORMATO REQUERIDO:
            - Cada pregunta debe ser una afirmación clara
            - La respuesta debe ser "Verdadero" o "Falso"
            - Las afirmaciones deben ser específicas y verificables
            - Usa un lenguaje claro y académico
            
            RESPONDE SOLO EN FORMATO JSON:
            [
                {{
                    "Q": "Afirmación 1",
                    "Answer": "Verdadero",
                    "Explanation": "Explicación de por qué es verdadero/falso"
                }},
                ...
            ]
            
            IMPORTANTE: Responde únicamente con el JSON, sin texto adicional.
            """
            
            response = self.model.generate_content(prompt)
            ai_text = response.text.strip()
            
            if ai_text.startswith("```json"):
                ai_text = ai_text[7:]
            if ai_text.endswith("```"):
                ai_text = ai_text[:-3]
            
            quiz = json.loads(ai_text)
            return quiz if isinstance(quiz, list) else self._generate_simple_true_false(text, num_questions)
                
        except Exception as e:
            print(f"❌ Error generando quiz V/F con IA: {e}")
            return self._generate_simple_true_false(text, num_questions)

    def _generate_simple_true_false(self, text: str, num_questions: int) -> List[Dict[str, Any]]:
        """Genera quiz simple de verdadero/falso"""
        print("📝 Generando quiz básico de verdadero/falso...")
        
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        quiz = []
        
        for i in range(min(num_questions, len(sentences))):
            if i < len(sentences):
                sentence = sentences[i]
                if len(sentence) > 20:
                    # Alternar entre verdadero y falso
                    is_true = i % 2 == 0
                    quiz.append({
                        "Q": f"La siguiente afirmación es correcta: '{sentence[:50]}...'",
                        "Answer": "Verdadero" if is_true else "Falso",
                        "Explanation": f"Esta afirmación es {'correcta' if is_true else 'incorrecta'} según el contenido."
                    })
        
        return quiz

    def _generate_ai_fill_blank(self, text: str, num_questions: int) -> List[Dict[str, Any]]:
        """Genera quiz de completar espacios usando IA"""
        try:
            prompt = f"""
            Genera {num_questions} preguntas de completar espacios basadas en el siguiente contenido:
            
            CONTENIDO:
            {text}
            
            FORMATO REQUERIDO:
            - Cada pregunta debe tener un espacio en blanco marcado con "_____"
            - La respuesta debe ser la palabra o frase que completa el espacio
            - Las preguntas deben ser educativas y claras
            
            RESPONDE SOLO EN FORMATO JSON:
            [
                {{
                    "Q": "Pregunta con _____ en blanco",
                    "Answer": "respuesta_correcta",
                    "Explanation": "Explicación de la respuesta"
                }},
                ...
            ]
            
            IMPORTANTE: Responde únicamente con el JSON, sin texto adicional.
            """
            
            response = self.model.generate_content(prompt)
            ai_text = response.text.strip()
            
            if ai_text.startswith("```json"):
                ai_text = ai_text[7:]
            if ai_text.endswith("```"):
                ai_text = ai_text[:-3]
            
            quiz = json.loads(ai_text)
            return quiz if isinstance(quiz, list) else self._generate_simple_fill_blank(text, num_questions)
                
        except Exception as e:
            print(f"❌ Error generando quiz de completar con IA: {e}")
            return self._generate_simple_fill_blank(text, num_questions)

    def _generate_simple_fill_blank(self, text: str, num_questions: int) -> List[Dict[str, Any]]:
        """Genera quiz simple de completar espacios"""
        print("📝 Generando quiz básico de completar espacios...")
        
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        quiz = []
        
        for i in range(min(num_questions, len(sentences))):
            if i < len(sentences):
                sentence = sentences[i]
                words = sentence.split()
                if len(words) > 3:
                    # Tomar una palabra del medio para el espacio en blanco
                    blank_word = words[len(words)//2]
                    question = sentence.replace(blank_word, "_____")
                    quiz.append({
                        "Q": question,
                        "Answer": blank_word,
                        "Explanation": f"La palabra '{blank_word}' completa correctamente la oración."
                    })
        
        return quiz

    def _generate_ai_open_questions(self, text: str, num_questions: int) -> List[Dict[str, Any]]:
        """Genera quiz de preguntas abiertas usando IA"""
        try:
            prompt = f"""
            Genera {num_questions} preguntas abiertas basadas en el siguiente contenido:
            
            CONTENIDO:
            {text}
            
            FORMATO REQUERIDO:
            - Cada pregunta debe requerir una respuesta elaborada
            - Incluye una respuesta modelo como referencia
            - Las preguntas deben fomentar el pensamiento crítico
            
            RESPONDE SOLO EN FORMATO JSON:
            [
                {{
                    "Q": "Pregunta abierta 1",
                    "Answer": "Respuesta modelo detallada",
                    "Explanation": "Puntos clave que debe incluir la respuesta"
                }},
                ...
            ]
            
            IMPORTANTE: Responde únicamente con el JSON, sin texto adicional.
            """
            
            response = self.model.generate_content(prompt)
            ai_text = response.text.strip()
            
            if ai_text.startswith("```json"):
                ai_text = ai_text[7:]
            if ai_text.endswith("```"):
                ai_text = ai_text[:-3]
            
            quiz = json.loads(ai_text)
            return quiz if isinstance(quiz, list) else self._generate_simple_open_questions(text, num_questions)
                
        except Exception as e:
            print(f"❌ Error generando preguntas abiertas con IA: {e}")
            return self._generate_simple_open_questions(text, num_questions)

    def _generate_simple_open_questions(self, text: str, num_questions: int) -> List[Dict[str, Any]]:
        """Genera quiz simple de preguntas abiertas"""
        print("📝 Generando quiz básico de preguntas abiertas...")
        
        quiz = []
        for i in range(num_questions):
            quiz.append({
                "Q": f"Explica detalladamente el concepto {i+1} del contenido estudiado.",
                "Answer": f"Respuesta modelo para el concepto {i+1}: Debe incluir definición, características principales y ejemplos del contenido.",
                "Explanation": "La respuesta debe ser completa, estructurada y basada en el material estudiado."
            })
        
        return quiz

    def _generate_ai_mixed(self, text: str, num_questions: int) -> List[Dict[str, Any]]:
        """Genera quiz mixto usando IA"""
        try:
            prompt = f"""
            Genera {num_questions} preguntas mixtas basadas en el siguiente contenido:
            
            CONTENIDO:
            {text}
            
            FORMATO REQUERIDO:
            - Combina diferentes tipos: opción múltiple, verdadero/falso, completar espacios
            - Cada pregunta debe especificar su tipo
            - Mantén variedad en los tipos de preguntas
            
            RESPONDE SOLO EN FORMATO JSON:
            [
                {{
                    "Q": "Pregunta 1",
                    "Type": "multiple_choice",
                    "Options": ["A", "B", "C", "D"],
                    "Answer": "A",
                    "Explanation": "Explicación"
                }},
                {{
                    "Q": "Afirmación 2",
                    "Type": "true_false",
                    "Answer": "Verdadero",
                    "Explanation": "Explicación"
                }},
                ...
            ]
            
            IMPORTANTE: Responde únicamente con el JSON, sin texto adicional.
            """
            
            response = self.model.generate_content(prompt)
            ai_text = response.text.strip()
            
            if ai_text.startswith("```json"):
                ai_text = ai_text[7:]
            if ai_text.endswith("```"):
                ai_text = ai_text[:-3]
            
            quiz = json.loads(ai_text)
            return quiz if isinstance(quiz, list) else self._generate_simple_mixed(text, num_questions)
                
        except Exception as e:
            print(f"❌ Error generando quiz mixto con IA: {e}")
            return self._generate_simple_mixed(text, num_questions)

    def _generate_simple_mixed(self, text: str, num_questions: int) -> List[Dict[str, Any]]:
        """Genera quiz simple mixto"""
        print("📝 Generando quiz básico mixto...")
        
        quiz = []
        for i in range(num_questions):
            if i % 3 == 0:  # Opción múltiple
                quiz.append({
                    "Q": f"Pregunta {i+1} de opción múltiple sobre el contenido",
                    "Type": "multiple_choice",
                    "Options": ["Opción A", "Opción B", "Opción C", "Opción D"],
                    "Answer": "A",
                    "Explanation": "Explicación de la respuesta correcta."
                })
            elif i % 3 == 1:  # Verdadero/Falso
                quiz.append({
                    "Q": f"Afirmación {i+1}: El contenido contiene información relevante.",
                    "Type": "true_false",
                    "Answer": "Verdadero",
                    "Explanation": "El contenido estudiado contiene información relevante."
                })
            else:  # Completar espacios
                quiz.append({
                    "Q": f"El concepto {i+1} es importante para _____ el tema.",
                    "Type": "fill_blank",
                    "Answer": "comprender",
                    "Explanation": "La palabra 'comprender' completa correctamente la oración."
                })
        
        return quiz

    def _generate_ai_topic(self, text: str, num_questions: int, topic: str) -> List[Dict[str, Any]]:
        """Genera quiz sobre tema específico usando IA"""
        try:
            prompt = f"""
            Genera {num_questions} preguntas sobre el tema específico "{topic}" basadas en el siguiente contenido:
            
            CONTENIDO:
            {text}
            
            TEMA ESPECÍFICO: {topic}
            
            FORMATO REQUERIDO:
            - Todas las preguntas deben estar relacionadas con el tema "{topic}"
            - Usa diferentes tipos de preguntas
            - Enfócate en aspectos específicos del tema
            
            RESPONDE SOLO EN FORMATO JSON:
            [
                {{
                    "Q": "Pregunta específica sobre {topic}",
                    "Type": "multiple_choice",
                    "Options": ["A", "B", "C", "D"],
                    "Answer": "A",
                    "Explanation": "Explicación relacionada con {topic}"
                }},
                ...
            ]
            
            IMPORTANTE: Responde únicamente con el JSON, sin texto adicional.
            """
            
            response = self.model.generate_content(prompt)
            ai_text = response.text.strip()
            
            if ai_text.startswith("```json"):
                ai_text = ai_text[7:]
            if ai_text.endswith("```"):
                ai_text = ai_text[:-3]
            
            quiz = json.loads(ai_text)
            return quiz if isinstance(quiz, list) else self._generate_simple_topic(text, num_questions, topic)
                
        except Exception as e:
            print(f"❌ Error generando quiz de tema con IA: {e}")
            return self._generate_simple_topic(text, num_questions, topic)

    def _generate_simple_topic(self, text: str, num_questions: int, topic: str) -> List[Dict[str, Any]]:
        """Genera quiz simple sobre tema específico"""
        print(f"📝 Generando quiz básico sobre {topic}...")
        
        quiz = []
        for i in range(num_questions):
            quiz.append({
                "Q": f"¿Qué información importante se menciona sobre {topic}?",
                "Type": "multiple_choice",
                "Options": [
                    f"Información relevante sobre {topic}",
                    f"Datos secundarios de {topic}",
                    f"Información irrelevante",
                    f"Datos desactualizados"
                ],
                "Answer": "A",
                "Explanation": f"La primera opción contiene información relevante sobre {topic}."
            })
        
        return quiz

    def _modify_quiz(self, filepath: str, quiz: List[Dict[str, Any]]) -> None:
        """Permite modificar preguntas del quiz"""
        print(f"\n📝 MODIFICAR QUIZ:")
        print("Selecciona la pregunta a modificar (número) o '0' para cancelar:")
        
        for i, question in enumerate(quiz, 1):
            print(f"{i}. {question['Q'][:50]}...")
        
        try:
            choice = int(input("\nNúmero de pregunta: "))
            if 1 <= choice <= len(quiz):
                question = quiz[choice - 1]
                print(f"\n📋 Pregunta actual:")
                print(f"❓ {question['Q']}")
                print(f"✅ Respuesta: {question['Answer']}")
                
                new_question = input(f"\nNueva pregunta (Enter para mantener): ").strip()
                new_answer = input(f"Nueva respuesta (Enter para mantener): ").strip()
                
                if new_question:
                    question['Q'] = new_question
                if new_answer:
                    question['Answer'] = new_answer
                
                # Guardar cambios
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(quiz, f, ensure_ascii=False, indent=2)
                
                print("✅ Pregunta modificada y guardada.")
            else:
                print("❌ Número inválido.")
        except ValueError:
            print("❌ Entrada inválida.")
        except Exception as e:
            print(f"❌ Error: {e}")

    def _export_quiz(self, filepath: str, quiz: List[Dict[str, Any]]) -> None:
        """Exporta quiz en diferentes formatos"""
        print(f"\n📤 EXPORTAR QUIZ:")
        print("1. 📄 Exportar como texto plano")
        print("2. 📊 Exportar como CSV")
        print("3. 📋 Copiar al portapapeles")
        print("0. Cancelar")
        
        try:
            choice = input("\nSelecciona formato: ").strip()
            
            if choice == "1":
                self._export_as_text(quiz)
            elif choice == "2":
                self._export_as_csv(quiz)
            elif choice == "3":
                self._copy_to_clipboard(quiz)
            elif choice == "0":
                print("❌ Exportación cancelada.")
            else:
                print("❌ Opción inválida.")
                
        except Exception as e:
            print(f"❌ Error exportando: {e}")

    def _export_as_text(self, quiz: List[Dict[str, Any]]) -> None:
        """Exporta quiz como texto plano"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"quiz_export_{timestamp}.txt"
        filepath = os.path.join(self.storage_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("🎯 QUIZ EXPORTADO - StudyBox\n")
                f.write("="*50 + "\n\n")
                
                for i, question in enumerate(quiz, 1):
                    f.write(f"📋 Pregunta {i}:\n")
                    f.write(f"❓ {question['Q']}\n")
                    
                    if 'Options' in question:
                        for j, option in enumerate(question['Options']):
                            letter = chr(65 + j)
                            f.write(f"   {letter}. {option}\n")
                    
                    f.write(f"✅ Respuesta: {question['Answer']}\n")
                    if 'Explanation' in question:
                        f.write(f"💡 Explicación: {question['Explanation']}\n")
                    f.write("-" * 40 + "\n\n")
            
            print(f"✅ Quiz exportado como texto: {filepath}")
        except Exception as e:
            print(f"❌ Error exportando como texto: {e}")

    def _export_as_csv(self, quiz: List[Dict[str, Any]]) -> None:
        """Exporta quiz como CSV"""
        import datetime
        import csv
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"quiz_export_{timestamp}.csv"
        filepath = os.path.join(self.storage_dir, filename)
        
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Pregunta', 'Opciones', 'Respuesta', 'Explicación'])
                
                for question in quiz:
                    options = ' | '.join(question.get('Options', []))
                    explanation = question.get('Explanation', '')
                    writer.writerow([question['Q'], options, question['Answer'], explanation])
            
            print(f"✅ Quiz exportado como CSV: {filepath}")
        except Exception as e:
            print(f"❌ Error exportando como CSV: {e}")

    def _copy_to_clipboard(self, quiz: List[Dict[str, Any]]) -> None:
        """Copia quiz al portapapeles"""
        try:
            import pyperclip
            
            text = "🎯 QUIZ - StudyBox\n" + "="*30 + "\n\n"
            for i, question in enumerate(quiz, 1):
                text += f"{i}. {question['Q']}\n"
                if 'Options' in question:
                    for j, option in enumerate(question['Options']):
                        letter = chr(65 + j)
                        text += f"   {letter}. {option}\n"
                text += f"   Respuesta: {question['Answer']}\n\n"
            
            pyperclip.copy(text)
            print("✅ Quiz copiado al portapapeles.")
        except ImportError:
            print("❌ pyperclip no está instalado. Instálalo con: pip install pyperclip")
        except Exception as e:
            print(f"❌ Error copiando al portapapeles: {e}")
