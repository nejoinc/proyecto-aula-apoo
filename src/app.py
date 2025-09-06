from typing import List, Dict, Any
from .file_manager import FileManager
from .content_processor import ContentProcessor
from .tools.summary_tool import SummaryTool
from .tools.flashcard_tool import FlashcardTool
from .tools.quiz_tool import QuizTool

class StudyBoxApp:
    def __init__(self):
        self.files: list[str] = []
        self.texts: list[str] = []
        self.tools: list[str] = []

    def upload_file(self, file: str) -> None:
        try: 
            saved_path: str = FileManager.save_file(file) 
            self.files.append(saved_path) 
            print(f"[+] Archivo '{file}' guardado en: {saved_path}")
        except FileNotFoundError as e:
            print(f"❌ Error al guardar el archivo: {e}")

    def process_files(self) -> None:
        print("[*] Procesando archivos...")
        self.texts.clear()
        for file in self.files:
            if file.endswith(".mp3") or file.endswith(".wav"):
                text: str = ContentProcessor.process_audio(file)
            else:
                text: str = FileManager.extract_text(file)

            text: str = ContentProcessor.clean_text(text)
            self.texts.append(text)
            print(f"    - Procesado {file}: {text[:50]}...")

    def add_tool(self, tool_name: str) -> None:
        self.tools.append(tool_name)
        print(f"[+] Herramienta '{tool_name}' agregada.")

    def run_tools(self) -> None:
        print("[*] Ejecutando herramientas...")
        if not self.texts:
            print("⚠️ No hay textos procesados. Use 'Procesar archivos' primero.")
            return

        for tool in self.tools:
            print(f"\n--- Ejecutando {tool} ---")
            for text in self.texts:
                if tool.lower() == "summary":
                    print(SummaryTool.generate_summary(text, "short"))
                elif tool.lower() == "flashcards":
                    cards: List[Dict[str, str]] = FlashcardTool.generate_flashcards(text)
                    for c in cards:
                        print(f"Q: {c['Q']} | A: {c['A']}")
                elif tool.lower() == "quiz":
                    quiz: List[Dict[str, Any]] = QuizTool.generate_quiz(text, 2)
                    for q in quiz:
                        print(f"Q: {q['Q']} | Opciones: {q['Options']}")
                else:
                    print(f"❌ Herramienta '{tool}' no reconocida.")
