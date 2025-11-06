import os
from .file_manager import FileManager
from .content_processor import ContentProcessor
from .tools.chatbot_tool import ChatbotTool
from .tools.audio_generator_tool import AudioGeneratorTool
from .tools.audio_player_tool import AudioPlayerTool
from .tools.flashcard_tool import FlashcardTool
from .tools.quiz_tool import QuizTool

class StudyBoxApp:
    def __init__(self):
        self.files = []
        self.texts = []
        self.content_processor = ContentProcessor()
        self.chatbot = ChatbotTool()
        self.audio_generator = AudioGeneratorTool()
        self.audio_player = AudioPlayerTool()
        self.flashcard_generator = FlashcardTool()
        self.quiz_generator = QuizTool()

    def upload_file(self, file):
        try: 
            saved_path = FileManager.save_file(file) 
            self.files.append(saved_path) 
            print(f"[+] Archivo '{file}' guardado en: {saved_path}")
        except:
            print(f"Error al guardar el archivo")

    def process_files(self):
        print("\nSelecciona los archivos que quieres procesar")
        
        all_files = self._get_all_available_files()
        
        if not all_files:
            print("No hay archivos disponibles para procesar.")
            return
        
        selected_files = self._show_file_selection_menu(all_files)
        
        if not selected_files:
            print("No se seleccionaron archivos.")
            return
        
        self._process_selected_files(selected_files)

    def _get_all_available_files(self):
        all_files = []
        
        for file_path in self.files:
            if os.path.exists(file_path):
                all_files.append(file_path)
        
        storage_files = FileManager.list_files()
        for filename in storage_files:
            file_path = os.path.join(FileManager.STORAGE_DIR, filename)
            if file_path not in all_files and os.path.exists(file_path):
                all_files.append(file_path)
        
        return all_files

    def _show_file_selection_menu(self, files):
        print(f"\nArchivos disponibles ({len(files)}):")
        print("-" * 50)
        
        for i in range(len(files)):
            file_path = files[i]
            filename = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            print(f"{i+1}. {filename} ({file_size} bytes)")
        
        print("-" * 50)
        print("Opciones:")
        print("  - Numeros separados por comas (ej: 1,3,5)")
        print("  - 'todos' para procesar todos")
        print("  - '0' para cancelar")
        
        while True:
            selection = input("\nSelecciona archivos: ").strip().lower()
            
            if selection == "0":
                return []
            elif selection == "todos":
                return files
            else:
                try:
                    partes = selection.split(",")
                    indices = []
                    for x in partes:
                        indices.append(int(x.strip()))
                    selected_files = []
                    
                    for idx in indices:
                        if idx >= 1 and idx <= len(files):
                            selected_files.append(files[idx-1])
                        else:
                            print(f"Numero {idx} fuera de rango")
                    
                    if len(selected_files) > 0:
                        print(f"\nArchivos seleccionados:")
                        for file_path in selected_files:
                            print(f"   {os.path.basename(file_path)}")
                        return selected_files
                    else:
                        print("No se seleccionaron archivos validos.")
                        
                except:
                    print("Formato invalido.")

    def _process_selected_files(self, files_to_process):
        print(f"\nProcesando {len(files_to_process)} archivo(s)...")
        self.texts = []
        
        for file in files_to_process:
            try:
                print(f"    Procesando: {os.path.basename(file)}")
                
                if file.endswith(".mp3") or file.endswith(".wav"):
                    text = self.content_processor.process_audio(file)
                else:
                    text = FileManager.extract_text(file)

                text = self.content_processor.clean_text(text)
                
                if text and len(text) > 10:
                    improved_text = self.content_processor.process_text_with_ai(text)
                    if improved_text:
                        text = improved_text

                self.texts.append(text)
                print(f"    Listo: {text[:50]}...")
                
            except:
                error_msg = f"Error procesando {file}"
                print(f"    Error: {error_msg}")
                self.texts.append(error_msg)

    def start_chatbot(self):
        if not self.texts:
            print("No hay contenido procesado. Procesa archivos primero.")
            return
        
        print(f"Iniciando chatbot con {len(self.texts)} archivo(s) procesado(s)...")
        self.chatbot.start_chat_session(self.texts)

    def start_audio_generator(self):
        if not self.texts:
            print("No hay contenido procesado. Procesa archivos primero.")
            return
        
        print(f"Iniciando generador de audio con {len(self.texts)} archivo(s) procesado(s)...")
        self.audio_generator.generate_audio_content(self.texts)

    def start_audio_player(self):
        print("Abriendo el reproductor de audio...")
        self.audio_player.show_audio_menu()

    def start_flashcard_generator(self):
        if not self.texts:
            print("No hay contenido procesado. Procesa archivos primero.")
            return
        
        print(f"Iniciando generador de flashcards con {len(self.texts)} archivo(s) procesado(s)...")
        self.flashcard_generator.generate_flashcards(self.texts)

    def start_quiz_generator(self):
        if not self.texts:
            print("No hay contenido procesado. Procesa archivos primero.")
            return
        
        print(f"Iniciando generador de quiz con {len(self.texts)} archivo(s) procesado(s)...")
        self.quiz_generator.generate_quiz(self.texts)

    def show_key_concepts(self):
        print("Extrayendo conceptos clave...")
        if not self.texts:
            print("No hay textos procesados. Usa 'Procesar archivos' primero.")
            return
        
        all_concepts = []
        i = 0
        for text in self.texts:
            i = i + 1
            print(f"\nConceptos del archivo {i}:")
            concepts = self.content_processor.extract_key_concepts(text)
            for concept in concepts:
                all_concepts.append(concept)
            
            if concepts:
                j = 0
                for concept in concepts:
                    j = j + 1
                    print(f"   {j}. {concept}")
            else:
                print("   No se pudieron extraer conceptos.")
        
        unique_concepts = list(set(all_concepts))
        if unique_concepts:
            print(f"\nConceptos unicos encontrados ({len(unique_concepts)}):")
            contador = 0
            for concept in unique_concepts:
                if contador < 15:
                    print(f"   {concept}")
                    contador = contador + 1

    def reload_files_from_storage(self):
        print("Recargando archivos desde storage...")
        self.files = []
        
        storage_files = FileManager.list_files()
        if not storage_files:
            print("No hay archivos en storage.")
            return
        
        for filename in storage_files:
            file_path = os.path.join(FileManager.STORAGE_DIR, filename)
            self.files.append(file_path)
            print(f"    Cargado: {filename}")
        
        print(f"{len(self.files)} archivo(s) cargado(s) desde storage.")
