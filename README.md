# StudyBox
Una herramienta sencilla para estudiar mejor con tus propios materiales.

---

## ¿Qué hace?
Tomas tus archivos (texto o audio) y los conviertes en herramientas de estudio:
- Resúmenes
- Flashcards
- Quizzes
- Conceptos clave
- Audio narrado

---

## Funciones principales
- 📂 Soporte para TXT, PDF, DOCX, MD, PY, JSON, CSV y audio (MP3/WAV)
- 📝 Extracción y limpieza de texto con IA
- 🤖 Chatbot inteligente para preguntas sobre tu contenido
- 🎵 Generación de audio TTS (local)
- 🃏 Flashcards automáticas con IA
- 🎯 Extracción de conceptos clave
- 💻 **2 interfaces disponibles: CLI y GUI Desktop**

---

## Tecnologías
- **GUI Desktop**: Tkinter (interfaz gráfica de escritorio)
- **CLI**: Python 3.8+
- **IA**: Google Gemini API (opcional, funciona en modo simulado sin ella)
- **TTS**: pyttsx3 (local)
- **Procesamiento**: pdfplumber, python-docx, SpeechRecognition

---

## Instalación rápida
Requisitos:
- Python 3.13+

Windows:
```bash
git clone <repository-url>
cd proyecto-aula-apoo
install_requirements.bat
# o manual
py -m pip install -r requirements.txt
```

Linux/Mac:
```bash
git clone <repository-url>
cd proyecto-aula-apoo
chmod +x install_requirements.sh
./install_requirements.sh
# o manual
python3 -m pip install -r requirements.txt
```

### Configuración
1. Crea un archivo `.env` en la raíz:
```env
GEMINI_API_KEY=tu_api_key_aqui
ELEVENLABS_API_KEY=tu_api_key_aqui  # Optional for premium audio
```

2. Para la API de Gemini:
   - Ve a Google AI Studio y crea tu API key
   - Agrégala al `.env`

### Ejecución

#### Opción 1: Interfaz Gráfica (GUI) ⭐ RECOMENDADO
```bash
# Windows
py main_gui.py

# Linux/Mac
python3 main_gui.py
```

La interfaz gráfica incluye todas las funcionalidades en una ventana moderna e intuitiva:
- 📤 Subir archivos con diálogo visual
- ⚙️ Procesar archivos con selección múltiple
- 🗑️ Gestión de archivos
- 🤖 Chatbot interactivo en ventana de chat
- 🃏 Generador de flashcards con vista previa
- 🎯 Quiz y otras herramientas de estudio
- 💡 Extracción de conceptos clave

#### Opción 2: Interfaz de Consola (CLI)
```bash
# Windows
py main.py

# Linux/Mac
python3 main.py
```

---

## Arquitectura (resumen)
- Ingesta → extrae texto
- Procesado → limpieza y mejoras
- Salidas → resúmenes, flashcards, quiz, audio
- GUI → interfaz Tkinter moderna (opcional)

---

## Equipo
Proyecto desarrollado por:
- José Manuel Jaramillo
- Samuel Romaña
- Nicolás Peña

---

## Roadmap
- [x] Subida de archivos y extracción
- [x] Procesamiento con IA
- [x] Chat de preguntas
- [x] Generación de audio
- [x] Conceptos clave
- [x] Resúmenes
- [x] Flashcards
- [x] Quizzes
- [x] **Interfaz gráfica de escritorio (GUI)**
- [ ] Exportación (PDF, CSV, Anki)
- [ ] Modo colaborativo
- [ ] App móvil
- [ ] Drag & drop de archivos
- [ ] Dashboard de progreso

---

## Contribuciones
¡Bienvenidas!
1. Haz fork
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit
4. Push
5. Abre un Pull Request

---

## Licencia
MIT. Ver [LICENSE](./LICENSE).

---
