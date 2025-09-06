import os
from typing import List, Dict, Any, Optional
from .file_manager import FileManager
from .content_processor import ContentProcessor
from .tools.chatbot_tool import ChatbotTool
from .tools.audio_generator_tool import AudioGeneratorTool
from .tools.audio_player_tool import AudioPlayerTool
from .tools.flashcard_tool import FlashcardTool
from .tools.quiz_tool import QuizTool

class StudyBoxApp:
    def __init__(self) -> None:
        self.files: List[str] = []
        self.texts: List[str] = []
        self.content_processor = ContentProcessor()
        self.chatbot = ChatbotTool()
        self.audio_generator = AudioGeneratorTool()
        self.audio_player = AudioPlayerTool()
        self.flashcard_generator = FlashcardTool()
        self.quiz_generator = QuizTool()

    def upload_file(self, file: str) -> None:
        try: 
            saved_path: str = FileManager.save_file(file) 
            self.files.append(saved_path) 
            print(f"[+] Archivo '{file}' guardado en: {saved_path}")
        except FileNotFoundError as e:
            print(f"❌ Error al guardar el archivo: {e}")

    def process_files(self) -> None:
        print("\n=== 📄 Seleccionar Archivos para Procesar ===")
        
        all_files = self._get_all_available_files()
        
        if not all_files:
            print("⚠️ No hay archivos disponibles para procesar.")
            print("   Sube archivos primero o asegúrate de que haya archivos en storage.")
            return
        
        selected_files = self._show_file_selection_menu(all_files)
        
        if not selected_files:
            print("❌ No se seleccionaron archivos.")
            return
        
        self._process_selected_files(selected_files)

    def _get_all_available_files(self) -> List[str]:
        all_files: List[str] = []
        
        for file_path in self.files:
            if os.path.exists(file_path):
                all_files.append(file_path)
        
        storage_files = FileManager.list_files()
        for filename in storage_files:
            file_path = os.path.join(FileManager.STORAGE_DIR, filename)
            if file_path not in all_files and os.path.exists(file_path):
                all_files.append(file_path)
        
        return all_files

    def _show_file_selection_menu(self, files: List[str]) -> List[str]:
        print(f"\n📋 Archivos disponibles ({len(files)}):")
        print("=" * 50)
        
        for i, file_path in enumerate(files, 1):
            filename = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            print(f"{i:2d}. {filename} ({file_size} bytes)")
        
        print("=" * 50)
        print("Opciones:")
        print("  • Ingresa números separados por comas (ej: 1,3,5)")
        print("  • Ingresa 'todos' para procesar todos los archivos")
        print("  • Ingresa '0' para cancelar")
        
        while True:
            selection = input("\nSelecciona archivos: ").strip().lower()
            
            if selection == "0":
                return []
            elif selection == "todos":
                return files
            else:
                try:
                    indices = [int(x.strip()) for x in selection.split(",")]
                    selected_files: List[str] = []
                    
                    for idx in indices:
                        if 1 <= idx <= len(files):
                            selected_files.append(files[idx-1])
                        else:
                            print(f"❌ Número {idx} no válido. Rango: 1-{len(files)}")
                    
                    if selected_files:
                        print(f"\n✅ Archivos seleccionados ({len(selected_files)}):")
                        for file_path in selected_files:
                            print(f"   • {os.path.basename(file_path)}")
                        return selected_files
                    else:
                        print("❌ No se seleccionaron archivos válidos.")
                        
                except ValueError:
                    print("❌ Formato inválido. Usa números separados por comas.")

    def _process_selected_files(self, files_to_process: List[str]) -> None:
        print(f"\n[*] Procesando {len(files_to_process)} archivo(s) seleccionado(s)...")
        self.texts.clear()
        
        for file in files_to_process:
            try:
                print(f"    📄 Procesando: {os.path.basename(file)}")
                
                text: str
                if file.endswith(".mp3") or file.endswith(".wav"):
                    text = self.content_processor.process_audio(file)
                else:
                    text = FileManager.extract_text(file)

                text = self.content_processor.clean_text(text)
                
                if text and len(text) > 10:
                    improved_text: str = self.content_processor.process_text_with_ai(text)
                    if improved_text:
                        text = improved_text

                self.texts.append(text)
                print(f"    ✅ Procesado: {text[:50]}...")
                
            except Exception as e:
                error_msg: str = f"Error procesando {file}: {str(e)}"
                print(f"    ❌ {error_msg}")
                self.texts.append(error_msg)

    def start_chatbot(self) -> None:
        if not self.texts:
            print("⚠️ No hay contenido procesado. Procesa archivos primero.")
            return
        
        print(f"🤖 Iniciando chatbot con {len(self.texts)} archivo(s) procesado(s)...")
        self.chatbot.start_chat_session(self.texts)

    def start_audio_generator(self) -> None:
        if not self.texts:
            print("⚠️ No hay contenido procesado. Procesa archivos primero.")
            return
        
        print(f"🎵 Iniciando generador de audio con {len(self.texts)} archivo(s) procesado(s)...")
        self.audio_generator.generate_audio_content(self.texts)

    def start_audio_player(self) -> None:
        print("🎧 Iniciando reproductor de audio...")
        self.audio_player.show_audio_menu()

    def start_flashcard_generator(self) -> None:
        if not self.texts:
            print("⚠️ No hay contenido procesado. Procesa archivos primero.")
            return
        
        print(f"🃏 Iniciando generador de flashcards con {len(self.texts)} archivo(s) procesado(s)...")
        self.flashcard_generator.generate_flashcards(self.texts)

    def start_quiz_generator(self) -> None:
        if not self.texts:
            print("⚠️ No hay contenido procesado. Procesa archivos primero.")
            return
        
        print(f"🎯 Iniciando generador de quiz con {len(self.texts)} archivo(s) procesado(s)...")
        self.quiz_generator.generate_quiz(self.texts)

    def show_key_concepts(self) -> None:
        print("[*] Extrayendo conceptos clave...")
        if not self.texts:
            print("⚠️ No hay textos procesados. Use 'Procesar archivos' primero.")
            return
        
        all_concepts: List[str] = []
        for i, text in enumerate(self.texts):
            print(f"\n📚 Conceptos del archivo {i+1}:")
            concepts: List[str] = self.content_processor.extract_key_concepts(text)
            all_concepts.extend(concepts)
            
            if concepts:
                for j, concept in enumerate(concepts, 1):
                    print(f"   {j}. {concept}")
            else:
                print("   No se pudieron extraer conceptos.")
        
        unique_concepts: List[str] = list(set(all_concepts))
        if unique_concepts:
            print(f"\n🎯 Conceptos únicos encontrados ({len(unique_concepts)}):")
            for concept in unique_concepts[:15]:
                print(f"   • {concept}")

    def reload_files_from_storage(self) -> None:
        print("🔄 Recargando archivos desde storage...")
        self.files.clear()
        
        storage_files: List[str] = FileManager.list_files()
        if not storage_files:
            print("⚠️ No hay archivos en storage.")
            return
        
        for filename in storage_files:
            file_path: str = os.path.join(FileManager.STORAGE_DIR, filename)
            self.files.append(file_path)
            print(f"    📄 Cargado: {filename}")
        
        print(f"✅ {len(self.files)} archivo(s) cargado(s) desde storage.")
