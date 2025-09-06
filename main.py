from src.app import StudyBoxApp
from src.file_manager import FileManager

def menu():
    print("\n=== 📚 StudyBox - Menú Principal ===")
    print("1. Subir archivo")
    print("2. Procesar archivos")
    print("3. Agregar herramienta")
    print("4. Ejecutar herramientas")
    print("5. Listar archivos")   
    print("0. Salir")

if __name__ == "__main__":
    app = StudyBoxApp()

    while True:
        menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            archivo = input("Ingrese la ruta del archivo: ")
            app.upload_file(archivo)

        elif opcion == "2":
            app.process_files()

        elif opcion == "3":
            herramienta = input("Ingrese el nombre de la herramienta: ")
            app.add_tool(herramienta)

        elif opcion == "4":
            app.run_tools()

        elif opcion == "5":
            archivos = FileManager.list_files()
            if archivos:
                print("📂 Archivos en almacenamiento local:")
                for f in archivos:
                    print(" -", f)
            else:
                print("⚠️ No hay archivos guardados todavía.")

        elif opcion == "0":
            print("👋 Saliendo de StudyBox...")
            break

        else:
            print("❌ Opción no válida, intente de nuevo.")
