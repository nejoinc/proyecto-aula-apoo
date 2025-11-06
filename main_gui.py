"""
Lanzador de la interfaz gráfica de StudyBox

Este módulo inicia la aplicación con interfaz gráfica (GUI)
en lugar de la interfaz de consola.

Uso:
    python main_gui.py
"""

import tkinter as tk
from src.gui_app import StudyBoxGUI


def main():
    """Función principal que inicia la aplicación GUI"""
    print("🚀 Iniciando StudyBox GUI...")
    print("📚 Cargando interfaz gráfica...\n")
    
    # Crear la ventana principal
    root = tk.Tk()
    
    # Inicializar la aplicación
    app = StudyBoxGUI(root)
    
    # Iniciar el loop principal
    root.mainloop()
    
    print("\n👋 StudyBox cerrado. ¡Hasta luego!")


if __name__ == "__main__":
    main()


