class PrimerObjetoPrueba:
    
    def __init__(self, nombre: str, edad: int):
        self.nombre: str = nombre
        self.edad: int = edad
        
    def __str__(self) -> str:
        return f"Nombre: {self.nombre}, Edad: {self.edad}"
    
    def saludar(self) -> str:
        return f"Hola, mi nombre es {self.nombre} y tengo {self.edad} años"

