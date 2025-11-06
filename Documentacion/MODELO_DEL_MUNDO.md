# 📐 Modelo del Mundo - StudyBox

## Guía Completa del Modelo de Dominio y Arquitectura

**Proyecto:** StudyBox - Aplicación de Estudio Inteligente  
**Autores:** José Manuel Jaramillo, Samuel Romaña, Nicolás Peña  
**Fecha:** Noviembre 2025

---

## 📋 Tabla de Contenidos

1. [Introducción y Contexto](#introducción-y-contexto)
2. [Modelo de Dominio](#modelo-de-dominio)
3. [Arquitectura del Sistema](#arquitectura-del-sistema)
4. [Componentes Principales](#componentes-principales)
5. [Flujo de Datos](#flujo-de-datos)
6. [Patrones de Diseño](#patrones-de-diseño)
7. [Casos de Uso](#casos-de-uso)
8. [Diagrama de Clases](#diagrama-de-clases)

---

## 1. Introducción y Contexto

### ¿Qué es StudyBox?

StudyBox es una aplicación de estudio inteligente que utiliza Inteligencia Artificial (Google Gemini) para ayudar a estudiantes a procesar, analizar y estudiar materiales educativos de manera más efectiva.

### Problema que Resuelve

- **Sobrecarga de información:** Los estudiantes tienen mucho material que estudiar
- **Falta de herramientas interactivas:** Materiales estáticos sin retroalimentación
- **Tiempo limitado:** Necesidad de optimizar el estudio
- **Diferentes estilos de aprendizaje:** No todos aprenden de la misma manera

### Solución Propuesta

Una aplicación multiplataforma que:
- Procesa automáticamente materiales de estudio
- Genera herramientas de aprendizaje interactivas
- Proporciona retroalimentación inmediata
- Se adapta a diferentes estilos de aprendizaje

---

## 2. Modelo de Dominio

### 2.1 Conceptos Principales

#### 📄 **Documento/Archivo**
- **Definición:** Material de estudio original que el usuario quiere procesar
- **Tipos:** TXT, PDF, DOCX, MD, código fuente, audio
- **Atributos:**
  - Nombre del archivo
  - Tipo de archivo
  - Tamaño
  - Ruta de almacenamiento
  - Fecha de subida
- **Operaciones:**
  - Subir
  - Procesar
  - Eliminar
  - Listar

#### 📝 **Contenido Procesado**
- **Definición:** Texto extraído y limpiado del documento original
- **Atributos:**
  - Texto limpio
  - Metadatos (origen, fecha de procesamiento)
  - Conceptos clave extraídos
  - Resumen
- **Operaciones:**
  - Extraer
  - Limpiar
  - Analizar
  - Almacenar

#### 🤖 **Herramienta de Estudio**
Concepto abstracto que engloba todas las herramientas generadas:
- Flashcards
- Quizzes
- Audio
- Chatbot
- Resúmenes

#### 🃏 **Flashcard**
- **Definición:** Tarjeta de estudio con pregunta y respuesta
- **Atributos:**
  - Pregunta (Q)
  - Respuesta (A)
  - Tipo (automática, concepto, definición)
  - Fecha de creación
- **Operaciones:**
  - Generar
  - Estudiar
  - Guardar
  - Exportar

#### 🎯 **Quiz**
- **Definición:** Evaluación interactiva del conocimiento
- **Atributos:**
  - Lista de preguntas
  - Tipo (opción múltiple, verdadero/falso, etc.)
  - Puntaje
  - Fecha de creación
- **Operaciones:**
  - Generar
  - Responder
  - Calificar
  - Guardar resultados

#### 🎵 **Audio**
- **Definición:** Narración de texto a voz
- **Atributos:**
  - Script de texto
  - Archivo de audio generado
  - Tipo (resumen, explicación, etc.)
  - Duración
- **Operaciones:**
  - Generar script
  - Convertir a audio
  - Reproducir
  - Guardar

#### 💬 **Conversación (Chatbot)**
- **Definición:** Interacción pregunta-respuesta con IA
- **Atributos:**
  - Historial de mensajes
  - Contexto del contenido
  - Usuario y asistente
- **Operaciones:**
  - Preguntar
  - Responder
  - Mantener contexto
  - Comandos especiales

#### 👤 **Estudiante (Usuario)**
- **Definición:** Usuario de la aplicación
- **Atributos:**
  - Nombre
  - Archivos subidos
  - Progreso de estudio
  - Configuraciones
- **Operaciones:**
  - Subir archivos
  - Usar herramientas
  - Ver progreso

---

## 3. Arquitectura del Sistema

### 3.1 Patrón Arquitectónico: MVC Modificado

```
┌─────────────────────────────────────────────────────┐
│                    USUARIO                           │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│                   VISTA (View)                       │
│  ┌──────────────┐  ┌──────────────┐                │
│  │  GUI (Tk)    │  │  CLI         │                 │
│  │  main_gui.py │  │  main.py     │                 │
│  │  gui_app.py  │  │  app.py      │                 │
│  └──────────────┘  └──────────────┘                 │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│              CONTROLADOR (Controller)                │
│                                                      │
│  ┌───────────────────────────────────────┐          │
│  │  StudyBoxApp (app.py)                 │          │
│  │  - Coordina todas las operaciones     │          │
│  │  - Gestiona flujo de la aplicación    │          │
│  └───────────────────────────────────────┘          │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│                 MODELO (Model)                       │
│                                                      │
│  ┌──────────────────┐  ┌──────────────────┐        │
│  │  FileManager     │  │ ContentProcessor │        │
│  │  - Gestión de    │  │ - Procesamiento  │        │
│  │    archivos      │  │   con IA         │        │
│  └──────────────────┘  └──────────────────┘        │
│                                                      │
│  ┌────────────────────────────────────────┐         │
│  │         HERRAMIENTAS (Tools)           │         │
│  │  ┌──────────────┐  ┌──────────────┐   │         │
│  │  │ChatbotTool   │  │FlashcardTool │   │         │
│  │  └──────────────┘  └──────────────┘   │         │
│  │  ┌──────────────┐  ┌──────────────┐   │         │
│  │  │QuizTool      │  │AudioGenTool  │   │         │
│  │  └──────────────┘  └──────────────┘   │         │
│  │  ┌──────────────┐                      │         │
│  │  │AudioPlayTool │                      │         │
│  │  └──────────────┘                      │         │
│  └────────────────────────────────────────┘         │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│              ALMACENAMIENTO                          │
│                                                      │
│  📂 src/storage/                                     │
│     ├── 📄 Archivos originales                      │
│     ├── 🃏 flashcards/                              │
│     ├── 🎯 quizzes/                                 │
│     ├── 🎵 generated_audio/                         │
│     ├── 📝 audio_scripts/                           │
│     └── 💾 datos_estudiante.json                    │
└─────────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│              SERVICIOS EXTERNOS                      │
│                                                      │
│  🤖 Google Gemini API (IA)                          │
│  🔊 pyttsx3 (Text-to-Speech local)                  │
│  🎵 pygame (Reproducción de audio)                  │
└─────────────────────────────────────────────────────┘
```

### 3.2 Capas del Sistema

#### **Capa de Presentación**
- **Responsabilidad:** Interfaz con el usuario
- **Componentes:**
  - `gui_app.py` - Interfaz gráfica con Tkinter
  - `main_gui.py` - Punto de entrada GUI
  - `main.py` - Punto de entrada CLI
  - `app.py` - Lógica de presentación CLI

#### **Capa de Lógica de Negocio**
- **Responsabilidad:** Operaciones principales de la aplicación
- **Componentes:**
  - `StudyBoxApp` - Orquestador principal
  - `ContentProcessor` - Procesamiento con IA
  - Herramientas especializadas

#### **Capa de Datos**
- **Responsabilidad:** Almacenamiento y gestión de archivos
- **Componentes:**
  - `FileManager` - Gestor de archivos
  - Sistema de archivos JSON para metadatos
  - Almacenamiento de archivos generados

#### **Capa de Servicios**
- **Responsabilidad:** Integración con servicios externos
- **Componentes:**
  - Cliente de Google Gemini
  - Motor TTS
  - Reproductor de audio

---

## 4. Componentes Principales

### 4.1 FileManager (Gestor de Archivos)

**Propósito:** Gestionar todos los archivos del sistema

**Responsabilidades:**
- Subir archivos
- Listar archivos almacenados
- Eliminar archivos
- Validar extensiones
- Gestionar rutas de almacenamiento

**Métodos principales:**
```python
- upload_file(file_path: str) -> str
- list_files() -> List[str]
- delete_file(filename: str) -> bool
- get_file_path(filename: str) -> str
- get_supported_extensions() -> List[str]
```

**Extensiones soportadas:**
- Documentos: `.txt`, `.pdf`, `.docx`, `.doc`, `.md`
- Código: `.py`, `.js`, `.java`, `.cpp`, `.c`, `.json`, `.csv`
- Audio: `.mp3`, `.wav`

### 4.2 ContentProcessor (Procesador de Contenido)

**Propósito:** Extraer y procesar contenido con IA

**Responsabilidades:**
- Extraer texto de diferentes formatos
- Limpiar y mejorar texto con IA
- Generar resúmenes
- Extraer conceptos clave

**Métodos principales:**
```python
- process_text(file_path: str) -> str
- process_audio(file_path: str) -> str
- clean_and_improve_text(text: str) -> str
- extract_key_concepts(text: str) -> List[str]
- generate_summary(text: str) -> str
```

**Integración con IA:**
- Usa Google Gemini API
- Fallback a modo simulado sin API
- Manejo de diferentes versiones de modelos

### 4.3 ChatbotTool (Herramienta de Chat)

**Propósito:** Interacción conversacional sobre el contenido

**Responsabilidades:**
- Responder preguntas
- Mantener contexto
- Generar resúmenes
- Extraer conceptos
- Proporcionar ejemplos

**Características:**
- Historial de conversación (últimas 10 interacciones)
- Comandos especiales: `resumen`, `conceptos`, `ejemplos`
- Respuestas contextuales basadas en el contenido procesado

### 4.4 FlashcardTool (Generador de Flashcards)

**Propósito:** Crear tarjetas de estudio

**Tipos de flashcards:**
1. **Automáticas:** Contenido general
2. **Conceptos clave:** Enfocadas en definiciones
3. **Definiciones:** Términos importantes

**Generación:**
- Con IA: Análisis inteligente del contenido
- Sin IA: Extracción basada en patrones

**Formato:**
```json
{
  "Q": "Pregunta",
  "A": "Respuesta"
}
```

### 4.5 QuizTool (Generador de Quizzes)

**Propósito:** Crear evaluaciones interactivas

**Tipos de quiz:**
1. **Opción múltiple:** 4 opciones, 1 correcta
2. **Verdadero/Falso:** Afirmaciones
3. **Completar espacios:** Palabras faltantes
4. **Preguntas abiertas:** Respuestas elaboradas
5. **Mixto:** Combinación de tipos

**Características:**
- Número configurable de preguntas (3-15)
- Calificación automática
- Feedback inmediato
- Guardado de resultados

### 4.6 AudioGeneratorTool (Generador de Audio)

**Propósito:** Convertir texto a audio narrado

**Tipos de audio:**
1. **Resumen narrado:** Síntesis conversacional
2. **Explicación de conceptos:** Detalles pedagógicos
3. **Lectura completa:** Todo el contenido
4. **Preguntas y respuestas:** Formato Q&A
5. **Historia/conversación:** Narrativa
6. **Guía de estudio:** Paso a paso

**Proceso:**
1. Generar script con IA (o simulado)
2. Guardar script como texto
3. Convertir a audio con TTS (pyttsx3)
4. Guardar archivo de audio

### 4.7 AudioPlayerTool (Reproductor)

**Propósito:** Reproducir archivos de audio generados

**Características:**
- Play/Pause/Stop
- Lista de archivos disponibles
- Controles integrados en GUI
- Soporte MP3 y WAV

---

## 5. Flujo de Datos

### 5.1 Flujo Principal de Estudio

```
1. USUARIO → Sube archivo
          ↓
2. FileManager → Guarda en storage/
          ↓
3. USUARIO → Selecciona "Procesar archivos"
          ↓
4. FileManager → Lee archivo
          ↓
5. ContentProcessor → Extrae texto
          ↓
6. ContentProcessor → Limpia con IA (opcional)
          ↓
7. APLICACIÓN → Almacena texto procesado
          ↓
8. USUARIO → Usa herramientas de estudio
```

### 5.2 Flujo de Generación de Flashcards

```
1. USUARIO → Selecciona tipo de flashcard
          ↓
2. FlashcardTool → Recibe contenido procesado
          ↓
3. FlashcardTool → Genera con IA o modo simple
          ↓
4. FlashcardTool → Crea lista de {Q, A}
          ↓
5. FlashcardTool → Guarda JSON en storage/flashcards/
          ↓
6. GUI → Muestra flashcards en pantalla
```

### 5.3 Flujo de Quiz Interactivo

```
1. USUARIO → Selecciona tipo y número de preguntas
          ↓
2. QuizTool → Genera preguntas con IA
          ↓
3. GUI → Muestra pregunta por pregunta
          ↓
4. USUARIO → Responde cada pregunta
          ↓
5. GUI → Verifica respuesta inmediatamente
          ↓
6. GUI → Actualiza puntaje
          ↓
7. GUI → Muestra resultado final con porcentaje
```

### 5.4 Flujo de Chat

```
1. USUARIO → Escribe pregunta
          ↓
2. ChatbotTool → Recibe pregunta + contexto
          ↓
3. ChatbotTool → Consulta a Gemini API
          ↓
4. ChatbotTool → Agrega a historial
          ↓
5. GUI → Muestra respuesta
          ↓
6. (Repite para siguiente pregunta con contexto)
```

---

## 6. Patrones de Diseño

### 6.1 Patrón Strategy (Estrategia)

**Aplicación:** Generación de contenido con/sin IA

```python
# Interfaz común
class ContentGenerator:
    def generate(self, context):
        pass

# Estrategia con IA
class AIGenerator(ContentGenerator):
    def generate(self, context):
        return gemini_api.generate(context)

# Estrategia sin IA (fallback)
class SimpleGenerator(ContentGenerator):
    def generate(self, context):
        return regex_based_extraction(context)

# Uso
generator = AIGenerator() if api_available else SimpleGenerator()
content = generator.generate(context)
```

**Beneficio:** Flexibilidad para usar IA o modo simulado

### 6.2 Patrón Facade (Fachada)

**Aplicación:** StudyBoxApp como fachada

```python
class StudyBoxApp:
    def __init__(self):
        self.file_manager = FileManager()
        self.content_processor = ContentProcessor()
        self.chatbot = ChatbotTool()
        self.flashcard_generator = FlashcardTool()
        # ... más herramientas
    
    def start_flashcards(self):
        # Coordina múltiples componentes
        texts = self.texts  # Contenido procesado
        self.flashcard_generator.generate_flashcards(texts)
```

**Beneficio:** Simplifica la interfaz para componentes complejos

### 6.3 Patrón Singleton (Implícito)

**Aplicación:** FileManager y almacenamiento

```python
class FileManager:
    STORAGE_DIR = "src/storage/"  # Directorio compartido
    
    @staticmethod
    def list_files():
        # Acceso a recurso compartido
```

**Beneficio:** Un solo punto de acceso al almacenamiento

### 6.4 Patrón Observer (en GUI)

**Aplicación:** Actualización de interfaz con threading

```python
def generate_quiz():
    # Hilo de trabajo
    threading.Thread(target=long_task).start()
    
def long_task():
    result = heavy_computation()
    # Notificar a la GUI
    window.after(0, lambda: update_ui(result))
```

**Beneficio:** Interfaz responsive durante operaciones largas

### 6.5 Patrón Factory Method (Implícito)

**Aplicación:** Creación de diferentes tipos de quiz/flashcards

```python
def create_quiz(quiz_type):
    if quiz_type == "multiple_choice":
        return MultipleChoiceQuiz()
    elif quiz_type == "true_false":
        return TrueFalseQuiz()
    # etc.
```

**Beneficio:** Encapsulación de la lógica de creación

---

## 7. Casos de Uso

### 7.1 Caso de Uso: Generar Flashcards

**Actor:** Estudiante

**Precondiciones:**
- El estudiante ha subido y procesado al menos un archivo

**Flujo Principal:**
1. El estudiante selecciona "Flashcards" en el menú
2. El sistema muestra tipos de flashcards disponibles
3. El estudiante selecciona un tipo (ej: "Conceptos")
4. El sistema genera flashcards usando IA
5. El sistema muestra las flashcards generadas
6. El sistema guarda las flashcards en JSON

**Postcondiciones:**
- Las flashcards están guardadas y disponibles para estudio

**Flujo Alternativo:**
- 4a. Si no hay IA disponible, genera flashcards simples

### 7.2 Caso de Uso: Realizar Quiz

**Actor:** Estudiante

**Precondiciones:**
- Contenido procesado disponible

**Flujo Principal:**
1. Estudiante selecciona "Quiz"
2. Sistema muestra tipos de quiz
3. Estudiante selecciona tipo
4. Estudiante selecciona número de preguntas (3-15)
5. Sistema genera quiz
6. Para cada pregunta:
   - Sistema muestra pregunta
   - Estudiante responde
   - Sistema verifica respuesta
   - Sistema muestra feedback inmediato
   - Sistema actualiza puntaje
7. Sistema muestra resultado final con porcentaje

**Postcondiciones:**
- El estudiante conoce su rendimiento
- El quiz se guarda con resultados

### 7.3 Caso de Uso: Chatear con Asistente

**Actor:** Estudiante

**Precondiciones:**
- Contenido procesado disponible

**Flujo Principal:**
1. Estudiante abre chatbot
2. Sistema carga contexto del contenido
3. Estudiante escribe pregunta
4. Sistema envía pregunta + contexto a IA
5. Sistema muestra respuesta
6. Sistema mantiene historial
7. Se repite desde paso 3

**Comandos Especiales:**
- "resumen": Genera resumen del contenido
- "conceptos": Extrae conceptos clave
- "ejemplos": Genera ejemplos prácticos

---

## 8. Diagrama de Clases

### 8.1 Diagrama Simplificado

```
┌─────────────────────┐
│   StudyBoxApp       │
├─────────────────────┤
│ - texts: List[str]  │
│ - file_manager      │
│ - content_processor │
│ - chatbot           │
│ - flashcard_gen     │
│ - quiz_gen          │
│ - audio_gen         │
│ - audio_player      │
├─────────────────────┤
│ + upload_file()     │
│ + process_files()   │
│ + start_chatbot()   │
│ + start_flashcards()│
│ + start_quiz()      │
└──────────┬──────────┘
           │
           │ usa
           │
     ┌─────┴─────────────────────────────────┐
     │                                        │
     ▼                                        ▼
┌──────────────────┐                  ┌──────────────────┐
│  FileManager     │                  │ContentProcessor  │
├──────────────────┤                  ├──────────────────┤
│ + STORAGE_DIR    │                  │ - model          │
├──────────────────┤                  │ - ai_available   │
│ + upload_file()  │                  ├──────────────────┤
│ + list_files()   │                  │ + process_text() │
│ + delete_file()  │                  │ + clean_text()   │
│ + get_file_path()│                  │ + extract_key()  │
└──────────────────┘                  └──────────────────┘
     │
     │ gestiona
     │
     ▼
┌──────────────────┐
│    Archivo       │
├──────────────────┤
│ - nombre         │
│ - ruta           │
│ - tipo           │
│ - tamaño         │
└──────────────────┘
```

### 8.2 Jerarquía de Herramientas

```
         ┌──────────────┐
         │   Tool       │  (Concepto abstracto)
         └──────┬───────┘
                │
     ┌──────────┴──────────────────────────┐
     │                                      │
     ▼                                      ▼
┌──────────────┐                     ┌──────────────┐
│ChatbotTool   │                     │FlashcardTool │
├──────────────┤                     ├──────────────┤
│- model       │                     │- model       │
│- ai_available│                     │- ai_available│
├──────────────┤                     ├──────────────┤
│+ chat()      │                     │+ generate()  │
│+ _prepare()  │                     │+ _generate_ai│
│+ _generate() │                     │+ _generate_  │
└──────────────┘                     │  simple()    │
                                     └──────────────┘
     │                                      │
     │                                      │
     ▼                                      ▼
┌──────────────┐                     ┌──────────────┐
│QuizTool      │                     │AudioGenTool  │
├──────────────┤                     ├──────────────┤
│- model       │                     │- model       │
│- ai_available│                     │- ai_available│
├──────────────┤                     │- tts_engine  │
│+ generate()  │                     ├──────────────┤
│+ _generate_  │                     │+ generate()  │
│  multiple()  │                     │+ _generate_  │
│+ _generate_  │                     │  summary()   │
│  tf()        │                     │+ _generate_  │
└──────────────┘                     │  concepts()  │
                                     └──────────────┘
     │
     ▼
┌──────────────┐
│AudioPlayTool │
├──────────────┤
│- is_playing  │
│- current_file│
├──────────────┤
│+ play()      │
│+ pause()     │
│+ stop()      │
└──────────────┘
```

### 8.3 Relaciones entre Clases

**Composición:**
- `StudyBoxApp` **tiene** `FileManager`
- `StudyBoxApp` **tiene** `ContentProcessor`
- `StudyBoxApp` **tiene** múltiples `Tool`s

**Dependencia:**
- `ContentProcessor` **depende de** Gemini API
- `AudioGeneratorTool` **depende de** pyttsx3
- `AudioPlayerTool` **depende de** pygame
- Todas las herramientas **dependen de** contenido procesado

**Asociación:**
- `FileManager` **gestiona** `Archivos`
- `Quiz` **contiene** múltiples `Preguntas`
- `Flashcard` **asociada con** contenido específico

---

## 9. Tecnologías y Dependencias

### 9.1 Tecnologías Core

| Tecnología | Propósito | Versión |
|------------|-----------|---------|
| Python | Lenguaje principal | 3.13+ |
| Tkinter | Interfaz gráfica | Incluido en Python |
| Google Gemini API | Inteligencia Artificial | Latest |
| pyttsx3 | Text-to-Speech | 2.90+ |
| pygame | Reproducción de audio | 2.5.0+ |

### 9.2 Librerías de Procesamiento

| Librería | Uso |
|----------|-----|
| pdfplumber | Extracción de texto de PDF |
| python-docx | Lectura de archivos DOCX |
| SpeechRecognition | Transcripción de audio |
| python-dotenv | Gestión de variables de entorno |

### 9.3 Diagrama de Dependencias

```
StudyBox
├── Python 3.13+
├── google-generativeai (Gemini)
├── pyttsx3 (TTS)
├── pygame (Audio)
├── pdfplumber (PDF)
├── python-docx (Word)
├── SpeechRecognition (Audio → Texto)
├── python-dotenv (.env)
└── tkinter (GUI - incluido)
```

---

## 10. Modelo de Datos

### 10.1 Estructura de Almacenamiento

```
src/storage/
│
├── 📄 Archivos originales
│   ├── documento1.pdf
│   ├── apuntes.txt
│   └── codigo.py
│
├── 🃏 flashcards/
│   ├── flashcards_automaticas_20251106_120000.json
│   └── flashcards_conceptos_20251106_120500.json
│
├── 🎯 quizzes/
│   ├── quiz_multiple_choice_20251106_121000.json
│   └── quiz_verdadero_falso_20251106_121500.json
│
├── 🎵 generated_audio/
│   ├── resumen_narrado_local_tts.wav
│   └── explicacion_conceptos_local_tts.wav
│
├── 📝 audio_scripts/
│   ├── resumen_narrado.txt
│   └── explicacion_conceptos.txt
│
└── 💾 datos_estudiante.json
```

### 10.2 Formato de Flashcards

```json
[
  {
    "Q": "¿Qué es la Programación Orientada a Objetos?",
    "A": "Es un paradigma de programación que organiza el código en objetos que contienen datos y métodos"
  },
  {
    "Q": "¿Qué es una clase?",
    "A": "Una plantilla o molde para crear objetos con características y comportamientos similares"
  }
]
```

### 10.3 Formato de Quiz

```json
{
  "type": "multiple_choice",
  "questions": [
    {
      "question": "¿Qué es una clase en POO?",
      "options": [
        "Una plantilla para crear objetos",
        "Una función especial",
        "Un tipo de dato",
        "Un método estático"
      ],
      "correct": "Una plantilla para crear objetos"
    }
  ],
  "created_at": "2025-11-06T12:00:00",
  "num_questions": 5
}
```

### 10.4 Formato de Datos del Estudiante

```json
{
  "nombre": "Usuario",
  "archivos_procesados": 15,
  "flashcards_generadas": 120,
  "quizzes_completados": 8,
  "puntaje_promedio": 85.5,
  "ultima_sesion": "2025-11-06T14:30:00"
}
```

---

## 11. Restricciones y Limitaciones

### 11.1 Restricciones Técnicas

1. **API de Gemini:**
   - Requiere conexión a internet
   - Límites de tasa de la API
   - Requiere API key válida

2. **Procesamiento de archivos:**
   - PDF con imágenes son lentos
   - Archivos muy grandes (>10MB) pueden fallar
   - Algunos formatos PDF escaneados no se extraen bien

3. **Audio:**
   - TTS local tiene voz robótica
   - Calidad limitada comparada con TTS premium
   - Archivos de audio pueden ser grandes

### 11.2 Limitaciones Funcionales

1. **Sin conexión:**
   - Funciona en modo simulado (respuestas básicas)
   - No hay generación inteligente de contenido

2. **Idioma:**
   - Optimizado para español
   - IA puede responder en inglés ocasionalmente

3. **Almacenamiento:**
   - Almacenamiento local únicamente
   - No hay sincronización en la nube
   - No hay backup automático

---

## 12. Extensibilidad Futura

### 12.1 Mejoras Planificadas

1. **Exportación:**
   - PDF con flashcards
   - Formato Anki
   - CSV para análisis

2. **Colaboración:**
   - Compartir flashcards
   - Sesiones de estudio en grupo
   - Competencias de quiz

3. **Análisis:**
   - Dashboard de progreso
   - Estadísticas de rendimiento
   - Recomendaciones personalizadas

4. **Integración:**
   - Calendario de estudio
   - Recordatorios
   - Integración con Notion/Obsidian

### 12.2 Nuevas Herramientas

- **Mapas Mentales:** Visualización de conceptos
- **Resumen con IA avanzada:** Usando Gemini 2.0
- **Traductor:** Traducir materiales al español
- **OCR mejorado:** Para PDFs escaneados

---

## 13. Conclusiones

### Fortalezas del Modelo

1. **Modularidad:** Componentes independientes y reutilizables
2. **Extensibilidad:** Fácil agregar nuevas herramientas
3. **Usabilidad:** Interfaz gráfica intuitiva
4. **Robustez:** Funciona con y sin IA
5. **Versatilidad:** Múltiples formas de estudiar

### Cumplimiento de Objetivos

✅ **Procesar materiales de estudio** - Completado  
✅ **Generar herramientas interactivas** - Completado  
✅ **Proporcionar retroalimentación** - Completado  
✅ **Interfaz amigable** - Completado  
✅ **Multiplataforma** - Completado  

---

## 14. Referencias

### Documentación del Proyecto

- `README.md` - Documentación general
- `GUIA_GUI.md` - Guía de la interfaz gráfica
- `INICIO_RAPIDO.md` - Guía de inicio rápido

### APIs y Librerías

- [Google Gemini API](https://ai.google.dev/)
- [pyttsx3 Docs](https://pyttsx3.readthedocs.io/)
- [pygame Docs](https://www.pygame.org/docs/)
- [Tkinter Docs](https://docs.python.org/3/library/tkinter.html)

---

**Documento creado:** Noviembre 2025  
**Versión:** 1.0  
**Autores:** José Manuel Jaramillo, Samuel Romaña, Nicolás Peña

---

## Apéndice A: Glosario

| Término | Definición |
|---------|------------|
| **IA** | Inteligencia Artificial |
| **TTS** | Text-to-Speech (Texto a Voz) |
| **GUI** | Graphical User Interface (Interfaz Gráfica de Usuario) |
| **CLI** | Command Line Interface (Interfaz de Línea de Comandos) |
| **API** | Application Programming Interface |
| **MVC** | Model-View-Controller (Patrón arquitectónico) |
| **OCR** | Optical Character Recognition (Reconocimiento Óptico de Caracteres) |
| **JSON** | JavaScript Object Notation (Formato de datos) |

---

## Apéndice B: Comandos Útiles

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar GUI
python main_gui.py

# Ejecutar CLI
python main.py

# Listar archivos del proyecto
tree src/

# Ver estructura de almacenamiento
ls -la src/storage/
```

---

**FIN DEL DOCUMENTO**

