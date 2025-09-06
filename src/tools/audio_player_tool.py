import os
import threading
import time
from typing import List, Optional
import pygame
from pathlib import Path

class AudioPlayerTool:
    
    def __init__(self):
        """Inicializa el reproductor de audio"""
        self.is_playing = False
        self.current_file = None
        self.pygame_initialized = False
        
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            self.pygame_initialized = True
            print("✅ Reproductor de audio inicializado")
        except Exception as e:
            print(f"⚠️ Error inicializando reproductor: {e}")
            self.pygame_initialized = False

    def play_audio_file(self, file_path: str) -> bool:
        """Reproduce un archivo de audio"""
        if not self.pygame_initialized:
            print("❌ Reproductor no disponible. Instalando pygame...")
            return self._install_and_retry(file_path)
        
        if not os.path.exists(file_path):
            print(f"❌ Archivo no encontrado: {file_path}")
            return False
        
        try:
            # Detener reproducción actual si hay una
            if self.is_playing:
                self.stop_audio()
            
            print(f"🎵 Cargando audio: {os.path.basename(file_path)}")
            print("🔊 Iniciando reproducción directa en consola...")
            
            # Cargar y reproducir archivo
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            
            self.is_playing = True
            self.current_file = file_path
            
            # Mostrar controles mientras reproduce
            self._show_playback_controls()
            
            return True
            
        except Exception as e:
            print(f"❌ Error reproduciendo audio: {e}")
            return False

    def stop_audio(self) -> None:
        """Detiene la reproducción actual"""
        if self.pygame_initialized and self.is_playing:
            pygame.mixer.music.stop()
            self.is_playing = False
            self.current_file = None
            print("⏹️ Reproducción detenida")

    def pause_audio(self) -> None:
        """Pausa/reanuda la reproducción"""
        if not self.pygame_initialized:
            return
            
        if self.is_playing:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.pause()
                print("⏸️ Reproducción pausada")
            else:
                pygame.mixer.music.unpause()
                print("▶️ Reproducción reanudada")

    def _show_playback_controls(self) -> None:
        """Muestra controles de reproducción y reproduce directamente en consola"""
        print("\n🎧 Reproduciendo directamente en consola...")
        print("• Presiona ENTER para pausar/reanudar")
        print("• Presiona 's' + ENTER para detener")
        print("• Presiona 'q' + ENTER para salir")
        print("• 🔊 Audio reproduciéndose ahora...")
        
        # Hilo para monitorear controles
        control_thread = threading.Thread(target=self._monitor_controls)
        control_thread.daemon = True
        control_thread.start()
        
        # Mostrar progreso mientras reproduce
        self._show_playback_progress()
        
        if self.is_playing:
            print("✅ Reproducción completada")
            self.is_playing = False

    def _show_playback_progress(self) -> None:
        """Muestra progreso de reproducción en consola"""
        start_time = time.time()
        
        while self.is_playing and pygame.mixer.music.get_busy():
            elapsed = int(time.time() - start_time)
            print(f"\r🔊 Reproduciendo... {elapsed}s", end="", flush=True)
            time.sleep(1)
        
        print()  # Nueva línea al final

    def _monitor_controls(self) -> None:
        """Monitorea entrada del usuario para controles"""
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
                    
        except EOFError:
            # Usuario cerró la entrada
            pass

    def _install_and_retry(self, file_path: str) -> bool:
        """Instala pygame y reintenta reproducir"""
        try:
            import subprocess
            print("📦 Instalando pygame...")
            subprocess.check_call(['py', '-m', 'pip', 'install', 'pygame'])
            print("✅ pygame instalado. Reiniciando reproductor...")
            
            # Reinicializar pygame
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            self.pygame_initialized = True
            
            # Reintentar reproducción
            return self.play_audio_file(file_path)
            
        except Exception as e:
            print(f"❌ Error instalando pygame: {e}")
            return False

    def list_audio_files(self) -> List[str]:
        """Lista archivos de audio disponibles"""
        audio_dir = os.path.join(os.path.dirname(__file__), "..", "storage", "generated_audio")
        
        if not os.path.exists(audio_dir):
            return []
        
        audio_files = []
        for file in os.listdir(audio_dir):
            if file.lower().endswith(('.mp3', '.wav', '.ogg', '.m4a')):
                audio_files.append(os.path.join(audio_dir, file))
        
        return sorted(audio_files)

    def show_audio_menu(self) -> None:
        """Muestra menú de selección de archivos de audio"""
        audio_files = self.list_audio_files()
        
        if not audio_files:
            print("❌ No hay archivos de audio disponibles.")
            print("💡 Genera algunos audios primero usando el Generador de Audio.")
            return
        
        print("\n🎵 REPRODUCTOR DE AUDIO INTEGRADO - StudyBox")
        print("="*60)
        print("🔊 Reproduce audio directamente en la consola (sin abrir reproductor externo)")
        print("="*60)
        print("📁 Archivos de audio disponibles:")
        
        for i, file_path in enumerate(audio_files, 1):
            filename = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            print(f"{i:2d}. {filename} ({file_size} bytes)")
        
        print("="*60)
        print("🎧 Opciones de reproducción:")
        print("• Ingresa número para reproducir archivo EN LA CONSOLA")
        print("• Ingresa 'todos' para reproducir secuencialmente")
        print("• Ingresa '0' para volver al menú principal")
        print("="*60)
        print("💡 El audio se reproduce directamente aquí, no se abre reproductor externo")
        
        while True:
            try:
                selection = input("\nSelecciona audio: ").strip().lower()
                
                if selection == "0":
                    print("👋 Regresando al menú principal...")
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
                            print(f"❌ Número no válido. Rango: 1-{len(audio_files)}")
                    except ValueError:
                        print("❌ Entrada no válida. Usa números o 'todos'.")
                        
            except KeyboardInterrupt:
                print("\n👋 Regresando al menú principal...")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

    def _play_all_audio_files(self, audio_files: List[str]) -> None:
        """Reproduce todos los archivos de audio secuencialmente en consola"""
        print(f"\n🔄 Reproduciendo {len(audio_files)} archivo(s) secuencialmente EN LA CONSOLA...")
        print("🔊 Todos los audios se reproducirán directamente aquí")
        
        for i, file_path in enumerate(audio_files, 1):
            filename = os.path.basename(file_path)
            print(f"\n📀 Archivo {i}/{len(audio_files)}: {filename}")
            print("🎧 Reproduciendo directamente en consola...")
            
            if self.play_audio_file(file_path):
                if i < len(audio_files):
                    print("⏭️ Preparando siguiente archivo...")
                    time.sleep(2)
            else:
                print(f"❌ Error reproduciendo {filename}")
                break
        
        print("\n🎉 Reproducción completa finalizada")

    def get_audio_info(self, file_path: str) -> dict:
        """Obtiene información del archivo de audio"""
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
            
            # Intentar obtener duración si pygame está disponible
            if self.pygame_initialized:
                try:
                    pygame.mixer.music.load(file_path)
                    # pygame no tiene método directo para duración, pero podemos estimar
                    info["duration"] = "Desconocida"
                except:
                    info["duration"] = "No disponible"
            
            return info
            
        except Exception as e:
            return {"error": str(e)}

    def cleanup(self) -> None:
        """Limpia recursos del reproductor"""
        if self.pygame_initialized:
            pygame.mixer.quit()
            self.pygame_initialized = False
