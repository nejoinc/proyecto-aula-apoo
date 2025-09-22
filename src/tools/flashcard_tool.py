import os
import json
from typing import List, Dict, Any, Optional
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class FlashcardTool:
    def __init__(self):
        """Inicializa el generador de flashcards con IA"""
        try:
            api_key = os.getenv('GEMINI_API_KEY')
            if api_key and api_key != 'tu_api_key_aqui':
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel('gemini-1.5-flash')
                self.ai_available = True
            else:
                self.model = None
                self.ai_available = False
                print("⚠️ API key de Gemini no configurada para Flashcards. Funcionando en modo simulado.")
        except Exception as e:
            print(f"⚠️ IA no disponible para Flashcards: {e}")
            self.model = None
            self.ai_available = False
        
        # Directorio para almacenar flashcards
        self.storage_dir = os.path.join(os.path.dirname(__file__), "..", "storage", "flashcards")
        os.makedirs(self.storage_dir, exist_ok=True)

    def generate_flashcards(self, processed_texts: List[str]) -> None:
        """Genera flashcards inteligentes usando IA"""
        print("\nGenerador de flashcards")
        print("-"*60)
        
        if not processed_texts:
            print("❌ No hay contenido procesado disponible.")
            print("💡 Procesa algunos archivos primero para generar flashcards.")
            return
        
        print("Contenido disponible para generar flashcards:")
        for i, text in enumerate(processed_texts, 1):
            preview = text[:100] + "..." if len(text) > 100 else text
            print(f"{i}. {preview}")
        
        print("\nOpciones:")
        print("1. Automáticas")
        print("2. Por tema")
        print("3. Conceptos clave")
        print("4. Definiciones")
        print("5. Ejemplos")
        print("0. Volver")
        
        while True:
            try:
                choice = input("\nSelecciona opción: ").strip()
                
                if choice == "0":
                    print("👋 Regresando al menú principal...")
                    break
                elif choice == "1":
                    self._generate_automatic_flashcards(processed_texts)
                    break
                elif choice == "2":
                    self._generate_topic_flashcards(processed_texts)
                    break
                elif choice == "3":
                    self._generate_concept_flashcards(processed_texts)
                    break
                elif choice == "4":
                    self._generate_definition_flashcards(processed_texts)
                    break
                elif choice == "5":
                    self._generate_example_flashcards(processed_texts)
                    break
                else:
                    print("Opción inválida. Selecciona 1-5 o 0.")
                    
            except KeyboardInterrupt:
                print("\n👋 Regresando al menú principal...")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

    def _generate_automatic_flashcards(self, texts: List[str]) -> None:
        """Genera flashcards automáticamente usando IA"""
        print("\nGenerando flashcards automáticas...")
        
        combined_text = "\n\n".join(texts)
        context = combined_text[:8000]  # Limitar contexto
        
        if not self.ai_available:
            flashcards = self._generate_simple_flashcards(context)
        else:
            flashcards = self._generate_ai_flashcards(context, "automáticas")
        
        if flashcards:
            self._save_and_display_flashcards(flashcards, "automaticas")
        else:
            print("No se pudieron generar flashcards.")

    def _generate_topic_flashcards(self, texts: List[str]) -> None:
        """Genera flashcards sobre un tema específico"""
        topic = input("\nTema específico para las flashcards: ").strip()
        if not topic:
            print("❌ Tema no válido.")
            return
        
        print(f"\nGenerando flashcards sobre: {topic}")
        
        combined_text = "\n\n".join(texts)
        context = combined_text[:8000]
        
        if not self.ai_available:
            flashcards = self._generate_simple_flashcards(context, topic)
        else:
            flashcards = self._generate_ai_flashcards(context, f"sobre el tema: {topic}")
        
        if flashcards:
            self._save_and_display_flashcards(flashcards, f"tema_{topic.replace(' ', '_')}")
        else:
            print("No se pudieron generar flashcards.")

    def _generate_concept_flashcards(self, texts: List[str]) -> None:
        """Genera flashcards de conceptos clave"""
        print("\nGenerando flashcards de conceptos clave...")
        
        combined_text = "\n\n".join(texts)
        context = combined_text[:8000]
        
        if not self.ai_available:
            flashcards = self._generate_simple_flashcards(context, "conceptos")
        else:
            flashcards = self._generate_ai_flashcards(context, "conceptos clave y definiciones importantes")
        
        if flashcards:
            self._save_and_display_flashcards(flashcards, "conceptos")
        else:
            print("No se pudieron generar flashcards.")

    def _generate_definition_flashcards(self, texts: List[str]) -> None:
        """Genera flashcards de definiciones"""
        print("\nGenerando flashcards de definiciones...")
        
        combined_text = "\n\n".join(texts)
        context = combined_text[:8000]
        
        if not self.ai_available:
            flashcards = self._generate_simple_flashcards(context, "definiciones")
        else:
            flashcards = self._generate_ai_flashcards(context, "definiciones y términos importantes")
        
        if flashcards:
            self._save_and_display_flashcards(flashcards, "definiciones")
        else:
            print("No se pudieron generar flashcards.")

    def _generate_example_flashcards(self, texts: List[str]) -> None:
        """Genera flashcards de ejemplos"""
        print("\nGenerando flashcards de ejemplos...")
        
        combined_text = "\n\n".join(texts)
        context = combined_text[:8000]
        
        if not self.ai_available:
            flashcards = self._generate_simple_flashcards(context, "ejemplos")
        else:
            flashcards = self._generate_ai_flashcards(context, "ejemplos prácticos y casos de uso")
        
        if flashcards:
            self._save_and_display_flashcards(flashcards, "ejemplos")
        else:
            print("No se pudieron generar flashcards.")

    def _generate_ai_flashcards(self, text: str, prompt_type: str) -> List[Dict[str, str]]:
        """Genera flashcards usando IA"""
        try:
            prompt = f"""
            Genera 8 flashcards educativas de alta calidad basadas en el siguiente contenido:
            
            CONTENIDO:
            {text}
            
            TIPO DE FLASHCARDS: {prompt_type}
            
            FORMATO REQUERIDO:
            - Cada flashcard debe tener una pregunta clara y específica
            - La respuesta debe ser precisa y educativa
            - Las preguntas deben cubrir conceptos importantes del contenido
            - Usa un lenguaje claro y académico
            
            RESPONDE SOLO EN FORMATO JSON:
            [
                {{"Q": "Pregunta 1", "A": "Respuesta 1"}},
                {{"Q": "Pregunta 2", "A": "Respuesta 2"}},
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
            
            flashcards = json.loads(ai_text)
            
            # Validar formato
            if isinstance(flashcards, list) and all(
                isinstance(card, dict) and "Q" in card and "A" in card 
                for card in flashcards
            ):
                return flashcards
            else:
                print("⚠️ Formato de respuesta de IA inválido.")
                return self._generate_simple_flashcards(text)
                
        except json.JSONDecodeError as e:
            print(f"⚠️ Error parseando respuesta de IA: {e}")
            return self._generate_simple_flashcards(text)
        except Exception as e:
            print(f"❌ Error generando flashcards con IA: {e}")
            return self._generate_simple_flashcards(text)

    def _generate_simple_flashcards(self, text: str, topic: str = "") -> List[Dict[str, str]]:
        """Genera flashcards simples como fallback"""
        print("Generando flashcards básicas...")
        
        # Dividir texto en oraciones
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        
        flashcards = []
        for i, sentence in enumerate(sentences[:8]):  # Máximo 8 flashcards
            if len(sentence) > 20:
                # Crear pregunta basada en la oración
                words = sentence.split()
                if len(words) > 3:
                    # Tomar las primeras palabras como pregunta
                    question_words = words[:3]
                    question = " ".join(question_words) + "..."
                    flashcards.append({
                        "Q": f"¿Qué dice sobre {question}?",
                        "A": sentence
                    })
        
        # Si no hay suficientes, crear algunas genéricas
        while len(flashcards) < 5:
            flashcards.append({
                "Q": f"¿Cuál es un concepto importante del contenido?",
                "A": f"Concepto clave {len(flashcards) + 1} del material estudiado."
            })
        
        return flashcards

    def _save_and_display_flashcards(self, flashcards: List[Dict[str, str]], filename_prefix: str) -> None:
        """Guarda y muestra las flashcards generadas"""
        import datetime
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"flashcards_{filename_prefix}_{timestamp}.json"
        filepath = os.path.join(self.storage_dir, filename)
        
        # Guardar flashcards
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(flashcards, f, ensure_ascii=False, indent=2)
            print(f"\n💾 Flashcards guardadas en: {filepath}")
        except Exception as e:
            print(f"❌ Error guardando flashcards: {e}")
        
        # Mostrar flashcards
        print(f"\nFlashcards generadas ({len(flashcards)}):")
        print("-"*60)
        
        for i, card in enumerate(flashcards, 1):
            print(f"\n📋 Flashcard {i}:")
            print(f"❓ Pregunta: {card['Q']}")
            print(f"✅ Respuesta: {card['A']}")
            print("-" * 40)
        
        # Opciones adicionales
        self._show_flashcard_options(filepath, flashcards)

    def _show_flashcard_options(self, filepath: str, flashcards: List[Dict[str, str]]) -> None:
        """Muestra opciones adicionales para las flashcards"""
        print(f"\nOpciones:")
        print("1. 🔄 Generar más flashcards")
        print("2. 📝 Modificar flashcards existentes")
        print("3. 🎮 Modo estudio interactivo")
        print("4. 📤 Exportar flashcards")
        print("0. ✅ Finalizar")
        
        while True:
            try:
                choice = input("\nSelecciona opción: ").strip()
                
                if choice == "0":
                    print("Listo.")
                    break
                elif choice == "1":
                    print("🔄 Redirigiendo a generación de más flashcards...")
                    return  # Volver al menú principal de flashcards
                elif choice == "2":
                    self._modify_flashcards(filepath, flashcards)
                    break
                elif choice == "3":
                    self._interactive_study_mode(flashcards)
                    break
                elif choice == "4":
                    self._export_flashcards(filepath, flashcards)
                    break
                else:
                    print("❌ Opción inválida.")
                    
            except KeyboardInterrupt:
                print("\n👋 Finalizando...")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

    def _modify_flashcards(self, filepath: str, flashcards: List[Dict[str, str]]) -> None:
        """Permite modificar flashcards existentes"""
        print(f"\nModificar flashcards:")
        print("Selecciona la flashcard a modificar (número) o '0' para cancelar:")
        
        for i, card in enumerate(flashcards, 1):
            print(f"{i}. {card['Q'][:50]}...")
        
        try:
            choice = int(input("\nNúmero de flashcard: "))
            if 1 <= choice <= len(flashcards):
                card = flashcards[choice - 1]
                print(f"\n📋 Flashcard actual:")
                print(f"❓ Pregunta: {card['Q']}")
                print(f"✅ Respuesta: {card['A']}")
                
                new_question = input(f"\nNueva pregunta (Enter para mantener): ").strip()
                new_answer = input(f"Nueva respuesta (Enter para mantener): ").strip()
                
                if new_question:
                    card['Q'] = new_question
                if new_answer:
                    card['A'] = new_answer
                
                # Guardar cambios
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(flashcards, f, ensure_ascii=False, indent=2)
                
                print("Flashcard modificada y guardada.")
            else:
                print("❌ Número inválido.")
        except ValueError:
            print("❌ Entrada inválida.")
        except Exception as e:
            print(f"❌ Error: {e}")

    def _interactive_study_mode(self, flashcards: List[Dict[str, str]]) -> None:
        """Modo de estudio interactivo"""
        print(f"\nModo estudio interactivo")
        print("-"*50)
        print("📚 Estudia tus flashcards de forma interactiva")
        print("• Presiona Enter para ver la respuesta")
        print("• Escribe 'siguiente' para pasar a la siguiente")
        print("• Escribe 'salir' para terminar")
        print("="*50)
        
        correct_answers = 0
        total_questions = len(flashcards)
        
        for i, card in enumerate(flashcards, 1):
            print(f"\n📋 Flashcard {i}/{total_questions}")
            print(f"❓ Pregunta: {card['Q']}")
            
            user_input = input("\nPresiona Enter para ver la respuesta: ").strip().lower()
            
            if user_input == "salir":
                print("Terminando sesión de estudio...")
                break
            elif user_input == "siguiente":
                continue
            
            print(f"✅ Respuesta: {card['A']}")
            
            # Preguntar si la respuesta fue correcta
            while True:
                correct = input("\n¿Respondiste correctamente? (s/n): ").strip().lower()
                if correct in ['s', 'si', 'sí', 'y', 'yes']:
                    correct_answers += 1
                    print("Correcto")
                    break
                elif correct in ['n', 'no']:
                    print("Sigue practicando esta tarjeta.")
                    break
                else:
                    print("Responde 's' o 'n'.")
        
        # Mostrar resultados
        if total_questions > 0:
            percentage = (correct_answers / total_questions) * 100
            print(f"\nResultados del estudio:")
            print(f"✅ Respuestas correctas: {correct_answers}/{total_questions}")
            print(f"📈 Porcentaje: {percentage:.1f}%")
            
            if percentage >= 80:
                print("Excelente trabajo!")
            elif percentage >= 60:
                print("Bien, sigue practicando.")
            else:
                print("Necesitas repasar más. ¡Ánimo!")

    def _export_flashcards(self, filepath: str, flashcards: List[Dict[str, str]]) -> None:
        """Exporta flashcards en diferentes formatos"""
        print(f"\nExportar flashcards:")
        print("1. 📄 Exportar como texto plano")
        print("2. 📊 Exportar como CSV")
        print("3. 📋 Copiar al portapapeles")
        print("0. Cancelar")
        
        try:
            choice = input("\nSelecciona formato: ").strip()
            
            if choice == "1":
                self._export_as_text(flashcards)
            elif choice == "2":
                self._export_as_csv(flashcards)
            elif choice == "3":
                self._copy_to_clipboard(flashcards)
            elif choice == "0":
                print("Exportación cancelada.")
            else:
                print("❌ Opción inválida.")
                
        except Exception as e:
            print(f"❌ Error exportando: {e}")

    def _export_as_text(self, flashcards: List[Dict[str, str]]) -> None:
        """Exporta flashcards como texto plano"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"flashcards_export_{timestamp}.txt"
        filepath = os.path.join(self.storage_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("🃏 FLASHCARDS EXPORTADAS - StudyBox\n")
                f.write("="*50 + "\n\n")
                
                for i, card in enumerate(flashcards, 1):
                    f.write(f"📋 Flashcard {i}:\n")
                    f.write(f"❓ Pregunta: {card['Q']}\n")
                    f.write(f"✅ Respuesta: {card['A']}\n")
                    f.write("-" * 40 + "\n\n")
            
            print(f"Flashcards exportadas como texto: {filepath}")
        except Exception as e:
            print(f"❌ Error exportando como texto: {e}")

    def _export_as_csv(self, flashcards: List[Dict[str, str]]) -> None:
        """Exporta flashcards como CSV"""
        import datetime
        import csv
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"flashcards_export_{timestamp}.csv"
        filepath = os.path.join(self.storage_dir, filename)
        
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Pregunta', 'Respuesta'])
                
                for card in flashcards:
                    writer.writerow([card['Q'], card['A']])
            
            print(f"Flashcards exportadas como CSV: {filepath}")
        except Exception as e:
            print(f"❌ Error exportando como CSV: {e}")

    def _copy_to_clipboard(self, flashcards: List[Dict[str, str]]) -> None:
        """Copia flashcards al portapapeles"""
        try:
            import pyperclip
            
            text = "🃏 FLASHCARDS - StudyBox\n" + "="*30 + "\n\n"
            for i, card in enumerate(flashcards, 1):
                text += f"{i}. {card['Q']}\n   Respuesta: {card['A']}\n\n"
            
            pyperclip.copy(text)
            print("Flashcards copiadas al portapapeles.")
        except ImportError:
            print("❌ pyperclip no está instalado. Instálalo con: pip install pyperclip")
        except Exception as e:
            print(f"❌ Error copiando al portapapeles: {e}")

    def list_saved_flashcards(self) -> None:
        """Lista todas las flashcards guardadas"""
        print("\nFlashcards guardadas:")
        print("-"*40)
        
        if not os.path.exists(self.storage_dir):
            print("❌ No hay flashcards guardadas.")
            return
        
        files = [f for f in os.listdir(self.storage_dir) if f.endswith('.json')]
        
        if not files:
            print("❌ No hay flashcards guardadas.")
            return
        
        for i, filename in enumerate(files, 1):
            filepath = os.path.join(self.storage_dir, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    flashcards = json.load(f)
                print(f"{i}. {filename} ({len(flashcards)} tarjetas)")
            except Exception as e:
                print(f"{i}. {filename} (error leyendo)")
        
        print(f"\nTotal: {len(files)} archivos de flashcards")
