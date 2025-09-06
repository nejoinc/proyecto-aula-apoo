from model import PrimerObjetoPrueba

class UIConsole:

    def __init__(self):
        self.clase = PrimerObjetoPrueba("Juan", 20)
    
    def mostrar_menu(self):
        """Muestra el menú principal"""
        while True:
            print("\n" + "="*40)
            print("        MENÚ DE PRUEBA")
            print("="*40)
            print("1. Mostrar información del objeto")
            print("2. Saludar")
            print("3. Cambiar nombre")
            print("4. Cambiar edad")
            print("5. Salir")
            print("="*40)
            
            opcion = input("Selecciona una opción (1-5): ").strip()
            
            if opcion == "1":
                self.mostrar_info()
            elif opcion == "2":
                self.saludar()
            elif opcion == "3":
                self.cambiar_nombre()
            elif opcion == "4":
                self.cambiar_edad()
            elif opcion == "5":
                print("¡Hasta luego!")
                break
            else:
                print("❌ Opción no válida. Intenta de nuevo.")
    
    def mostrar_info(self):
        """Muestra la información del objeto"""
        print(f"\n📋 Información del objeto:")
        print(f"   {self.clase}")
    
    def saludar(self):
        """Muestra el saludo del objeto"""
        print(f"\n👋 {self.clase.saludar()}")
    
    def cambiar_nombre(self):
        """Permite cambiar el nombre del objeto"""
        nuevo_nombre = input("Ingresa el nuevo nombre: ").strip()
        if nuevo_nombre:
            self.clase.nombre = nuevo_nombre
            print(f"✅ Nombre cambiado a: {nuevo_nombre}")
        else:
            print("❌ El nombre no puede estar vacío")
    
    def cambiar_edad(self):
        """Permite cambiar la edad del objeto"""
        try:
            nueva_edad = int(input("Ingresa la nueva edad: ").strip())
            if nueva_edad >= 0:
                self.clase.edad = nueva_edad
                print(f"✅ Edad cambiada a: {nueva_edad}")
            else:
                print("❌ La edad debe ser un número positivo")
        except ValueError:
            print("❌ Por favor ingresa un número válido")

