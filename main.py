from src.app import StudyBoxApp
from src.file_manager import FileManager

def menu():
    print("\n=== StudyBox - Menu Principal ===")
    print("1. Subir archivo")
    print("2. Procesar archivos")
    print("3. Eliminar archivos")
    print("4. Chatbot de Estudio")
    print("5. Generador de Audio")
    print("6. Reproductor de Audio")
    print("7. Generador de Flashcards")
    print("8. Generador de Quiz")
    print("9. Listar archivos")
    print("10. Mostrar conceptos clave")
    print("11. Ver archivos soportados")
    print("12. Recargar archivos desde storage")
    print("0. Salir")

if __name__ == "__main__":
    app = StudyBoxApp()

    while True:
        menu()
        opcion = input("Seleccione una opcion (0-12): ")

        if opcion == "1":
            archivo = input("Ingrese la ruta del archivo (por ejemplo C:/ruta/archivo.txt): ")
            app.upload_file(archivo)

        elif opcion == "2":
            app.process_files()

        elif opcion == "3":
            archivos = FileManager.list_files()
            if archivos:
                print("Archivos en almacenamiento local:")
                for f in archivos:
                    print(" -", f)
            else:
                print("No hay archivos guardados todavia.")
                continue

            Delete_File = input("Ingrese el archivo que quiere eliminar: ")

            if Delete_File in archivos:
                try:
                    if FileManager.delete_file(Delete_File):
                        print(f"El archivo '{Delete_File}' fue eliminado exitosamente.")
                    else:
                        print(f"Error: No se pudo eliminar el archivo '{Delete_File}'.")
                except:
                    print(f"Error al eliminar el archivo '{Delete_File}'")
            else:
                print(f"El archivo '{Delete_File}' no existe en la lista.")




        elif opcion == "4":
            app.start_chatbot()

        elif opcion == "5":
            app.start_audio_generator()

        elif opcion == "6":
            app.start_audio_player()

        elif opcion == "7":
            app.start_flashcard_generator()

        elif opcion == "8":
            app.start_quiz_generator()

        elif opcion == "9":
            archivos = FileManager.list_files()
            if archivos:
                print("Archivos en almacenamiento local:")
                for f in archivos:
                    print(" -", f)
            else:
                print("No hay archivos guardados todavia.")

        elif opcion == "10":
            app.show_key_concepts()

        elif opcion == "11":
            extensions = FileManager.get_supported_extensions()
            print("Tipos de archivo soportados:")
            for ext in extensions:
                print(f"   {ext}")

        elif opcion == "12":
            app.reload_files_from_storage()

        elif opcion == "0":
            print("Saliendo de StudyBox...")
            break

        else:
            print("Opcion no valida, intente de nuevo.")
