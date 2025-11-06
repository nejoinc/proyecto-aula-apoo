import os
import threading
import time
import pygame

class AudioPlayerTool:
    
    def __init__(self):
        self.is_playing = False
        self.current_file = None
        self.pygame_initialized = False
        
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            self.pygame_initialized = True
            print("Reproductor de audio listo")
        except:
            print("Error inicializando reproductor")
            self.pygame_initialized = False

    def play_audio_file(self, file_path):
        if not self.pygame_initialized:
            print("Reproductor no disponible. Instalando pygame...")
            return self._install_and_retry(file_path)
        
        if not os.path.exists(file_path):
            print(f"Archivo no encontrado: {file_path}")
            return False
        
        try:
            if self.is_playing:
                self.stop_audio()
            
            print(f"Cargando: {os.path.basename(file_path)}")
            print("Reproduciendo en consola...")
            
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            
            self.is_playing = True
            self.current_file = file_path
            
            self._show_playback_controls()
            
            return True
            
        except:
            print("Error reproduciendo audio")
            return False

    def stop_audio(self):
        if self.pygame_initialized and self.is_playing:
            pygame.mixer.music.stop()
            self.is_playing = False
            self.current_file = None
            print("Reproduccion detenida")

    def pause_audio(self):
        if not self.pygame_initialized:
            return
            
        if self.is_playing:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.pause()
                print("Reproduccion pausada")
            else:
                pygame.mixer.music.unpause()
                print("Reproduccion reanudada")

    def _show_playback_controls(self):
        print("\nReproduccion en consola")
        print("ENTER: pausar/reanudar")
        print("s + ENTER: detener")
        print("q + ENTER: salir")
        print("Reproduciendo...")
        
        control_thread = threading.Thread(target=self._monitor_controls)
        control_thread.daemon = True
        control_thread.start()
        
        self._show_playback_progress()
        
        if self.is_playing:
            print("Reproduccion completada")
            self.is_playing = False

    def _show_playback_progress(self):
        start_time = time.time()
        
        while self.is_playing and pygame.mixer.music.get_busy():
            elapsed = int(time.time() - start_time)
            print(f"\rReproduciendo... {elapsed}s", end="", flush=True)
            time.sleep(1)
        
        print()

    def _monitor_controls(self):
        try:
            while self.is_playing:
                user_input = input().strip().lower()
                
                if user_input == '':
                    self.pause_audio()
                elif user_input == 's':
                    self.stop_audio()
                    break
                elif user_input == 'q':
                    self.stop_audio()
                    break
                    
        except:
            pass

    def _install_and_retry(self, file_path):
        try:
            import subprocess
            print("Instalando pygame...")
            subprocess.check_call(['py', '-m', 'pip', 'install', 'pygame'])
            print("pygame instalado. Reiniciando reproductor...")
            
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            self.pygame_initialized = True
            
            return self.play_audio_file(file_path)
            
        except:
            print("Error instalando pygame")
            return False

    def list_audio_files(self):
        audio_dir = os.path.join(os.path.dirname(__file__), "..", "storage", "generated_audio")
        
        if not os.path.exists(audio_dir):
            return []
        
        audio_files = []
        for file in os.listdir(audio_dir):
            if file.lower().endswith(('.mp3', '.wav', '.ogg', '.m4a')):
                audio_files.append(os.path.join(audio_dir, file))
        
        return sorted(audio_files)

    def show_audio_menu(self):
        audio_files = self.list_audio_files()
        
        if not audio_files:
            print("No hay archivos de audio disponibles.")
            print("Genera algunos audios primero usando el Generador de Audio.")
            return
        
        print("\n🎵 REPRODUCTOR DE AUDIO INTEGRADO - StudyBox")
        print("="*60)
        print("🔊 Reproduce audio directamente en la consola (sin abrir reproductor externo)")
        print("="*60)
        print("Archivos de audio disponibles:")
        
        i = 1
        for file_path in audio_files:
            filename = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            print(f"{i}. {filename} ({file_size} bytes)")
            i = i + 1
        
        print("="*60)
        print("Opciones de reproduccion:")
        print("Ingresa numero para reproducir archivo EN LA CONSOLA")
        print("Ingresa 'todos' para reproducir secuencialmente")
        print("Ingresa '0' para volver al menu principal")
        print("="*60)
        print("El audio se reproduce directamente aqui")
        
        while True:
            try:
                selection = input("\nSelecciona audio: ").strip().lower()
                
                if selection == "0":
                    print("Regresando al menu principal...")
                    break
                elif selection == "todos":
                    self._play_all_audio_files(audio_files)
                    break
                else:
                    try:
                        index = int(selection) - 1
                        if 0 <= index < len(audio_files):
                            self.play_audio_file(audio_files[index])
                        else:
                            print(f"Numero no valido. Rango: 1-{len(audio_files)}")
                    except:
                        print("Entrada no valida. Usa numeros o 'todos'.")
                        
            except:
                print("\nRegresando al menu principal...")
                break

    def _play_all_audio_files(self, audio_files):
        print(f"\nReproduciendo {len(audio_files)} archivo(s) secuencialmente EN LA CONSOLA...")
        print("Todos los audios se reproduciran directamente aqui")
        
        i = 1
        for file_path in audio_files:
            filename = os.path.basename(file_path)
            print(f"\nArchivo {i}/{len(audio_files)}: {filename}")
            print("Reproduciendo directamente en consola...")
            
            if self.play_audio_file(file_path):
                if i < len(audio_files):
                    print("Preparando siguiente archivo...")
                    time.sleep(2)
            else:
                print(f"Error reproduciendo {filename}")
                break
            i = i + 1
        
        print("\nReproduccion completa finalizada")

    def get_audio_info(self, file_path):
        try:
            if not os.path.exists(file_path):
                return {"error": "Archivo no encontrado"}
            
            file_size = os.path.getsize(file_path)
            file_extension = os.path.splitext(file_path)[1].lower()
            
            info = {
                "filename": os.path.basename(file_path),
                "size": file_size,
                "extension": file_extension,
                "path": file_path
            }
            
            if self.pygame_initialized:
                try:
                    pygame.mixer.music.load(file_path)
                    info["duration"] = "Desconocida"
                except:
                    info["duration"] = "No disponible"
            
            return info
            
        except:
            return {"error": "Error obteniendo info"}

    def cleanup(self):
        if self.pygame_initialized:
            pygame.mixer.quit()
            self.pygame_initialized = False
