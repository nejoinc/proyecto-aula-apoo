from src.app import StudyBoxApp
from src.file_manager import FileManager
from typing import List

def menu() -> None:
    print("\n=== 📚 StudyBox - Menú Principal ===")
    print("1. Subir archivo")
    print("2. Procesar archivos")
    print("3. 🤖 Chatbot de Estudio")
    print("4. 🎵 Generador de Audio")
    print("5. 🎧 Reproductor de Audio")
    print("6. 🃏 Generador de Flashcards")
    print("7. 🎯 Generador de Quiz")
    print("8. Listar archivos")
    print("9. Mostrar conceptos clave")
    print("10. Ver archivos soportados")
    print("11. Recargar archivos desde storage")
    print("0. Salir")

if __name__ == "__main__":
    app: StudyBoxApp = StudyBoxApp()

    while True:
        menu()
        opcion: str = input("Seleccione una opción: ")

        if opcion == "1":
            archivo: str = input("Ingrese la ruta del archivo: ")
            app.upload_file(archivo)

        elif opcion == "2":
            app.process_files()

        elif opcion == "3":
            app.start_chatbot()

        elif opcion == "4":
            app.start_audio_generator()

        elif opcion == "5":
            app.start_audio_player()

        elif opcion == "6":
            app.start_flashcard_generator()

        elif opcion == "7":
            app.start_quiz_generator()

        elif opcion == "8":
            archivos: List[str] = FileManager.list_files()
            if archivos:
                print("📂 Archivos en almacenamiento local:")
                for f in archivos:
                    print(" -", f)
            else:
                print("⚠️ No hay archivos guardados todavía.")

        elif opcion == "9":
            app.show_key_concepts()

        elif opcion == "10":
            extensions: List[str] = FileManager.get_supported_extensions()
            print("📋 Tipos de archivo soportados:")
            for ext in extensions:
                print(f"   • {ext}")

        elif opcion == "11":
            app.reload_files_from_storage()

        elif opcion == "0":
            print("👋 Saliendo de StudyBox...")
            break

        else:
            print("❌ Opción no válida, intente de nuevo.")
