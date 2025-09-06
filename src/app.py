from .file_manager import FileManager
from .content_processor import ContentProcessor
from .tools.summary_tool import SummaryTool
from .tools.flashcard_tool import FlashcardTool
from .tools.quiz_tool import QuizTool

class StudyBoxApp:
    def __init__(self):
        self.files = []
        self.texts = []
        self.tools = []

    def upload_file(self, file):
        try: 
            saved_path = FileManager.save_file(file) 
            self.files.append(saved_path) 
            print(f"[+] Archivo '{file}' guardado en: {saved_path}")
        except FileNotFoundError as e:
            print(f"❌ Error al guardar el archivo: {e}")

    def process_files(self):
        print("[*] Procesando archivos...")
        self.texts.clear()
        for file in self.files:
            if file.endswith(".mp3") or file.endswith(".wav"):
                text = ContentProcessor.process_audio(file)
            else:
                text = FileManager.extract_text(file)

            text = ContentProcessor.clean_text(text)
            self.texts.append(text)
            print(f"    - Procesado {file}: {text[:50]}...")

    def add_tool(self, tool_name):
        self.tools.append(tool_name)
        print(f"[+] Herramienta '{tool_name}' agregada.")

    def run_tools(self):
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
                    cards = FlashcardTool.generate_flashcards(text)
                    for c in cards:
                        print(f"Q: {c['Q']} | A: {c['A']}")
                elif tool.lower() == "quiz":
                    quiz = QuizTool.generate_quiz(text, 2)
                    for q in quiz:
                        print(f"Q: {q['Q']} | Opciones: {q['Options']}")
                else:
                    print(f"❌ Herramienta '{tool}' no reconocida.")
