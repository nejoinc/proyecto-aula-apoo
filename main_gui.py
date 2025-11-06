import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
from src.app import StudyBoxApp
from src.file_manager import FileManager

class StudyBoxGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("StudyBox - Aplicacion de Estudio")
        self.root.geometry("1200x700")
        self.root.minsize(900, 600)
        
        self.colors = {
            'primary': '#2C3E50',
            'secondary': '#3498DB',
            'accent': '#E74C3C',
            'success': '#27AE60',
            'warning': '#F39C12',
            'bg': '#ECF0F1',
            'text': '#2C3E50',
            'white': '#FFFFFF'
        }
        
        self.app = StudyBoxApp()
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        frame_principal = ttk.Frame(self.root)
        frame_principal.pack(fill=tk.BOTH, expand=True)
        
        self.crear_sidebar(frame_principal)
        self.crear_area_contenido(frame_principal)
        self.crear_barra_estado()
    
    def crear_sidebar(self, parent):
        sidebar = tk.Frame(parent, bg=self.colors['primary'], width=250)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)
        
        titulo = tk.Label(
            sidebar,
            text="StudyBox",
            bg=self.colors['primary'],
            fg=self.colors['white'],
            font=('Arial', 18, 'bold'),
            pady=20
        )
        titulo.pack()
        
        tk.Frame(sidebar, bg=self.colors['secondary'], height=2).pack(fill=tk.X, padx=10)
        
        self.crear_seccion_label(sidebar, "Gestion de Archivos")
        self.crear_boton_sidebar(sidebar, "Subir Archivo", self.subir_archivo)
        self.crear_boton_sidebar(sidebar, "Procesar Archivos", self.procesar_archivos)
        self.crear_boton_sidebar(sidebar, "Listar Archivos", self.listar_archivos)
        self.crear_boton_sidebar(sidebar, "Eliminar Archivo", self.eliminar_archivo)
        
        tk.Frame(sidebar, bg=self.colors['secondary'], height=1).pack(fill=tk.X, padx=10, pady=10)
        
        self.crear_seccion_label(sidebar, "Herramientas de Estudio")
        self.crear_boton_sidebar(sidebar, "Chatbot", self.abrir_chatbot)
        self.crear_boton_sidebar(sidebar, "Flashcards", self.generar_flashcards)
        self.crear_boton_sidebar(sidebar, "Quiz", self.generar_quiz)
        self.crear_boton_sidebar(sidebar, "Generar Audio", self.generar_audio)
        self.crear_boton_sidebar(sidebar, "Reproducir Audio", self.reproducir_audio)
        self.crear_boton_sidebar(sidebar, "Conceptos Clave", self.mostrar_conceptos)
        
        tk.Frame(sidebar, bg=self.colors['secondary'], height=1).pack(fill=tk.X, padx=10, pady=10)
        
        btn_salir = tk.Button(
            sidebar,
            text="Salir",
            bg=self.colors['accent'],
            fg=self.colors['white'],
            font=('Arial', 10, 'bold'),
            relief=tk.FLAT,
            cursor='hand2',
            command=self.root.quit
        )
        btn_salir.pack(side=tk.BOTTOM, fill=tk.X, padx=15, pady=15)
    
    def crear_seccion_label(self, parent, texto):
        label = tk.Label(
            parent,
            text=texto,
            bg=self.colors['primary'],
            fg=self.colors['secondary'],
            font=('Arial', 11, 'bold'),
            anchor='w',
            padx=15,
            pady=10
        )
        label.pack(fill=tk.X)
    
    def crear_boton_sidebar(self, parent, texto, comando):
        btn = tk.Button(
            parent,
            text=texto,
            bg=self.colors['primary'],
            fg=self.colors['white'],
            font=('Arial', 10),
            relief=tk.FLAT,
            cursor='hand2',
            anchor='w',
            padx=15,
            pady=10,
            command=comando
        )
        btn.pack(fill=tk.X, padx=5, pady=2)
        
        def on_enter(e):
            btn['bg'] = self.colors['secondary']
        
        def on_leave(e):
            btn['bg'] = self.colors['primary']
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
    
    def crear_area_contenido(self, parent):
        contenido_frame = tk.Frame(parent, bg=self.colors['bg'])
        contenido_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        header = tk.Frame(contenido_frame, bg=self.colors['white'], height=80)
        header.pack(fill=tk.X, padx=20, pady=20)
        header.pack_propagate(False)
        
        self.header_label = tk.Label(
            header,
            text="Bienvenido a StudyBox",
            bg=self.colors['white'],
            fg=self.colors['primary'],
            font=('Arial', 20, 'bold'),
            anchor='w'
        )
        self.header_label.pack(side=tk.LEFT, padx=20, pady=20)
        
        canvas_contenido = tk.Canvas(contenido_frame, bg=self.colors['bg'], highlightthickness=0)
        canvas_contenido.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        scrollbar = ttk.Scrollbar(contenido_frame, orient=tk.VERTICAL, command=canvas_contenido.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=(0, 20), padx=(0, 20))
        
        canvas_contenido.configure(yscrollcommand=scrollbar.set)
        
        self.contenido_interno = tk.Frame(canvas_contenido, bg=self.colors['bg'])
        canvas_contenido.create_window((0, 0), window=self.contenido_interno, anchor='nw')
        
        def configurar_scroll(event):
            canvas_contenido.configure(scrollregion=canvas_contenido.bbox("all"))
        
        self.contenido_interno.bind("<Configure>", configurar_scroll)
        
        self.mostrar_pantalla_inicio()
    
    def crear_barra_estado(self):
        self.barra_estado = tk.Label(
            self.root,
            text="Listo",
            bg=self.colors['primary'],
            fg=self.colors['white'],
            font=('Arial', 9),
            anchor='w',
            padx=10
        )
        self.barra_estado.pack(side=tk.BOTTOM, fill=tk.X)
    
    def actualizar_estado(self, mensaje):
        self.barra_estado.config(text=mensaje)
        self.root.update_idletasks()
    
    def limpiar_contenido(self):
        for widget in self.contenido_interno.winfo_children():
            widget.destroy()
    
    def mostrar_pantalla_inicio(self):
        self.limpiar_contenido()
        self.header_label.config(text="Bienvenido a StudyBox")
        
        frame_bienvenida = tk.Frame(self.contenido_interno, bg=self.colors['white'], relief=tk.FLAT)
        frame_bienvenida.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(
            frame_bienvenida,
            text="StudyBox",
            bg=self.colors['white'],
            font=('Arial', 80)
        ).pack(pady=30)
        
        tk.Label(
            frame_bienvenida,
            text="Bienvenido a StudyBox",
            bg=self.colors['white'],
            fg=self.colors['primary'],
            font=('Arial', 24, 'bold')
        ).pack(pady=10)
        
        tk.Label(
            frame_bienvenida,
            text="Tu compañero inteligente de estudio",
            bg=self.colors['white'],
            fg=self.colors['text'],
            font=('Arial', 12)
        ).pack(pady=5)
        
        descripcion = """
StudyBox te ayuda a estudiar de manera mas efectiva.

Funcionalidades principales:
• Procesa tus archivos de estudio (TXT, PDF, DOCX, MD, etc.)
• Chatea con un asistente de IA sobre tu contenido
• Genera flashcards automaticas para repasar
• Crea quizzes personalizados
• Convierte texto a audio para estudiar mientras haces otras cosas
• Extrae conceptos clave de tus materiales

¡Comienza subiendo un archivo desde el menu lateral!
        """
        
        tk.Label(
            frame_bienvenida,
            text=descripcion,
            bg=self.colors['white'],
            fg=self.colors['text'],
            font=('Arial', 11),
            justify=tk.LEFT
        ).pack(pady=20, padx=40)
    
    def subir_archivo(self):
        self.limpiar_contenido()
        self.header_label.config(text="Subir Archivo")
        self.actualizar_estado("Seleccionando archivo...")
        
        extensions = FileManager.get_supported_extensions()
        filetypes = [
            ("Todos los archivos soportados", " ".join([f"*{ext}" for ext in extensions])),
            ("Archivos de texto", "*.txt *.md"),
            ("Codigo", "*.py *.js *.java"),
            ("Todos los archivos", "*.*")
        ]
        
        archivo = filedialog.askopenfilename(
            title="Selecciona un archivo",
            filetypes=filetypes
        )
        
        if archivo:
            try:
                self.app.upload_file(archivo)
                
                resultado = tk.Frame(self.contenido_interno, bg=self.colors['white'])
                resultado.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
                
                tk.Label(
                    resultado,
                    text="✓",
                    bg=self.colors['white'],
                    font=('Arial', 60)
                ).pack(pady=30)
                
                tk.Label(
                    resultado,
                    text="Archivo subido correctamente",
                    bg=self.colors['white'],
                    fg=self.colors['success'],
                    font=('Arial', 16, 'bold')
                ).pack(pady=10)
                
                tk.Label(
                    resultado,
                    text=f"Archivo: {os.path.basename(archivo)}",
                    bg=self.colors['white'],
                    fg=self.colors['text'],
                    font=('Arial', 11)
                ).pack(pady=5)
                
                self.actualizar_estado(f"Archivo subido: {os.path.basename(archivo)}")
                
            except:
                messagebox.showerror("Error", "No se pudo subir el archivo")
                self.actualizar_estado("Error al subir archivo")
        else:
            self.actualizar_estado("Operacion cancelada")
            self.mostrar_pantalla_inicio()
    
    def procesar_archivos(self):
        self.limpiar_contenido()
        self.header_label.config(text="Procesar Archivos")
        self.actualizar_estado("Cargando archivos disponibles...")
        
        archivos_disponibles = self.app._get_all_available_files()
        
        if not archivos_disponibles:
            tk.Label(
                self.contenido_interno,
                text="No hay archivos disponibles",
                bg=self.colors['bg'],
                fg=self.colors['warning'],
                font=('Arial', 14, 'bold')
            ).pack(pady=50)
            
            tk.Label(
                self.contenido_interno,
                text="Sube archivos primero usando la opcion 'Subir Archivo'",
                bg=self.colors['bg'],
                fg=self.colors['text'],
                font=('Arial', 11)
            ).pack(pady=10)
            
            self.actualizar_estado("No hay archivos disponibles")
            return
        
        frame_lista = tk.Frame(self.contenido_interno, bg=self.colors['white'])
        frame_lista.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(
            frame_lista,
            text="Selecciona los archivos a procesar:",
            bg=self.colors['white'],
            fg=self.colors['primary'],
            font=('Arial', 12, 'bold')
        ).pack(pady=10, padx=10, anchor='w')
        
        vars_archivo = []
        canvas = tk.Canvas(frame_lista, bg=self.colors['white'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame_lista, orient=tk.VERTICAL, command=canvas.yview)
        frame_scrollable = tk.Frame(canvas, bg=self.colors['white'])
        
        frame_scrollable.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=frame_scrollable, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        for ruta_archivo in archivos_disponibles:
            var = tk.BooleanVar(value=False)
            vars_archivo.append((var, ruta_archivo))
            
            frame_archivo = tk.Frame(frame_scrollable, bg=self.colors['white'])
            frame_archivo.pack(fill=tk.X, padx=10, pady=5)
            
            cb = tk.Checkbutton(
                frame_archivo,
                variable=var,
                bg=self.colors['white'],
                font=('Arial', 10)
            )
            cb.pack(side=tk.LEFT)
            
            nombre_archivo = os.path.basename(ruta_archivo)
            tamano_archivo = os.path.getsize(ruta_archivo)
            tamano_kb = tamano_archivo / 1024
            
            tk.Label(
                frame_archivo,
                text=f"{nombre_archivo} ({tamano_kb:.1f} KB)",
                bg=self.colors['white'],
                fg=self.colors['text'],
                font=('Arial', 10),
                anchor='w'
            ).pack(side=tk.LEFT, padx=10)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
        
        frame_botones = tk.Frame(frame_lista, bg=self.colors['white'])
        frame_botones.pack(fill=tk.X, pady=10, padx=10)
        
        def seleccionar_todos():
            for var, _ in vars_archivo:
                var.set(True)
        
        def deseleccionar_todos():
            for var, _ in vars_archivo:
                var.set(False)
        
        def procesar_seleccionados():
            archivos_seleccionados = [ruta for var, ruta in vars_archivo if var.get()]
            
            if not archivos_seleccionados:
                messagebox.showwarning("Advertencia", "No se seleccionaron archivos")
                return
            
            self.actualizar_estado(f"Procesando {len(archivos_seleccionados)} archivo(s)...")
            
            try:
                self.app._process_selected_files(archivos_seleccionados)
                messagebox.showinfo("Exito", f"Se procesaron {len(archivos_seleccionados)} archivo(s) correctamente")
                self.actualizar_estado(f"Procesamiento completado: {len(archivos_seleccionados)} archivo(s)")
            except:
                messagebox.showerror("Error", "Error procesando archivos")
        
        tk.Button(
            frame_botones,
            text="Seleccionar Todos",
            bg=self.colors['success'],
            fg=self.colors['white'],
            font=('Arial', 10),
            relief=tk.FLAT,
            cursor='hand2',
            command=seleccionar_todos
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            frame_botones,
            text="Deseleccionar Todos",
            bg=self.colors['warning'],
            fg=self.colors['white'],
            font=('Arial', 10),
            relief=tk.FLAT,
            cursor='hand2',
            command=deseleccionar_todos
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            frame_botones,
            text="Procesar Seleccionados",
            bg=self.colors['secondary'],
            fg=self.colors['white'],
            font=('Arial', 10, 'bold'),
            relief=tk.FLAT,
            cursor='hand2',
            command=procesar_seleccionados
        ).pack(side=tk.RIGHT, padx=5)
        
        self.actualizar_estado(f"{len(archivos_disponibles)} archivo(s) disponible(s)")
    
    def listar_archivos(self):
        self.limpiar_contenido()
        self.header_label.config(text="Archivos Almacenados")
        self.actualizar_estado("Cargando lista de archivos...")
        
        archivos = FileManager.list_files()
        
        if not archivos:
            tk.Label(
                self.contenido_interno,
                text="No hay archivos almacenados",
                bg=self.colors['bg'],
                fg=self.colors['warning'],
                font=('Arial', 14, 'bold')
            ).pack(pady=50)
            
            self.actualizar_estado("No hay archivos almacenados")
            return
        
        frame_lista = tk.Frame(self.contenido_interno, bg=self.colors['white'])
        frame_lista.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(
            frame_lista,
            text=f"Archivos en almacenamiento ({len(archivos)}):",
            bg=self.colors['white'],
            fg=self.colors['primary'],
            font=('Arial', 12, 'bold')
        ).pack(pady=10, padx=10, anchor='w')
        
        frame_tree = tk.Frame(frame_lista, bg=self.colors['white'])
        frame_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(frame_tree)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree = ttk.Treeview(
            frame_tree,
            columns=('Nombre', 'Tamano'),
            show='headings',
            yscrollcommand=scrollbar.set
        )
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=tree.yview)
        
        tree.heading('Nombre', text='Nombre del Archivo')
        tree.heading('Tamano', text='Tamano')
        
        tree.column('Nombre', width=400)
        tree.column('Tamano', width=100)
        
        for nombre_archivo in archivos:
            ruta_archivo = os.path.join(FileManager.STORAGE_DIR, nombre_archivo)
            if os.path.exists(ruta_archivo):
                tamano = os.path.getsize(ruta_archivo)
                tamano_kb = tamano / 1024
                tree.insert('', tk.END, values=(nombre_archivo, f'{tamano_kb:.1f} KB'))
            else:
                tree.insert('', tk.END, values=(nombre_archivo, 'N/A'))
        
        self.actualizar_estado(f"{len(archivos)} archivo(s) almacenado(s)")
    
    def eliminar_archivo(self):
        self.limpiar_contenido()
        self.header_label.config(text="Eliminar Archivo")
        self.actualizar_estado("Cargando archivos...")
        
        archivos = FileManager.list_files()
        
        if not archivos:
            tk.Label(
                self.contenido_interno,
                text="No hay archivos para eliminar",
                bg=self.colors['bg'],
                fg=self.colors['warning'],
                font=('Arial', 14, 'bold')
            ).pack(pady=50)
            
            self.actualizar_estado("No hay archivos")
            return
        
        frame_lista = tk.Frame(self.contenido_interno, bg=self.colors['white'])
        frame_lista.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(
            frame_lista,
            text="Selecciona el archivo a eliminar:",
            bg=self.colors['white'],
            fg=self.colors['primary'],
            font=('Arial', 12, 'bold')
        ).pack(pady=10, padx=10, anchor='w')
        
        frame_listbox = tk.Frame(frame_lista, bg=self.colors['white'])
        frame_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(frame_listbox)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        listbox = tk.Listbox(
            frame_listbox,
            font=('Arial', 10),
            yscrollcommand=scrollbar.set
        )
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)
        
        for nombre_archivo in archivos:
            listbox.insert(tk.END, nombre_archivo)
        
        def eliminar_seleccionado():
            seleccion = listbox.curselection()
            if not seleccion:
                messagebox.showwarning("Advertencia", "Selecciona un archivo para eliminar")
                return
            
            nombre_archivo = listbox.get(seleccion[0])
            
            confirmar = messagebox.askyesno(
                "Confirmar eliminacion",
                f"¿Estas seguro de que quieres eliminar '{nombre_archivo}'?"
            )
            
            if confirmar:
                try:
                    if FileManager.delete_file(nombre_archivo):
                        messagebox.showinfo("Exito", f"Archivo '{nombre_archivo}' eliminado correctamente")
                        self.eliminar_archivo()
                    else:
                        messagebox.showerror("Error", f"No se pudo eliminar '{nombre_archivo}'")
                except:
                    messagebox.showerror("Error", "Error al eliminar el archivo")
        
        tk.Button(
            frame_lista,
            text="Eliminar Seleccionado",
            bg=self.colors['accent'],
            fg=self.colors['white'],
            font=('Arial', 10, 'bold'),
            relief=tk.FLAT,
            cursor='hand2',
            command=eliminar_seleccionado
        ).pack(pady=10)
        
        self.actualizar_estado(f"{len(archivos)} archivo(s) disponible(s) para eliminar")
    
    def abrir_chatbot(self):
        if not self.app.texts:
            messagebox.showwarning(
                "Advertencia",
                "No hay contenido procesado.\nProcesa algunos archivos primero."
            )
            return
        
        ventana_chat = tk.Toplevel(self.root)
        ventana_chat.title("Chatbot de Estudio")
        ventana_chat.geometry("800x600")
        ventana_chat.configure(bg=self.colors['bg'])
        
        header = tk.Frame(ventana_chat, bg=self.colors['primary'], height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="Chatbot de Estudio",
            bg=self.colors['primary'],
            fg=self.colors['white'],
            font=('Arial', 14, 'bold')
        ).pack(pady=15, padx=20, side=tk.LEFT)
        
        frame_chat = tk.Frame(ventana_chat, bg=self.colors['white'])
        frame_chat.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        display_chat = scrolledtext.ScrolledText(
            frame_chat,
            wrap=tk.WORD,
            font=('Arial', 10),
            bg=self.colors['bg'],
            fg=self.colors['text'],
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        display_chat.pack(fill=tk.BOTH, expand=True)
        display_chat.config(state=tk.DISABLED)
        
        frame_entrada = tk.Frame(ventana_chat, bg=self.colors['white'])
        frame_entrada.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        entrada = tk.Entry(
            frame_entrada,
            font=('Arial', 11),
            relief=tk.FLAT,
            bg=self.colors['bg']
        )
        entrada.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, ipady=8, padx=(0, 10))
        
        contexto = self.app.chatbot._prepare_context(self.app.texts)
        historial_conversacion = []
        
        def agregar_mensaje(remitente, mensaje):
            display_chat.config(state=tk.NORMAL)
            display_chat.insert(tk.END, f"\n{remitente}:\n", 'remitente')
            display_chat.insert(tk.END, f"{mensaje}\n", 'mensaje')
            display_chat.see(tk.END)
            display_chat.config(state=tk.DISABLED)
        
        display_chat.tag_config('remitente', foreground=self.colors['primary'], font=('Arial', 10, 'bold'))
        display_chat.tag_config('mensaje', foreground=self.colors['text'])
        
        agregar_mensaje("Asistente", "Hola! Estoy listo para ayudarte con tu material de estudio.\n\nPuedes preguntarme sobre conceptos, pedir resumenes, ejemplos, o hacer preguntas especificas.\n\nComandos especiales:\n- 'resumen' - Genera un resumen del contenido\n- 'conceptos' - Extrae conceptos clave\n- 'ejemplos' - Genera ejemplos practicos")
        
        def enviar_mensaje(event=None):
            entrada_usuario = entrada.get().strip()
            if not entrada_usuario:
                return
            
            entrada.delete(0, tk.END)
            agregar_mensaje("Tu", entrada_usuario)
            
            if entrada_usuario.lower() in ['salir', 'exit', 'quit']:
                ventana_chat.destroy()
                return
            
            try:
                if entrada_usuario.lower() == 'resumen':
                    respuesta = self.app.chatbot._generate_summary(contexto)
                elif entrada_usuario.lower() == 'conceptos':
                    respuesta = self.app.chatbot._extract_concepts(contexto)
                elif entrada_usuario.lower() == 'ejemplos':
                    respuesta = self.app.chatbot._generate_examples(contexto)
                else:
                    respuesta = self.app.chatbot._generate_response(entrada_usuario, contexto, historial_conversacion)
                
                historial_conversacion.append({
                    "user": entrada_usuario,
                    "assistant": respuesta
                })
                
                if len(historial_conversacion) > 10:
                    historial_conversacion = historial_conversacion[-10:]
                
                agregar_mensaje("Asistente", respuesta)
            except:
                error_msg = "Lo siento, ocurrio un error"
                agregar_mensaje("Asistente", error_msg)
        
        btn_enviar = tk.Button(
            frame_entrada,
            text="Enviar",
            bg=self.colors['secondary'],
            fg=self.colors['white'],
            font=('Arial', 10, 'bold'),
            relief=tk.FLAT,
            cursor='hand2',
            command=enviar_mensaje
        )
        btn_enviar.pack(side=tk.RIGHT)
        
        entrada.bind('<Return>', enviar_mensaje)
        entrada.focus()
        
        self.actualizar_estado("Chatbot iniciado")
    
    def generar_flashcards(self):
        if not self.app.texts:
            messagebox.showwarning(
                "Advertencia",
                "No hay contenido procesado.\nProcesa algunos archivos primero."
            )
            return
        
        messagebox.showinfo("Info", "Generando flashcards...\nEsta funcionalidad se ejecutara en la consola")
        self.actualizar_estado("Generador de flashcards")
        self.app.start_flashcard_generator()
    
    def generar_quiz(self):
        if not self.app.texts:
            messagebox.showwarning(
                "Advertencia",
                "No hay contenido procesado.\nProcesa algunos archivos primero."
            )
            return
        
        messagebox.showinfo("Info", "Generando quiz...\nEsta funcionalidad se ejecutara en la consola")
        self.actualizar_estado("Generador de quiz")
        self.app.start_quiz_generator()
    
    def generar_audio(self):
        if not self.app.texts:
            messagebox.showwarning(
                "Advertencia",
                "No hay contenido procesado.\nProcesa algunos archivos primero."
            )
            return
        
        messagebox.showinfo("Info", "Generando audio...\nEsta funcionalidad se ejecutara en la consola")
        self.actualizar_estado("Generador de audio")
        self.app.start_audio_generator()
    
    def reproducir_audio(self):
        messagebox.showinfo("Info", "Abriendo reproductor de audio...\nEsta funcionalidad se ejecutara en la consola")
        self.actualizar_estado("Reproductor de audio")
        self.app.start_audio_player()
    
    def mostrar_conceptos(self):
        if not self.app.texts:
            messagebox.showwarning(
                "Advertencia",
                "No hay contenido procesado.\nProcesa algunos archivos primero."
            )
            return
        
        self.limpiar_contenido()
        self.header_label.config(text="Conceptos Clave")
        self.actualizar_estado("Extrayendo conceptos clave...")
        
        frame_carga = tk.Frame(self.contenido_interno, bg=self.colors['white'])
        frame_carga.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(
            frame_carga,
            text="Extrayendo conceptos clave...",
            bg=self.colors['white'],
            fg=self.colors['primary'],
            font=('Arial', 12, 'bold')
        ).pack(pady=50)
        
        self.root.update()
        
        todos_conceptos = []
        for texto in self.app.texts:
            conceptos = self.app.content_processor.extract_key_concepts(texto)
            for concepto in conceptos:
                todos_conceptos.append(concepto)
        
        conceptos_unicos = list(set(todos_conceptos))
        
        self.limpiar_contenido()
        self.header_label.config(text="Conceptos Clave")
        
        if not conceptos_unicos:
            tk.Label(
                self.contenido_interno,
                text="No se encontraron conceptos clave",
                bg=self.colors['bg'],
                fg=self.colors['warning'],
                font=('Arial', 14, 'bold')
            ).pack(pady=50)
            return
        
        frame_conceptos = tk.Frame(self.contenido_interno, bg=self.colors['white'])
        frame_conceptos.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(
            frame_conceptos,
            text=f"Se encontraron {len(conceptos_unicos)} conceptos unicos",
            bg=self.colors['white'],
            fg=self.colors['primary'],
            font=('Arial', 12, 'bold')
        ).pack(pady=10)
        
        widget_texto = scrolledtext.ScrolledText(
            frame_conceptos,
            wrap=tk.WORD,
            font=('Arial', 10),
            bg=self.colors['bg'],
            fg=self.colors['text'],
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        widget_texto.pack(fill=tk.BOTH, expand=True, pady=10)
        
        i = 1
        for concepto in conceptos_unicos:
            if i <= 50:
                widget_texto.insert(tk.END, f"{i}. {concepto}\n")
                i = i + 1
        
        widget_texto.config(state=tk.DISABLED)
        
        self.actualizar_estado(f"{len(conceptos_unicos)} conceptos clave encontrados")

if __name__ == "__main__":
    root = tk.Tk()
    app = StudyBoxGUI(root)
    root.mainloop()
