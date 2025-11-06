"""
Interfaz gráfica (GUI) de StudyBox usando Tkinter

Este módulo proporciona una interfaz gráfica moderna y amigable
para todas las funcionalidades de StudyBox.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import time
from typing import List, Optional
import threading

from .app import StudyBoxApp
from .file_manager import FileManager
from .tools.chatbot_tool import ChatbotTool
from .tools.audio_generator_tool import AudioGeneratorTool
from .tools.audio_player_tool import AudioPlayerTool
from .tools.flashcard_tool import FlashcardTool
from .tools.quiz_tool import QuizTool


class StudyBoxGUI:
    """Interfaz gráfica principal de StudyBox"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("📚 StudyBox - Aplicación de Estudio")
        self.root.geometry("1200x700")
        self.root.minsize(900, 600)
        
        # Configurar el tema de colores
        self.colors = {
            'primary': '#2C3E50',      # Azul oscuro
            'secondary': '#3498DB',    # Azul claro
            'accent': '#E74C3C',       # Rojo
            'success': '#27AE60',      # Verde
            'warning': '#F39C12',      # Naranja
            'bg': '#ECF0F1',           # Gris claro
            'text': '#2C3E50',         # Texto oscuro
            'white': '#FFFFFF'
        }
        
        # Inicializar la aplicación
        self.app = StudyBoxApp()
        
        # Configurar el estilo
        self.setup_style()
        
        # Crear la interfaz
        self.create_widgets()
        
    def setup_style(self):
        """Configura los estilos de la aplicación"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar estilos personalizados
        style.configure('Sidebar.TFrame', background=self.colors['primary'])
        style.configure('Content.TFrame', background=self.colors['bg'])
        style.configure('Title.TLabel', 
                       background=self.colors['primary'],
                       foreground=self.colors['white'],
                       font=('Segoe UI', 16, 'bold'),
                       padding=10)
        style.configure('SideButton.TButton',
                       background=self.colors['secondary'],
                       foreground=self.colors['white'],
                       font=('Segoe UI', 10),
                       padding=10)
        
    def create_widgets(self):
        """Crea todos los widgets de la interfaz"""
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Sidebar (panel lateral)
        self.create_sidebar(main_frame)
        
        # Content area (área de contenido)
        self.create_content_area(main_frame)
        
        # Barra de estado
        self.create_status_bar()
        
    def create_sidebar(self, parent):
        """Crea el panel lateral con los botones de navegación"""
        sidebar = tk.Frame(parent, bg=self.colors['primary'], width=250)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)
        
        # Título
        title_label = tk.Label(
            sidebar,
            text="📚 StudyBox",
            bg=self.colors['primary'],
            fg=self.colors['white'],
            font=('Segoe UI', 18, 'bold'),
            pady=20
        )
        title_label.pack()
        
        # Separador
        tk.Frame(sidebar, bg=self.colors['secondary'], height=2).pack(fill=tk.X, padx=10)
        
        # Sección: Gestión de Archivos
        self.create_section_label(sidebar, "📂 Gestión de Archivos")
        
        self.create_sidebar_button(sidebar, "📤 Subir Archivo", self.upload_file)
        self.create_sidebar_button(sidebar, "⚙️ Procesar Archivos", self.process_files)
        self.create_sidebar_button(sidebar, "📋 Listar Archivos", self.list_files)
        self.create_sidebar_button(sidebar, "🗑️ Eliminar Archivo", self.delete_file)
        
        # Separador
        tk.Frame(sidebar, bg=self.colors['secondary'], height=1).pack(fill=tk.X, padx=10, pady=10)
        
        # Sección: Herramientas de Estudio
        self.create_section_label(sidebar, "🎓 Herramientas de Estudio")
        
        self.create_sidebar_button(sidebar, "🤖 Chatbot", self.start_chatbot)
        self.create_sidebar_button(sidebar, "🃏 Flashcards", self.start_flashcards)
        self.create_sidebar_button(sidebar, "🎯 Quiz", self.start_quiz)
        self.create_sidebar_button(sidebar, "🎵 Generar Audio", self.start_audio_generator)
        self.create_sidebar_button(sidebar, "🎧 Reproducir Audio", self.start_audio_player)
        self.create_sidebar_button(sidebar, "💡 Conceptos Clave", self.show_key_concepts)
        
        # Separador
        tk.Frame(sidebar, bg=self.colors['secondary'], height=1).pack(fill=tk.X, padx=10, pady=10)
        
        # Botón de salir
        exit_btn = tk.Button(
            sidebar,
            text="🚪 Salir",
            bg=self.colors['accent'],
            fg=self.colors['white'],
            font=('Segoe UI', 10, 'bold'),
            relief=tk.FLAT,
            cursor='hand2',
            command=self.exit_app
        )
        exit_btn.pack(side=tk.BOTTOM, fill=tk.X, padx=15, pady=15)
        
    def create_section_label(self, parent, text):
        """Crea una etiqueta de sección"""
        label = tk.Label(
            parent,
            text=text,
            bg=self.colors['primary'],
            fg=self.colors['secondary'],
            font=('Segoe UI', 11, 'bold'),
            anchor='w',
            padx=15,
            pady=10
        )
        label.pack(fill=tk.X)
        
    def create_sidebar_button(self, parent, text, command):
        """Crea un botón en el sidebar"""
        btn = tk.Button(
            parent,
            text=text,
            bg=self.colors['primary'],
            fg=self.colors['white'],
            font=('Segoe UI', 10),
            relief=tk.FLAT,
            cursor='hand2',
            anchor='w',
            padx=15,
            pady=10,
            command=command
        )
        btn.pack(fill=tk.X, padx=5, pady=2)
        
        # Efecto hover
        def on_enter(e):
            btn['bg'] = self.colors['secondary']
            
        def on_leave(e):
            btn['bg'] = self.colors['primary']
            
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
    def create_content_area(self, parent):
        """Crea el área de contenido principal"""
        content_frame = tk.Frame(parent, bg=self.colors['bg'])
        content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Header
        header = tk.Frame(content_frame, bg=self.colors['white'], height=80)
        header.pack(fill=tk.X, padx=20, pady=20)
        header.pack_propagate(False)
        
        self.header_label = tk.Label(
            header,
            text="Bienvenido a StudyBox",
            bg=self.colors['white'],
            fg=self.colors['primary'],
            font=('Segoe UI', 20, 'bold'),
            anchor='w'
        )
        self.header_label.pack(side=tk.LEFT, padx=20, pady=20)
        
        # Content area con scroll
        content_canvas = tk.Canvas(content_frame, bg=self.colors['bg'], highlightthickness=0)
        content_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        scrollbar = ttk.Scrollbar(content_frame, orient=tk.VERTICAL, command=content_canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=(0, 20), padx=(0, 20))
        
        content_canvas.configure(yscrollcommand=scrollbar.set)
        
        self.content_inner = tk.Frame(content_canvas, bg=self.colors['bg'])
        content_canvas.create_window((0, 0), window=self.content_inner, anchor='nw')
        
        def configure_scroll(event):
            content_canvas.configure(scrollregion=content_canvas.bbox("all"))
            
        self.content_inner.bind("<Configure>", configure_scroll)
        
        # Mostrar pantalla de inicio
        self.show_welcome_screen()
        
    def create_status_bar(self):
        """Crea la barra de estado"""
        self.status_bar = tk.Label(
            self.root,
            text="Listo",
            bg=self.colors['primary'],
            fg=self.colors['white'],
            font=('Segoe UI', 9),
            anchor='w',
            padx=10
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def update_status(self, message: str):
        """Actualiza el mensaje de la barra de estado"""
        self.status_bar.config(text=message)
        self.root.update_idletasks()
        
    def clear_content(self):
        """Limpia el área de contenido"""
        for widget in self.content_inner.winfo_children():
            widget.destroy()
            
    def show_welcome_screen(self):
        """Muestra la pantalla de bienvenida"""
        self.clear_content()
        self.header_label.config(text="Bienvenido a StudyBox")
        
        welcome_frame = tk.Frame(self.content_inner, bg=self.colors['white'], relief=tk.FLAT)
        welcome_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Icono y mensaje de bienvenida
        tk.Label(
            welcome_frame,
            text="📚",
            bg=self.colors['white'],
            font=('Segoe UI', 80)
        ).pack(pady=30)
        
        tk.Label(
            welcome_frame,
            text="Bienvenido a StudyBox",
            bg=self.colors['white'],
            fg=self.colors['primary'],
            font=('Segoe UI', 24, 'bold')
        ).pack(pady=10)
        
        tk.Label(
            welcome_frame,
            text="Tu compañero inteligente de estudio",
            bg=self.colors['white'],
            fg=self.colors['text'],
            font=('Segoe UI', 12)
        ).pack(pady=5)
        
        # Descripción
        description = """
StudyBox te ayuda a estudiar de manera más efectiva.
        
Funcionalidades principales:
• Procesa tus archivos de estudio (TXT, PDF, DOCX, MD, etc.)
• Chatea con un asistente de IA sobre tu contenido
• Genera flashcards automáticas para repasar
• Crea quizzes personalizados
• Convierte texto a audio para estudiar mientras haces otras cosas
• Extrae conceptos clave de tus materiales

¡Comienza subiendo un archivo desde el menú lateral!
        """
        
        tk.Label(
            welcome_frame,
            text=description,
            bg=self.colors['white'],
            fg=self.colors['text'],
            font=('Segoe UI', 11),
            justify=tk.LEFT
        ).pack(pady=20, padx=40)
        
    # ===== FUNCIONES DE GESTIÓN DE ARCHIVOS =====
    
    def upload_file(self):
        """Abre un diálogo para subir archivos"""
        self.clear_content()
        self.header_label.config(text="📤 Subir Archivo")
        self.update_status("Seleccionando archivo...")
        
        # Obtener extensiones soportadas
        extensions = FileManager.get_supported_extensions()
        filetypes = [
            ("Todos los archivos soportados", " ".join([f"*{ext}" for ext in extensions])),
            ("Archivos de texto", "*.txt *.md"),
            ("Documentos", "*.pdf *.docx *.doc"),
            ("Código", "*.py *.js *.java *.cpp"),
            ("Audio", "*.mp3 *.wav"),
            ("Todos los archivos", "*.*")
        ]
        
        file_path = filedialog.askopenfilename(
            title="Selecciona un archivo",
            filetypes=filetypes
        )
        
        if file_path:
            try:
                self.app.upload_file(file_path)
                
                # Mostrar confirmación
                result_frame = tk.Frame(self.content_inner, bg=self.colors['white'])
                result_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
                
                tk.Label(
                    result_frame,
                    text="✅",
                    bg=self.colors['white'],
                    font=('Segoe UI', 60)
                ).pack(pady=30)
                
                tk.Label(
                    result_frame,
                    text="Archivo subido correctamente",
                    bg=self.colors['white'],
                    fg=self.colors['success'],
                    font=('Segoe UI', 16, 'bold')
                ).pack(pady=10)
                
                tk.Label(
                    result_frame,
                    text=f"Archivo: {os.path.basename(file_path)}",
                    bg=self.colors['white'],
                    fg=self.colors['text'],
                    font=('Segoe UI', 11)
                ).pack(pady=5)
                
                self.update_status(f"Archivo subido: {os.path.basename(file_path)}")
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo subir el archivo:\n{str(e)}")
                self.update_status("Error al subir archivo")
        else:
            self.update_status("Operación cancelada")
            self.show_welcome_screen()
            
    def process_files(self):
        """Muestra la interfaz para procesar archivos"""
        self.clear_content()
        self.header_label.config(text="⚙️ Procesar Archivos")
        self.update_status("Cargando archivos disponibles...")
        
        # Obtener archivos disponibles
        all_files = self.app._get_all_available_files()
        
        if not all_files:
            tk.Label(
                self.content_inner,
                text="⚠️ No hay archivos disponibles",
                bg=self.colors['bg'],
                fg=self.colors['warning'],
                font=('Segoe UI', 14, 'bold')
            ).pack(pady=50)
            
            tk.Label(
                self.content_inner,
                text="Sube archivos primero usando la opción 'Subir Archivo'",
                bg=self.colors['bg'],
                fg=self.colors['text'],
                font=('Segoe UI', 11)
            ).pack(pady=10)
            
            self.update_status("No hay archivos disponibles")
            return
            
        # Frame para la lista de archivos
        list_frame = tk.Frame(self.content_inner, bg=self.colors['white'])
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(
            list_frame,
            text="Selecciona los archivos a procesar:",
            bg=self.colors['white'],
            fg=self.colors['primary'],
            font=('Segoe UI', 12, 'bold')
        ).pack(pady=10, padx=10, anchor='w')
        
        # Lista con checkboxes
        file_vars = []
        canvas = tk.Canvas(list_frame, bg=self.colors['white'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['white'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        for file_path in all_files:
            var = tk.BooleanVar(value=False)
            file_vars.append((var, file_path))
            
            file_frame = tk.Frame(scrollable_frame, bg=self.colors['white'])
            file_frame.pack(fill=tk.X, padx=10, pady=5)
            
            cb = tk.Checkbutton(
                file_frame,
                variable=var,
                bg=self.colors['white'],
                font=('Segoe UI', 10)
            )
            cb.pack(side=tk.LEFT)
            
            filename = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            size_kb = file_size / 1024
            
            tk.Label(
                file_frame,
                text=f"{filename} ({size_kb:.1f} KB)",
                bg=self.colors['white'],
                fg=self.colors['text'],
                font=('Segoe UI', 10),
                anchor='w'
            ).pack(side=tk.LEFT, padx=10)
            
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
        
        # Botones
        button_frame = tk.Frame(list_frame, bg=self.colors['white'])
        button_frame.pack(fill=tk.X, pady=10, padx=10)
        
        def select_all():
            for var, _ in file_vars:
                var.set(True)
                
        def deselect_all():
            for var, _ in file_vars:
                var.set(False)
                
        def process_selected():
            selected_files = [file_path for var, file_path in file_vars if var.get()]
            
            if not selected_files:
                messagebox.showwarning("Advertencia", "No se seleccionaron archivos")
                return
                
            # Procesar en un hilo separado para no bloquear la UI
            self.update_status(f"Procesando {len(selected_files)} archivo(s)...")
            
            def process_thread():
                try:
                    self.app._process_selected_files(selected_files)
                    self.root.after(0, lambda: self.show_process_success(len(selected_files)))
                except Exception as e:
                    self.root.after(0, lambda: messagebox.showerror("Error", f"Error procesando archivos:\n{str(e)}"))
                    
            threading.Thread(target=process_thread, daemon=True).start()
            
        tk.Button(
            button_frame,
            text="✅ Seleccionar Todos",
            bg=self.colors['success'],
            fg=self.colors['white'],
            font=('Segoe UI', 10),
            relief=tk.FLAT,
            cursor='hand2',
            command=select_all
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="❌ Deseleccionar Todos",
            bg=self.colors['warning'],
            fg=self.colors['white'],
            font=('Segoe UI', 10),
            relief=tk.FLAT,
            cursor='hand2',
            command=deselect_all
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="⚙️ Procesar Seleccionados",
            bg=self.colors['secondary'],
            fg=self.colors['white'],
            font=('Segoe UI', 10, 'bold'),
            relief=tk.FLAT,
            cursor='hand2',
            command=process_selected
        ).pack(side=tk.RIGHT, padx=5)
        
        self.update_status(f"{len(all_files)} archivo(s) disponible(s)")
        
    def show_process_success(self, num_files):
        """Muestra mensaje de éxito después de procesar"""
        messagebox.showinfo("Éxito", f"Se procesaron {num_files} archivo(s) correctamente")
        self.update_status(f"Procesamiento completado: {num_files} archivo(s)")
        
    def list_files(self):
        """Muestra la lista de archivos"""
        self.clear_content()
        self.header_label.config(text="📋 Archivos Almacenados")
        self.update_status("Cargando lista de archivos...")
        
        files = FileManager.list_files()
        
        if not files:
            tk.Label(
                self.content_inner,
                text="⚠️ No hay archivos almacenados",
                bg=self.colors['bg'],
                fg=self.colors['warning'],
                font=('Segoe UI', 14, 'bold')
            ).pack(pady=50)
            
            self.update_status("No hay archivos almacenados")
            return
            
        # Frame para la lista
        list_frame = tk.Frame(self.content_inner, bg=self.colors['white'])
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(
            list_frame,
            text=f"Archivos en almacenamiento ({len(files)}):",
            bg=self.colors['white'],
            fg=self.colors['primary'],
            font=('Segoe UI', 12, 'bold')
        ).pack(pady=10, padx=10, anchor='w')
        
        # Crear tabla de archivos
        tree_frame = tk.Frame(list_frame, bg=self.colors['white'])
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview
        tree = ttk.Treeview(
            tree_frame,
            columns=('Nombre', 'Tamaño'),
            show='headings',
            yscrollcommand=scrollbar.set
        )
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=tree.yview)
        
        tree.heading('Nombre', text='Nombre del Archivo')
        tree.heading('Tamaño', text='Tamaño')
        
        tree.column('Nombre', width=400)
        tree.column('Tamaño', width=100)
        
        for filename in files:
            file_path = os.path.join(FileManager.STORAGE_DIR, filename)
            if os.path.exists(file_path):
                size = os.path.getsize(file_path)
                size_kb = size / 1024
                tree.insert('', tk.END, values=(filename, f'{size_kb:.1f} KB'))
            else:
                tree.insert('', tk.END, values=(filename, 'N/A'))
                
        self.update_status(f"{len(files)} archivo(s) almacenado(s)")
        
    def delete_file(self):
        """Interfaz para eliminar archivos"""
        self.clear_content()
        self.header_label.config(text="🗑️ Eliminar Archivo")
        self.update_status("Cargando archivos...")
        
        files = FileManager.list_files()
        
        if not files:
            tk.Label(
                self.content_inner,
                text="⚠️ No hay archivos para eliminar",
                bg=self.colors['bg'],
                fg=self.colors['warning'],
                font=('Segoe UI', 14, 'bold')
            ).pack(pady=50)
            
            self.update_status("No hay archivos")
            return
            
        # Frame para la lista
        list_frame = tk.Frame(self.content_inner, bg=self.colors['white'])
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(
            list_frame,
            text="Selecciona el archivo a eliminar:",
            bg=self.colors['white'],
            fg=self.colors['primary'],
            font=('Segoe UI', 12, 'bold')
        ).pack(pady=10, padx=10, anchor='w')
        
        # Listbox con archivos
        listbox_frame = tk.Frame(list_frame, bg=self.colors['white'])
        listbox_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        listbox = tk.Listbox(
            listbox_frame,
            font=('Segoe UI', 10),
            yscrollcommand=scrollbar.set
        )
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)
        
        for filename in files:
            listbox.insert(tk.END, filename)
            
        # Botón de eliminar
        def delete_selected():
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("Advertencia", "Selecciona un archivo para eliminar")
                return
                
            filename = listbox.get(selection[0])
            
            confirm = messagebox.askyesno(
                "Confirmar eliminación",
                f"¿Estás seguro de que quieres eliminar '{filename}'?"
            )
            
            if confirm:
                try:
                    if FileManager.delete_file(filename):
                        messagebox.showinfo("Éxito", f"Archivo '{filename}' eliminado correctamente")
                        self.delete_file()  # Recargar la lista
                    else:
                        messagebox.showerror("Error", f"No se pudo eliminar '{filename}'")
                except Exception as e:
                    messagebox.showerror("Error", f"Error al eliminar el archivo:\n{str(e)}")
                    
        tk.Button(
            list_frame,
            text="🗑️ Eliminar Seleccionado",
            bg=self.colors['accent'],
            fg=self.colors['white'],
            font=('Segoe UI', 10, 'bold'),
            relief=tk.FLAT,
            cursor='hand2',
            command=delete_selected
        ).pack(pady=10)
        
        self.update_status(f"{len(files)} archivo(s) disponible(s) para eliminar")
        
    # ===== HERRAMIENTAS DE ESTUDIO =====
    
    def start_chatbot(self):
        """Inicia el chatbot en una ventana de chat"""
        if not self.app.texts:
            messagebox.showwarning(
                "Advertencia",
                "No hay contenido procesado.\nProcesa algunos archivos primero."
            )
            return
            
        # Crear ventana de chat
        chat_window = tk.Toplevel(self.root)
        chat_window.title("🤖 Chatbot de Estudio")
        chat_window.geometry("800x600")
        chat_window.configure(bg=self.colors['bg'])
        
        # Header
        header = tk.Frame(chat_window, bg=self.colors['primary'], height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="🤖 Chatbot de Estudio",
            bg=self.colors['primary'],
            fg=self.colors['white'],
            font=('Segoe UI', 14, 'bold')
        ).pack(pady=15, padx=20, side=tk.LEFT)
        
        # Área de chat
        chat_frame = tk.Frame(chat_window, bg=self.colors['white'])
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            font=('Segoe UI', 10),
            bg=self.colors['bg'],
            fg=self.colors['text'],
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        chat_display.pack(fill=tk.BOTH, expand=True)
        chat_display.config(state=tk.DISABLED)
        
        # Frame de entrada
        input_frame = tk.Frame(chat_window, bg=self.colors['white'])
        input_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        input_entry = tk.Entry(
            input_frame,
            font=('Segoe UI', 11),
            relief=tk.FLAT,
            bg=self.colors['bg']
        )
        input_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, ipady=8, padx=(0, 10))
        
        # Preparar contexto
        context = self.app.chatbot._prepare_context(self.app.texts)
        conversation_history = []
        
        def add_message(sender, message):
            chat_display.config(state=tk.NORMAL)
            chat_display.insert(tk.END, f"\n{sender}:\n", 'sender')
            chat_display.insert(tk.END, f"{message}\n", 'message')
            chat_display.see(tk.END)
            chat_display.config(state=tk.DISABLED)
            
        # Configurar etiquetas de texto
        chat_display.tag_config('sender', foreground=self.colors['primary'], font=('Segoe UI', 10, 'bold'))
        chat_display.tag_config('message', foreground=self.colors['text'])
        
        # Mensaje de bienvenida
        add_message("🤖 Asistente", "¡Hola! Estoy listo para ayudarte con tu material de estudio.\n\nPuedes preguntarme sobre conceptos, pedir resúmenes, ejemplos, o hacer preguntas específicas.\n\nComandos especiales:\n- 'resumen' - Genera un resumen del contenido\n- 'conceptos' - Extrae conceptos clave\n- 'ejemplos' - Genera ejemplos prácticos")
        
        def send_message(event=None):
            user_input = input_entry.get().strip()
            if not user_input:
                return
                
            input_entry.delete(0, tk.END)
            add_message("👤 Tú", user_input)
            
            if user_input.lower() in ['salir', 'exit', 'quit']:
                chat_window.destroy()
                return
                
            # Procesar en hilo separado
            def process_question():
                nonlocal conversation_history
                try:
                    if user_input.lower() == 'resumen':
                        response = self.app.chatbot._generate_summary(context)
                    elif user_input.lower() == 'conceptos':
                        response = self.app.chatbot._extract_concepts(context)
                    elif user_input.lower() == 'ejemplos':
                        response = self.app.chatbot._generate_examples(context)
                    else:
                        response = self.app.chatbot._generate_response(user_input, context, conversation_history)
                        
                    conversation_history.append({
                        "user": user_input,
                        "assistant": response
                    })
                    
                    if len(conversation_history) > 10:
                        conversation_history = conversation_history[-10:]
                        
                    chat_window.after(0, lambda: add_message("🤖 Asistente", response))
                except Exception as e:
                    error_msg = f"Lo siento, ocurrió un error: {str(e)}"
                    chat_window.after(0, lambda: add_message("🤖 Asistente", error_msg))
                
            threading.Thread(target=process_question, daemon=True).start()
            
        send_btn = tk.Button(
            input_frame,
            text="Enviar",
            bg=self.colors['secondary'],
            fg=self.colors['white'],
            font=('Segoe UI', 10, 'bold'),
            relief=tk.FLAT,
            cursor='hand2',
            command=send_message
        )
        send_btn.pack(side=tk.RIGHT)
        
        input_entry.bind('<Return>', send_message)
        input_entry.focus()
        
        self.update_status("Chatbot iniciado")
        
    def start_flashcards(self):
        """Inicia el generador de flashcards"""
        if not self.app.texts:
            messagebox.showwarning(
                "Advertencia",
                "No hay contenido procesado.\nProcesa algunos archivos primero."
            )
            return
            
        self.clear_content()
        self.header_label.config(text="🃏 Generador de Flashcards")
        self.update_status("Generador de flashcards")
        
        # Frame principal
        main_frame = tk.Frame(self.content_inner, bg=self.colors['white'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(
            main_frame,
            text="Genera flashcards automáticas de tu contenido",
            bg=self.colors['white'],
            fg=self.colors['primary'],
            font=('Segoe UI', 14, 'bold')
        ).pack(pady=20)
        
        tk.Label(
            main_frame,
            text="Selecciona el tipo de flashcards que deseas generar:",
            bg=self.colors['white'],
            fg=self.colors['text'],
            font=('Segoe UI', 11)
        ).pack(pady=10)
        
        # Botones para diferentes tipos
        buttons_frame = tk.Frame(main_frame, bg=self.colors['white'])
        buttons_frame.pack(pady=20)
        
        def generate_automatic():
            self.update_status("Generando flashcards automáticas...")
            threading.Thread(target=lambda: self._generate_flashcards_thread("automáticas"), daemon=True).start()
            
        def generate_concepts():
            self.update_status("Generando flashcards de conceptos...")
            threading.Thread(target=lambda: self._generate_flashcards_thread("conceptos"), daemon=True).start()
            
        def generate_definitions():
            self.update_status("Generando flashcards de definiciones...")
            threading.Thread(target=lambda: self._generate_flashcards_thread("definiciones"), daemon=True).start()
            
        tk.Button(
            buttons_frame,
            text="🔄 Flashcards Automáticas",
            bg=self.colors['secondary'],
            fg=self.colors['white'],
            font=('Segoe UI', 11, 'bold'),
            relief=tk.FLAT,
            cursor='hand2',
            width=25,
            command=generate_automatic
        ).pack(pady=5)
        
        tk.Button(
            buttons_frame,
            text="💡 Flashcards de Conceptos",
            bg=self.colors['success'],
            fg=self.colors['white'],
            font=('Segoe UI', 11, 'bold'),
            relief=tk.FLAT,
            cursor='hand2',
            width=25,
            command=generate_concepts
        ).pack(pady=5)
        
        tk.Button(
            buttons_frame,
            text="📖 Flashcards de Definiciones",
            bg=self.colors['warning'],
            fg=self.colors['white'],
            font=('Segoe UI', 11, 'bold'),
            relief=tk.FLAT,
            cursor='hand2',
            width=25,
            command=generate_definitions
        ).pack(pady=5)
        
    def _generate_flashcards_thread(self, flashcard_type):
        """Genera flashcards en un hilo separado"""
        combined_text = "\n\n".join(self.app.texts)
        context = combined_text[:8000]
        
        if flashcard_type == "automáticas":
            if self.app.flashcard_generator.ai_available:
                flashcards = self.app.flashcard_generator._generate_ai_flashcards(context, "automáticas")
            else:
                flashcards = self.app.flashcard_generator._generate_simple_flashcards(context)
        elif flashcard_type == "conceptos":
            if self.app.flashcard_generator.ai_available:
                flashcards = self.app.flashcard_generator._generate_ai_flashcards(context, "conceptos clave y definiciones importantes")
            else:
                flashcards = self.app.flashcard_generator._generate_simple_flashcards(context, "conceptos")
        else:  # definiciones
            if self.app.flashcard_generator.ai_available:
                flashcards = self.app.flashcard_generator._generate_ai_flashcards(context, "definiciones y términos importantes")
            else:
                flashcards = self.app.flashcard_generator._generate_simple_flashcards(context, "definiciones")
                
        self.root.after(0, lambda: self._show_flashcards(flashcards))
        
    def _show_flashcards(self, flashcards):
        """Muestra las flashcards generadas"""
        self.clear_content()
        self.header_label.config(text="🃏 Flashcards Generadas")
        
        if not flashcards:
            tk.Label(
                self.content_inner,
                text="❌ No se pudieron generar flashcards",
                bg=self.colors['bg'],
                fg=self.colors['accent'],
                font=('Segoe UI', 14, 'bold')
            ).pack(pady=50)
            return
            
        # Frame para las flashcards
        cards_frame = tk.Frame(self.content_inner, bg=self.colors['bg'])
        cards_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(
            cards_frame,
            text=f"Se generaron {len(flashcards)} flashcards",
            bg=self.colors['bg'],
            fg=self.colors['primary'],
            font=('Segoe UI', 12, 'bold')
        ).pack(pady=10)
        
        # Mostrar cada flashcard
        for i, card in enumerate(flashcards, 1):
            card_frame = tk.Frame(cards_frame, bg=self.colors['white'], relief=tk.RAISED, borderwidth=1)
            card_frame.pack(fill=tk.X, pady=5)
            
            tk.Label(
                card_frame,
                text=f"Flashcard {i}",
                bg=self.colors['white'],
                fg=self.colors['secondary'],
                font=('Segoe UI', 10, 'bold')
            ).pack(anchor='w', padx=10, pady=(10, 5))
            
            tk.Label(
                card_frame,
                text=f"❓ {card['Q']}",
                bg=self.colors['white'],
                fg=self.colors['text'],
                font=('Segoe UI', 10),
                wraplength=800,
                justify=tk.LEFT
            ).pack(anchor='w', padx=20, pady=5)
            
            tk.Label(
                card_frame,
                text=f"✅ {card['A']}",
                bg=self.colors['white'],
                fg=self.colors['text'],
                font=('Segoe UI', 10),
                wraplength=800,
                justify=tk.LEFT
            ).pack(anchor='w', padx=20, pady=(5, 10))
            
        self.update_status(f"{len(flashcards)} flashcards generadas")
        messagebox.showinfo("Éxito", f"Se generaron {len(flashcards)} flashcards correctamente")
        
    def start_quiz(self):
        """Inicia el generador de quizzes integrado en la GUI"""
        if not self.app.texts:
            messagebox.showwarning(
                "Advertencia",
                "No hay contenido procesado.\nProcesa algunos archivos primero."
            )
            return
            
        # Crear ventana de selección de quiz
        quiz_window = tk.Toplevel(self.root)
        quiz_window.title("🎯 Generador de Quiz")
        quiz_window.geometry("700x550")
        quiz_window.configure(bg=self.colors['bg'])
        
        # Header
        header = tk.Frame(quiz_window, bg=self.colors['primary'], height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="🎯 Generador de Quiz Interactivo",
            bg=self.colors['primary'],
            fg=self.colors['white'],
            font=('Segoe UI', 14, 'bold')
        ).pack(pady=15, padx=20, side=tk.LEFT)
        
        # Frame principal
        main_frame = tk.Frame(quiz_window, bg=self.colors['white'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        tk.Label(
            main_frame,
            text="Selecciona el tipo de quiz:",
            bg=self.colors['white'],
            fg=self.colors['primary'],
            font=('Segoe UI', 12, 'bold')
        ).pack(pady=20)
        
        # Tipos de quiz
        quiz_types = [
            ("📝 Opción Múltiple", "multiple_choice", "Preguntas con varias opciones de respuesta"),
            ("✓/✗ Verdadero/Falso", "true_false", "Afirmaciones para verificar si son correctas"),
            ("📋 Completar Espacios", "fill_blank", "Completa las palabras faltantes"),
            ("💭 Preguntas Abiertas", "open_questions", "Preguntas que requieren respuestas elaboradas"),
            ("🎲 Quiz Mixto", "mixed", "Combinación de diferentes tipos de preguntas"),
        ]
        
        # Frame para botones
        buttons_frame = tk.Frame(main_frame, bg=self.colors['white'])
        buttons_frame.pack(fill=tk.BOTH, expand=True, padx=20)
        
        for label, quiz_type, desc in quiz_types:
            btn_frame = tk.Frame(buttons_frame, bg=self.colors['white'])
            btn_frame.pack(fill=tk.X, pady=5)
            
            btn = tk.Button(
                btn_frame,
                text=label,
                bg=self.colors['secondary'],
                fg=self.colors['white'],
                font=('Segoe UI', 11, 'bold'),
                relief=tk.FLAT,
                cursor='hand2',
                width=25,
                anchor='w',
                command=lambda t=quiz_type: self._start_quiz_type(t, quiz_window)
            )
            btn.pack(side=tk.LEFT, padx=5)
            
            tk.Label(
                btn_frame,
                text=desc,
                bg=self.colors['white'],
                fg=self.colors['text'],
                font=('Segoe UI', 9)
            ).pack(side=tk.LEFT, padx=10)
        
        self.update_status("Selector de quiz abierto")
    
    def _start_quiz_type(self, quiz_type: str, parent_window):
        """Inicia un tipo específico de quiz"""
        parent_window.destroy()
        
        # Ventana para seleccionar número de preguntas
        num_window = tk.Toplevel(self.root)
        num_window.title("Configuración del Quiz")
        num_window.geometry("400x250")
        num_window.configure(bg=self.colors['bg'])
        num_window.transient(self.root)
        num_window.grab_set()
        
        content = tk.Frame(num_window, bg=self.colors['white'])
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(
            content,
            text="¿Cuántas preguntas deseas?",
            bg=self.colors['white'],
            fg=self.colors['primary'],
            font=('Segoe UI', 12, 'bold')
        ).pack(pady=20)
        
        # Slider para número de preguntas
        num_var = tk.IntVar(value=5)
        
        num_label = tk.Label(
            content,
            text=f"Número de preguntas: {num_var.get()}",
            bg=self.colors['white'],
            fg=self.colors['text'],
            font=('Segoe UI', 11)
        )
        num_label.pack(pady=10)
        
        def update_label(val):
            num_label.config(text=f"Número de preguntas: {int(float(val))}")
        
        scale = tk.Scale(
            content,
            from_=3,
            to=15,
            orient=tk.HORIZONTAL,
            variable=num_var,
            command=update_label,
            bg=self.colors['white'],
            fg=self.colors['text'],
            highlightthickness=0,
            length=300
        )
        scale.pack(pady=10)
        
        def start_generation():
            num_questions = num_var.get()
            num_window.destroy()
            self._generate_and_show_quiz(quiz_type, num_questions)
        
        # Frame para botones
        btn_frame = tk.Frame(content, bg=self.colors['white'])
        btn_frame.pack(pady=30)
        
        tk.Button(
            btn_frame,
            text="✓ Generar Quiz",
            bg=self.colors['success'],
            fg=self.colors['white'],
            font=('Segoe UI', 12, 'bold'),
            relief=tk.RAISED,
            cursor='hand2',
            width=20,
            height=2,
            command=start_generation
        ).pack(pady=10)
        
        tk.Button(
            btn_frame,
            text="Cancelar",
            bg=self.colors['accent'],
            fg=self.colors['white'],
            font=('Segoe UI', 10),
            relief=tk.FLAT,
            cursor='hand2',
            command=num_window.destroy
        ).pack(pady=5)
    
    def _generate_and_show_quiz(self, quiz_type: str, num_questions: int):
        """Genera el quiz y muestra la interfaz interactiva"""
        # Ventana de carga
        loading_window = tk.Toplevel(self.root)
        loading_window.title("Generando Quiz")
        loading_window.geometry("400x200")
        loading_window.configure(bg=self.colors['bg'])
        loading_window.transient(self.root)
        loading_window.grab_set()
        
        content = tk.Frame(loading_window, bg=self.colors['white'])
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(
            content,
            text="⏳ Generando tu quiz...",
            bg=self.colors['white'],
            fg=self.colors['primary'],
            font=('Segoe UI', 12, 'bold')
        ).pack(pady=30)
        
        progress = ttk.Progressbar(content, mode='indeterminate', length=300)
        progress.pack(pady=20)
        progress.start(10)
        
        # Generar quiz en hilo separado
        def generate():
            try:
                combined_text = "\n\n".join(self.app.texts)
                context = combined_text[:8000]
                
                # Generar según el tipo
                quiz = None
                if quiz_type == "multiple_choice":
                    if self.app.quiz_generator.ai_available:
                        quiz = self.app.quiz_generator._generate_ai_multiple_choice(context, num_questions)
                    else:
                        quiz = self.app.quiz_generator._generate_simple_multiple_choice(context, num_questions)
                
                elif quiz_type == "true_false":
                    if self.app.quiz_generator.ai_available:
                        quiz = self.app.quiz_generator._generate_ai_true_false(context, num_questions)
                    else:
                        quiz = self.app.quiz_generator._generate_simple_true_false(context, num_questions)
                
                elif quiz_type == "fill_blank":
                    if self.app.quiz_generator.ai_available:
                        quiz = self.app.quiz_generator._generate_ai_fill_blank(context, num_questions)
                    else:
                        quiz = self.app.quiz_generator._generate_simple_fill_blank(context, num_questions)
                
                elif quiz_type == "open_questions":
                    if self.app.quiz_generator.ai_available:
                        quiz = self.app.quiz_generator._generate_ai_open_questions(context, num_questions)
                    else:
                        quiz = self.app.quiz_generator._generate_simple_open_questions(context, num_questions)
                
                elif quiz_type == "mixed":
                    if self.app.quiz_generator.ai_available:
                        quiz = self.app.quiz_generator._generate_ai_mixed_quiz(context, num_questions)
                    else:
                        quiz = self.app.quiz_generator._generate_simple_mixed_quiz(context, num_questions)
                
                loading_window.after(0, lambda: loading_window.destroy())
                
                if quiz and len(quiz) > 0:
                    self.root.after(100, lambda: self._show_interactive_quiz(quiz, quiz_type))
                else:
                    self.root.after(100, lambda: messagebox.showerror("Error", "No se pudo generar el quiz"))
                
            except Exception as e:
                loading_window.after(0, lambda: loading_window.destroy())
                self.root.after(100, lambda: messagebox.showerror("Error", f"Error generando quiz:\n{str(e)}"))
        
        threading.Thread(target=generate, daemon=True).start()
    
    def _show_interactive_quiz(self, quiz: list, quiz_type: str):
        """Muestra el quiz de forma interactiva"""
        quiz_window = tk.Toplevel(self.root)
        quiz_window.title("🎯 Quiz Interactivo")
        quiz_window.geometry("900x700")
        quiz_window.configure(bg=self.colors['bg'])
        
        # Header
        header = tk.Frame(quiz_window, bg=self.colors['primary'], height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        progress_label = tk.Label(
            header,
            text=f"Pregunta 1 de {len(quiz)}",
            bg=self.colors['primary'],
            fg=self.colors['white'],
            font=('Segoe UI', 14, 'bold')
        )
        progress_label.pack(pady=15, padx=20, side=tk.LEFT)
        
        score_label = tk.Label(
            header,
            text="Puntaje: 0/0",
            bg=self.colors['primary'],
            fg=self.colors['white'],
            font=('Segoe UI', 12)
        )
        score_label.pack(pady=15, padx=20, side=tk.RIGHT)
        
        # Frame principal
        main_frame = tk.Frame(quiz_window, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Estado del quiz
        state = {
            'current': 0,
            'score': 0,
            'answered': 0,
            'user_answers': []
        }
        
        # Canvas con scroll para la pregunta
        canvas = tk.Canvas(main_frame, bg=self.colors['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
        question_frame = tk.Frame(canvas, bg=self.colors['bg'])
        
        canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 20), pady=20)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(20, 0), pady=20)
        
        canvas.create_window((0, 0), window=question_frame, anchor='nw', width=800)
        
        def update_scroll(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        question_frame.bind("<Configure>", update_scroll)
        
        def show_question(index):
            # Limpiar frame
            for widget in question_frame.winfo_children():
                widget.destroy()
            
            if index >= len(quiz):
                show_results()
                return
            
            q = quiz[index]
            
            # Actualizar header
            progress_label.config(text=f"Pregunta {index + 1} de {len(quiz)}")
            score_label.config(text=f"Puntaje: {state['score']}/{state['answered']}")
            
            # Pregunta
            q_text = q.get('question', q.get('Q', 'Pregunta'))
            
            tk.Label(
                question_frame,
                text=f"Pregunta {index + 1}:",
                bg=self.colors['bg'],
                fg=self.colors['primary'],
                font=('Segoe UI', 12, 'bold')
            ).pack(anchor='w', pady=(20, 10))
            
            question_label = tk.Label(
                question_frame,
                text=q_text,
                bg=self.colors['white'],
                fg=self.colors['text'],
                font=('Segoe UI', 11),
                wraplength=700,
                justify=tk.LEFT,
                padx=20,
                pady=20
            )
            question_label.pack(fill=tk.X, pady=(0, 20))
            
            answer_var = tk.StringVar()
            
            # Mostrar opciones según el tipo
            if 'options' in q or 'choices' in q:
                # Opción múltiple
                options = q.get('options', q.get('choices', []))
                for i, option in enumerate(options):
                    rb = tk.Radiobutton(
                        question_frame,
                        text=option,
                        variable=answer_var,
                        value=option,
                        bg=self.colors['bg'],
                        fg=self.colors['text'],
                        font=('Segoe UI', 10),
                        selectcolor=self.colors['secondary'],
                        activebackground=self.colors['bg'],
                        wraplength=650
                    )
                    rb.pack(anchor='w', pady=5, padx=30)
            
            elif quiz_type == "true_false":
                # Verdadero/Falso
                for option in ["Verdadero", "Falso"]:
                    rb = tk.Radiobutton(
                        question_frame,
                        text=option,
                        variable=answer_var,
                        value=option,
                        bg=self.colors['bg'],
                        fg=self.colors['text'],
                        font=('Segoe UI', 10),
                        selectcolor=self.colors['secondary'],
                        activebackground=self.colors['bg']
                    )
                    rb.pack(anchor='w', pady=5, padx=30)
            
            else:
                # Respuesta abierta
                tk.Label(
                    question_frame,
                    text="Tu respuesta:",
                    bg=self.colors['bg'],
                    fg=self.colors['text'],
                    font=('Segoe UI', 10)
                ).pack(anchor='w', pady=(10, 5), padx=30)
                
                answer_entry = tk.Text(
                    question_frame,
                    height=5,
                    font=('Segoe UI', 10),
                    wrap=tk.WORD
                )
                answer_entry.pack(fill=tk.X, padx=30, pady=5)
            
            # Botones
            btn_frame = tk.Frame(question_frame, bg=self.colors['bg'])
            btn_frame.pack(pady=30)
            
            def check_answer():
                if quiz_type in ["fill_blank", "open_questions"] or (quiz_type == "mixed" and 'answer' in q):
                    user_answer = answer_entry.get("1.0", tk.END).strip()
                else:
                    user_answer = answer_var.get()
                
                if not user_answer:
                    messagebox.showwarning("Advertencia", "Por favor selecciona o escribe una respuesta")
                    return
                
                correct_answer = q.get('answer', q.get('correct', q.get('A', '')))
                
                # Verificar respuesta
                is_correct = False
                if isinstance(correct_answer, str):
                    is_correct = user_answer.lower().strip() == correct_answer.lower().strip()
                
                state['answered'] += 1
                if is_correct:
                    state['score'] += 1
                    messagebox.showinfo("✓ Correcto!", f"¡Excelente!\n\nRespuesta correcta: {correct_answer}")
                else:
                    messagebox.showinfo("✗ Incorrecto", f"La respuesta correcta es:\n\n{correct_answer}")
                
                state['user_answers'].append({
                    'question': q_text,
                    'user_answer': user_answer,
                    'correct_answer': correct_answer,
                    'is_correct': is_correct
                })
                
                state['current'] += 1
                show_question(state['current'])
            
            tk.Button(
                btn_frame,
                text="Verificar Respuesta",
                bg=self.colors['success'],
                fg=self.colors['white'],
                font=('Segoe UI', 11, 'bold'),
                relief=tk.FLAT,
                cursor='hand2',
                command=check_answer
            ).pack(side=tk.LEFT, padx=10)
            
            if index < len(quiz) - 1:
                tk.Button(
                    btn_frame,
                    text="Saltar →",
                    bg=self.colors['warning'],
                    fg=self.colors['white'],
                    font=('Segoe UI', 11),
                    relief=tk.FLAT,
                    cursor='hand2',
                    command=lambda: (state.update({'current': state['current'] + 1}), show_question(state['current']))
                ).pack(side=tk.LEFT, padx=10)
        
        def show_results():
            for widget in question_frame.winfo_children():
                widget.destroy()
            
            progress_label.config(text="Quiz Completado")
            
            percentage = (state['score'] / state['answered'] * 100) if state['answered'] > 0 else 0
            
            tk.Label(
                question_frame,
                text="🎉 ¡Quiz Completado!",
                bg=self.colors['bg'],
                fg=self.colors['success'],
                font=('Segoe UI', 18, 'bold')
            ).pack(pady=30)
            
            result_frame = tk.Frame(question_frame, bg=self.colors['white'])
            result_frame.pack(fill=tk.X, padx=20, pady=20)
            
            tk.Label(
                result_frame,
                text=f"Puntaje Final: {state['score']}/{state['answered']}",
                bg=self.colors['white'],
                fg=self.colors['primary'],
                font=('Segoe UI', 16, 'bold')
            ).pack(pady=20)
            
            tk.Label(
                result_frame,
                text=f"Porcentaje: {percentage:.1f}%",
                bg=self.colors['white'],
                fg=self.colors['text'],
                font=('Segoe UI', 14)
            ).pack(pady=10)
            
            # Mensaje según el puntaje
            if percentage >= 90:
                msg = "¡Excelente trabajo! 🌟"
                color = self.colors['success']
            elif percentage >= 70:
                msg = "¡Buen trabajo! 👍"
                color = self.colors['secondary']
            elif percentage >= 50:
                msg = "Puedes mejorar 📚"
                color = self.colors['warning']
            else:
                msg = "Sigue practicando 💪"
                color = self.colors['accent']
            
            tk.Label(
                result_frame,
                text=msg,
                bg=self.colors['white'],
                fg=color,
                font=('Segoe UI', 12, 'bold')
            ).pack(pady=20)
            
            tk.Button(
                question_frame,
                text="Cerrar",
                bg=self.colors['primary'],
                fg=self.colors['white'],
                font=('Segoe UI', 11, 'bold'),
                relief=tk.FLAT,
                cursor='hand2',
                command=quiz_window.destroy
            ).pack(pady=20)
        
        # Mostrar primera pregunta
        show_question(0)
        self.update_status("Quiz interactivo iniciado")
        
    def start_audio_generator(self):
        """Inicia el generador de audio integrado en la GUI"""
        if not self.app.texts:
            messagebox.showwarning(
                "Advertencia",
                "No hay contenido procesado.\nProcesa algunos archivos primero."
            )
            return
            
        # Crear ventana de generador de audio
        audio_window = tk.Toplevel(self.root)
        audio_window.title("🎵 Generador de Audio")
        audio_window.geometry("800x600")
        audio_window.configure(bg=self.colors['bg'])
        
        # Header
        header = tk.Frame(audio_window, bg=self.colors['primary'], height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="🎵 Generador de Audio - Text to Speech",
            bg=self.colors['primary'],
            fg=self.colors['white'],
            font=('Segoe UI', 14, 'bold')
        ).pack(pady=15, padx=20, side=tk.LEFT)
        
        # Frame principal
        main_frame = tk.Frame(audio_window, bg=self.colors['white'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        tk.Label(
            main_frame,
            text="Selecciona el tipo de audio que deseas generar:",
            bg=self.colors['white'],
            fg=self.colors['primary'],
            font=('Segoe UI', 12, 'bold')
        ).pack(pady=20)
        
        # Tipos de audio disponibles
        audio_types = [
            ("1. 📖 Resumen narrado", "resumen", "Resume los conceptos principales de manera conversacional"),
            ("2. 💡 Explicación de conceptos", "conceptos", "Explica los conceptos clave detalladamente"),
            ("3. 📚 Lectura completa", "lectura", "Lee todo el contenido procesado"),
            ("4. ❓ Preguntas y respuestas", "qa", "Genera preguntas y respuestas sobre el tema"),
            ("5. 📖 Historia o conversación", "historia", "Convierte el contenido en una narrativa"),
            ("6. 🎯 Guía de estudio", "guia", "Crea una guía de estudio paso a paso"),
        ]
        
        # Frame para los botones
        buttons_frame = tk.Frame(main_frame, bg=self.colors['white'])
        buttons_frame.pack(fill=tk.BOTH, expand=True, padx=20)
        
        # Crear botones para cada tipo
        for label, tipo, desc in audio_types:
            btn_frame = tk.Frame(buttons_frame, bg=self.colors['white'])
            btn_frame.pack(fill=tk.X, pady=5)
            
            btn = tk.Button(
                btn_frame,
                text=label,
                bg=self.colors['secondary'],
                fg=self.colors['white'],
                font=('Segoe UI', 11, 'bold'),
                relief=tk.FLAT,
                cursor='hand2',
                width=30,
                anchor='w',
                command=lambda t=tipo: self._generate_audio_type(t, audio_window)
            )
            btn.pack(side=tk.LEFT, padx=5)
            
            tk.Label(
                btn_frame,
                text=desc,
                bg=self.colors['white'],
                fg=self.colors['text'],
                font=('Segoe UI', 9)
            ).pack(side=tk.LEFT, padx=10)
        
        # Botón para generar todos
        tk.Button(
            main_frame,
            text="🎵 Generar TODOS los tipos",
            bg=self.colors['success'],
            fg=self.colors['white'],
            font=('Segoe UI', 12, 'bold'),
            relief=tk.FLAT,
            cursor='hand2',
            command=lambda: self._generate_audio_type("todos", audio_window)
        ).pack(pady=20)
        
        self.update_status("Generador de audio abierto")
    
    def _generate_audio_type(self, audio_type: str, parent_window):
        """Genera un tipo específico de audio"""
        # Crear ventana de progreso
        progress_window = tk.Toplevel(parent_window)
        progress_window.title("Generando Audio")
        progress_window.geometry("600x400")
        progress_window.configure(bg=self.colors['bg'])
        progress_window.transient(parent_window)
        progress_window.grab_set()
        
        # Frame de contenido
        content_frame = tk.Frame(progress_window, bg=self.colors['white'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        tk.Label(
            content_frame,
            text="⏳ Generando audio...",
            bg=self.colors['white'],
            fg=self.colors['primary'],
            font=('Segoe UI', 14, 'bold')
        ).pack(pady=20)
        
        # Barra de progreso
        progress_bar = ttk.Progressbar(
            content_frame,
            mode='indeterminate',
            length=400
        )
        progress_bar.pack(pady=20)
        progress_bar.start(10)
        
        # Área de log
        log_text = scrolledtext.ScrolledText(
            content_frame,
            wrap=tk.WORD,
            font=('Consolas', 9),
            bg=self.colors['bg'],
            fg=self.colors['text'],
            relief=tk.FLAT,
            height=15
        )
        log_text.pack(fill=tk.BOTH, expand=True, pady=10)
        
        def add_log(message):
            log_text.insert(tk.END, f"{message}\n")
            log_text.see(tk.END)
            progress_window.update()
        
        # Generar audio en hilo separado
        def generate_thread():
            import sys
            from io import StringIO
            
            # Capturar prints
            old_stdout = sys.stdout
            sys.stdout = StringIO()
            
            try:
                context = self.app.audio_generator._prepare_context(self.app.texts)
                
                types_map = {
                    "resumen": ("Resumen Narrado", self.app.audio_generator._generate_summary_audio),
                    "conceptos": ("Explicación de Conceptos", self.app.audio_generator._generate_concepts_audio),
                    "lectura": ("Lectura Completa", self.app.audio_generator._generate_full_reading_audio),
                    "qa": ("Preguntas y Respuestas", self.app.audio_generator._generate_qa_audio),
                    "historia": ("Historia o Conversación", self.app.audio_generator._generate_story_audio),
                    "guia": ("Guía de Estudio", self.app.audio_generator._generate_study_guide_audio),
                }
                
                if audio_type == "todos":
                    progress_window.after(0, lambda: add_log("Generando TODOS los tipos de audio..."))
                    for name, (label, func) in types_map.items():
                        progress_window.after(0, lambda l=label: add_log(f"\n=== Generando: {l} ==="))
                        func(context)
                        progress_window.after(0, lambda l=label: add_log(f"✓ {l} completado"))
                else:
                    label, func = types_map.get(audio_type, ("Audio", None))
                    if func:
                        progress_window.after(0, lambda: add_log(f"Generando: {label}..."))
                        func(context)
                        progress_window.after(0, lambda: add_log(f"\n✓ {label} generado exitosamente!"))
                
                # Restaurar stdout
                sys.stdout = old_stdout
                
                progress_window.after(0, lambda: progress_bar.stop())
                progress_window.after(0, lambda: add_log("\n" + "="*50))
                progress_window.after(0, lambda: add_log("✓ Generación completada!"))
                progress_window.after(0, lambda: add_log("Los archivos de audio se guardaron en:"))
                progress_window.after(0, lambda: add_log("src/storage/generated_audio/"))
                progress_window.after(0, lambda: add_log("\nPuedes reproducirlos con el Reproductor de Audio"))
                
                # Botón para cerrar
                progress_window.after(100, lambda: self._add_close_button(content_frame, progress_window, progress_bar))
                
            except Exception as e:
                # Restaurar stdout
                sys.stdout = old_stdout
                
                progress_window.after(0, lambda: progress_bar.stop())
                progress_window.after(0, lambda: add_log(f"\n❌ Error: {str(e)}"))
                import traceback
                error_detail = traceback.format_exc()
                progress_window.after(0, lambda: add_log(f"\nDetalles: {error_detail}"))
                progress_window.after(100, lambda: self._add_close_button(content_frame, progress_window, progress_bar))
        
        threading.Thread(target=generate_thread, daemon=True).start()
    
    def _add_close_button(self, parent, window, progress_bar):
        """Agrega botón de cerrar después de completar"""
        try:
            progress_bar.stop()
        except:
            pass
        
        tk.Button(
            parent,
            text="✓ Cerrar",
            bg=self.colors['success'],
            fg=self.colors['white'],
            font=('Segoe UI', 11, 'bold'),
            relief=tk.FLAT,
            cursor='hand2',
            command=window.destroy
        ).pack(pady=10)
        
    def start_audio_player(self):
        """Inicia el reproductor de audio integrado en la GUI"""
        import pygame
        
        # Verificar si hay archivos de audio
        audio_files = self.app.audio_player.list_audio_files()
        
        if not audio_files:
            messagebox.showwarning(
                "Sin archivos",
                "No hay archivos de audio disponibles.\n\nGenera algunos audios primero usando el Generador de Audio."
            )
            return
        
        # Crear ventana de reproductor
        player_window = tk.Toplevel(self.root)
        player_window.title("🎧 Reproductor de Audio")
        player_window.geometry("700x500")
        player_window.configure(bg=self.colors['bg'])
        
        # Header
        header = tk.Frame(player_window, bg=self.colors['primary'], height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="🎧 Reproductor de Audio",
            bg=self.colors['primary'],
            fg=self.colors['white'],
            font=('Segoe UI', 14, 'bold')
        ).pack(pady=15, padx=20, side=tk.LEFT)
        
        # Frame principal
        main_frame = tk.Frame(player_window, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Lista de archivos
        tk.Label(
            main_frame,
            text="Archivos de audio disponibles:",
            bg=self.colors['bg'],
            fg=self.colors['primary'],
            font=('Segoe UI', 11, 'bold')
        ).pack(pady=(0, 10))
        
        list_frame = tk.Frame(main_frame, bg=self.colors['white'])
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        audio_listbox = tk.Listbox(
            list_frame,
            font=('Segoe UI', 10),
            yscrollcommand=scrollbar.set,
            selectmode=tk.SINGLE,
            bg=self.colors['white'],
            fg=self.colors['text'],
            selectbackground=self.colors['secondary'],
            selectforeground=self.colors['white']
        )
        audio_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=audio_listbox.yview)
        
        # Agregar archivos a la lista
        for file_path in audio_files:
            filename = os.path.basename(file_path)
            audio_listbox.insert(tk.END, filename)
        
        # Estado del reproductor
        current_playing = {"file": None, "index": None}
        is_paused = {"value": False}
        
        # Label de estado
        status_label = tk.Label(
            main_frame,
            text="Selecciona un archivo para reproducir",
            bg=self.colors['bg'],
            fg=self.colors['text'],
            font=('Segoe UI', 10)
        )
        status_label.pack(pady=10)
        
        # Barra de progreso
        progress_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        progress_frame.pack(fill=tk.X, pady=5)
        
        time_label = tk.Label(
            progress_frame,
            text="0:00",
            bg=self.colors['bg'],
            fg=self.colors['text'],
            font=('Segoe UI', 9)
        )
        time_label.pack(side=tk.LEFT, padx=5)
        
        progress_bar = ttk.Progressbar(
            progress_frame,
            mode='indeterminate',
            length=400
        )
        progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Frame de controles
        controls_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        controls_frame.pack(pady=15)
        
        def update_progress():
            """Actualiza el progreso de reproducción"""
            if current_playing["file"] and pygame.mixer.music.get_busy():
                elapsed = int(time.time() - current_playing.get("start_time", 0))
                time_label.config(text=f"{elapsed//60}:{elapsed%60:02d}")
                player_window.after(1000, update_progress)
            elif current_playing["file"] and not pygame.mixer.music.get_busy() and not is_paused["value"]:
                status_label.config(text="Reproducción completada")
                progress_bar.stop()
                play_btn.config(text="▶ Reproducir")
        
        def play_audio():
            """Reproduce el audio seleccionado"""
            selection = audio_listbox.curselection()
            if not selection:
                messagebox.showwarning("Advertencia", "Selecciona un archivo primero")
                return
            
            index = selection[0]
            file_path = audio_files[index]
            filename = os.path.basename(file_path)
            
            try:
                # Detener reproducción actual
                if current_playing["file"]:
                    pygame.mixer.music.stop()
                
                # Cargar y reproducir
                pygame.mixer.music.load(file_path)
                pygame.mixer.music.play()
                
                current_playing["file"] = file_path
                current_playing["index"] = index
                current_playing["start_time"] = time.time()
                is_paused["value"] = False
                
                status_label.config(text=f"Reproduciendo: {filename}")
                progress_bar.start(10)
                play_btn.config(text="⏸ Pausar")
                
                update_progress()
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo reproducir el audio:\n{str(e)}")
        
        def pause_audio():
            """Pausa o reanuda la reproducción"""
            if not current_playing["file"]:
                play_audio()
                return
            
            if not is_paused["value"]:
                pygame.mixer.music.pause()
                is_paused["value"] = True
                status_label.config(text="Pausado")
                progress_bar.stop()
                play_btn.config(text="▶ Reanudar")
            else:
                pygame.mixer.music.unpause()
                is_paused["value"] = False
                filename = os.path.basename(current_playing["file"])
                status_label.config(text=f"Reproduciendo: {filename}")
                progress_bar.start(10)
                play_btn.config(text="⏸ Pausar")
                update_progress()
        
        def stop_audio():
            """Detiene la reproducción"""
            if current_playing["file"]:
                pygame.mixer.music.stop()
                current_playing["file"] = None
                current_playing["index"] = None
                is_paused["value"] = False
                status_label.config(text="Detenido")
                progress_bar.stop()
                time_label.config(text="0:00")
                play_btn.config(text="▶ Reproducir")
        
        def on_double_click(event):
            """Reproduce al hacer doble clic"""
            play_audio()
        
        audio_listbox.bind('<Double-Button-1>', on_double_click)
        
        # Botones de control
        play_btn = tk.Button(
            controls_frame,
            text="▶ Reproducir",
            bg=self.colors['success'],
            fg=self.colors['white'],
            font=('Segoe UI', 11, 'bold'),
            relief=tk.FLAT,
            cursor='hand2',
            width=12,
            command=pause_audio
        )
        play_btn.pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            controls_frame,
            text="⏹ Detener",
            bg=self.colors['accent'],
            fg=self.colors['white'],
            font=('Segoe UI', 11, 'bold'),
            relief=tk.FLAT,
            cursor='hand2',
            width=12,
            command=stop_audio
        ).pack(side=tk.LEFT, padx=5)
        
        # Limpiar al cerrar
        def on_close():
            stop_audio()
            player_window.destroy()
        
        player_window.protocol("WM_DELETE_WINDOW", on_close)
        
        self.update_status("Reproductor de audio abierto")
        
    def show_key_concepts(self):
        """Muestra los conceptos clave"""
        if not self.app.texts:
            messagebox.showwarning(
                "Advertencia",
                "No hay contenido procesado.\nProcesa algunos archivos primero."
            )
            return
            
        self.clear_content()
        self.header_label.config(text="💡 Conceptos Clave")
        self.update_status("Extrayendo conceptos clave...")
        
        # Frame de carga
        loading_frame = tk.Frame(self.content_inner, bg=self.colors['white'])
        loading_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(
            loading_frame,
            text="⏳ Extrayendo conceptos clave...",
            bg=self.colors['white'],
            fg=self.colors['primary'],
            font=('Segoe UI', 12, 'bold')
        ).pack(pady=50)
        
        # Extraer conceptos en un hilo
        def extract_concepts():
            all_concepts = []
            for text in self.app.texts:
                concepts = self.app.content_processor.extract_key_concepts(text)
                all_concepts.extend(concepts)
                
            unique_concepts = list(set(all_concepts))
            self.root.after(0, lambda: self._show_concepts(unique_concepts))
            
        threading.Thread(target=extract_concepts, daemon=True).start()
        
    def _show_concepts(self, concepts):
        """Muestra los conceptos extraídos"""
        self.clear_content()
        self.header_label.config(text="💡 Conceptos Clave")
        
        if not concepts:
            tk.Label(
                self.content_inner,
                text="⚠️ No se encontraron conceptos clave",
                bg=self.colors['bg'],
                fg=self.colors['warning'],
                font=('Segoe UI', 14, 'bold')
            ).pack(pady=50)
            return
            
        # Frame para conceptos
        concepts_frame = tk.Frame(self.content_inner, bg=self.colors['white'])
        concepts_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(
            concepts_frame,
            text=f"Se encontraron {len(concepts)} conceptos únicos",
            bg=self.colors['white'],
            fg=self.colors['primary'],
            font=('Segoe UI', 12, 'bold')
        ).pack(pady=10)
        
        # Lista de conceptos
        text_widget = scrolledtext.ScrolledText(
            concepts_frame,
            wrap=tk.WORD,
            font=('Segoe UI', 10),
            bg=self.colors['bg'],
            fg=self.colors['text'],
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        text_widget.pack(fill=tk.BOTH, expand=True, pady=10)
        
        for i, concept in enumerate(concepts[:50], 1):  # Mostrar los primeros 50
            text_widget.insert(tk.END, f"{i}. {concept}\n")
            
        text_widget.config(state=tk.DISABLED)
        
        self.update_status(f"{len(concepts)} conceptos clave encontrados")
        
    def exit_app(self):
        """Sale de la aplicación"""
        if messagebox.askyesno("Salir", "¿Estás seguro de que quieres salir?"):
            self.root.quit()


def main():
    """Función principal para iniciar la GUI"""
    root = tk.Tk()
    app = StudyBoxGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()


