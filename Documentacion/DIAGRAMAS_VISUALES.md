# 📊 Diagramas Visuales - StudyBox

## Complemento al Modelo del Mundo

Este documento contiene diagramas visuales detallados para complementar el documento `MODELO_DEL_MUNDO.md`

---

## 1. Diagrama de Arquitectura Completo

```
┌──────────────────────────────────────────────────────────────────────┐
│                          CAPA DE PRESENTACIÓN                         │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌─────────────────────────────┐   ┌──────────────────────────────┐ │
│  │    GUI (Tkinter)            │   │    CLI (Terminal)            │ │
│  │                              │   │                              │ │
│  │  ┌────────────────────────┐ │   │  ┌────────────────────────┐ │ │
│  │  │  main_gui.py           │ │   │  │  main.py               │ │ │
│  │  │  - Punto de entrada    │ │   │  │  - Punto de entrada    │ │ │
│  │  └────────────────────────┘ │   │  └────────────────────────┘ │ │
│  │                              │   │                              │ │
│  │  ┌────────────────────────┐ │   │  ┌────────────────────────┐ │ │
│  │  │  gui_app.py            │ │   │  │  app.py (CLI Logic)    │ │ │
│  │  │  - StudyBoxGUI         │ │   │  │  - Menu loops          │ │ │
│  │  │  - Ventanas            │ │   │  │  - Input/Output        │ │ │
│  │  │  - Eventos             │ │   │  │  - Console formatting  │ │ │
│  │  └────────────────────────┘ │   │  └────────────────────────┘ │ │
│  └─────────────────────────────┘   └──────────────────────────────┘ │
│                                                                       │
└───────────────────────────────┬───────────────────────────────────────┘
                                │
                                │ Llamadas de funciones
                                ▼
┌──────────────────────────────────────────────────────────────────────┐
│                       CAPA DE LÓGICA DE NEGOCIO                      │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────────┐│
│  │                     StudyBoxApp (app.py)                        ││
│  │                     Orquestador Principal                       ││
│  │                                                                 ││
│  │  Atributos:                                                     ││
│  │    - texts: List[str]          (Contenido procesado)           ││
│  │    - file_manager              (Gestor de archivos)            ││
│  │    - content_processor         (Procesador con IA)             ││
│  │    - chatbot                   (Herramienta de chat)           ││
│  │    - flashcard_generator       (Generador de flashcards)       ││
│  │    - quiz_generator            (Generador de quizzes)          ││
│  │    - audio_generator           (Generador de audio)            ││
│  │    - audio_player              (Reproductor de audio)          ││
│  │                                                                 ││
│  │  Métodos principales:                                           ││
│  │    + upload_file(path)         → Sube archivo                  ││
│  │    + process_files(files)      → Procesa contenido             ││
│  │    + start_chatbot()           → Inicia chat                   ││
│  │    + start_flashcards()        → Genera flashcards             ││
│  │    + start_quiz()              → Genera quiz                   ││
│  │    + start_audio_generator()   → Genera audio                  ││
│  │    + start_audio_player()      → Reproduce audio               ││
│  └─────────────────────────────────────────────────────────────────┘│
│                                                                       │
│  ┌───────────────┐  ┌────────────────┐  ┌──────────────────────┐   │
│  │ FileManager   │  │ContentProcessor│  │   Tools Package      │   │
│  ├───────────────┤  ├────────────────┤  ├──────────────────────┤   │
│  │ + upload()    │  │ + process()    │  │ ChatbotTool          │   │
│  │ + list()      │  │ + clean()      │  │ FlashcardTool        │   │
│  │ + delete()    │  │ + extract()    │  │ QuizTool             │   │
│  │ + get_path()  │  │ + summarize()  │  │ AudioGeneratorTool   │   │
│  └───────────────┘  └────────────────┘  │ AudioPlayerTool      │   │
│                                          └──────────────────────┘   │
└───────────────────────────────┬───────────────────────────────────────┘
                                │
                                │ Lee/Escribe
                                ▼
┌──────────────────────────────────────────────────────────────────────┐
│                        CAPA DE PERSISTENCIA                          │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  📂 src/storage/                                                      │
│    │                                                                  │
│    ├── 📄 archivos_originales/                                       │
│    │     ├── documento1.pdf                                          │
│    │     ├── apuntes.txt                                             │
│    │     └── codigo.py                                               │
│    │                                                                  │
│    ├── 🃏 flashcards/                                                │
│    │     ├── flashcards_automaticas_20251106.json                    │
│    │     └── flashcards_conceptos_20251106.json                      │
│    │                                                                  │
│    ├── 🎯 quizzes/                                                   │
│    │     ├── quiz_multiple_choice_20251106.json                      │
│    │     └── quiz_verdadero_falso_20251106.json                      │
│    │                                                                  │
│    ├── 🎵 generated_audio/                                           │
│    │     ├── resumen_narrado_local_tts.wav                           │
│    │     └── explicacion_conceptos_local_tts.wav                     │
│    │                                                                  │
│    ├── 📝 audio_scripts/                                             │
│    │     ├── resumen_narrado.txt                                     │
│    │     └── explicacion_conceptos.txt                               │
│    │                                                                  │
│    └── 💾 datos_estudiante.json                                      │
│                                                                       │
└───────────────────────────────┬───────────────────────────────────────┘
                                │
                                │ API Calls
                                ▼
┌──────────────────────────────────────────────────────────────────────┐
│                      SERVICIOS EXTERNOS                              │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐  │
│  │  Google Gemini   │  │    pyttsx3       │  │     pygame       │  │
│  │      API         │  │   (TTS Local)    │  │  (Audio Player)  │  │
│  ├──────────────────┤  ├──────────────────┤  ├──────────────────┤  │
│  │ - Generación IA  │  │ - Texto a voz    │  │ - Reproducción   │  │
│  │ - Chat           │  │ - Múltiples voces│  │ - Controles      │  │
│  │ - Resúmenes      │  │ - Ajuste veloc.  │  │ - Formatos       │  │
│  │ - Análisis       │  │ - Offline        │  │ - MP3/WAV        │  │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘  │
│                                                                       │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐  │
│  │   pdfplumber     │  │   python-docx    │  │ SpeechRecognition│  │
│  │   (PDF Reader)   │  │  (Word Reader)   │  │ (Audio→Text)     │  │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘  │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
```

---

## 2. Diagrama de Secuencia: Generar y Estudiar con Flashcards

```
Usuario      GUI          StudyBoxApp    FlashcardTool    Gemini API    Storage
  │           │                │               │              │            │
  │ 1. Clic   │                │               │              │            │
  │ Flashcard │                │               │              │            │
  ├──────────>│                │               │              │            │
  │           │ 2. Tipo?       │               │              │            │
  │           ├───────────────>│               │              │            │
  │           │                │ 3. Generar    │              │            │
  │           │                ├──────────────>│              │            │
  │           │                │               │ 4. Prompt    │            │
  │           │                │               ├─────────────>│            │
  │           │                │               │              │            │
  │           │                │               │ 5. Response  │            │
  │           │                │               │<─────────────┤            │
  │           │                │ 6. Flashcards │              │            │
  │           │                │<──────────────┤              │            │
  │           │                │               │ 7. Guardar   │            │
  │           │                │               ├──────────────────────────>│
  │           │                │               │              │ 8. JSON    │
  │           │                │               │              │<───────────┤
  │           │ 9. Mostrar     │               │              │            │
  │           │<───────────────┤               │              │            │
  │ 10. Ver   │                │               │              │            │
  │<──────────┤                │               │              │            │
  │           │                │               │              │            │
```

---

## 3. Diagrama de Secuencia: Quiz Interactivo

```
Usuario      GUI         StudyBoxApp    QuizTool     Gemini API    GUI
  │           │              │              │            │          │
  │ 1. Clic   │              │              │            │          │
  │   Quiz    │              │              │            │          │
  ├──────────>│              │              │            │          │
  │           │ 2. Tipo?     │              │            │          │
  │           │<─────────────┤              │            │          │
  │ 3. Multiple              │              │            │          │
  │   Choice  │              │              │            │          │
  ├──────────>│              │              │            │          │
  │           │ 4. Cuántas?  │              │            │          │
  │           │<─────────────┤              │            │          │
  │ 5. 5 preg │              │              │            │          │
  ├──────────>│              │              │            │          │
  │           │ 6. Generar   │              │            │          │
  │           ├─────────────>│ 7. Generate  │            │          │
  │           │              ├─────────────>│ 8. Prompt  │          │
  │           │              │              ├───────────>│          │
  │           │              │              │9. Questions│          │
  │           │              │              │<───────────┤          │
  │           │              │ 10. Quiz     │            │          │
  │           │              │<─────────────┤            │          │
  │           │ 11. Show Q1  │              │            │          │
  │           ├──────────────────────────────────────────────────> │
  │ 12. Ver Q1│              │              │            │          │
  │<───────────────────────────────────────────────────────────────┤
  │ 13. Resp  │              │              │            │          │
  ├──────────>│              │              │            │          │
  │           │ 14. Check    │              │            │          │
  │           ├──────────────────────────────────────────────────> │
  │ 15.Correct│              │              │            │          │
  │<───────────────────────────────────────────────────────────────┤
  │           │ 16. Next Q   │              │            │          │
  │           ├──────────────────────────────────────────────────> │
  │           │              │              │            │          │
  │  ... (repetir para cada pregunta) ...               │          │
  │           │              │              │            │          │
  │           │ 17. Results  │              │            │          │
  │           ├──────────────────────────────────────────────────> │
  │ 18. Score │              │              │            │          │
  │<───────────────────────────────────────────────────────────────┤
  │           │              │              │            │          │
```

---

## 4. Diagrama de Estados: Quiz Interactivo

```
                    ┌──────────────┐
                    │   Inicio     │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  Seleccionar │
                    │     Tipo     │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  Seleccionar │
                    │   Cantidad   │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  Generando   │◄──┐
                    │   Quiz...    │   │
                    └──────┬───────┘   │ Error
                           │           │ (reintentar)
                           ▼           │
                    ┌──────────────┐   │
                    │  Mostrar     │───┘
                    │  Pregunta N  │
                    └──────┬───────┘
                           │
                ┌──────────┴──────────┐
                │                     │
                ▼                     ▼
         ┌─────────────┐       ┌─────────────┐
         │  Responder  │       │   Saltar    │
         └──────┬──────┘       └──────┬──────┘
                │                     │
                ▼                     │
         ┌─────────────┐              │
         │  Verificar  │              │
         │  Respuesta  │              │
         └──────┬──────┘              │
                │                     │
         ┌──────┴──────┐              │
         │             │              │
         ▼             ▼              │
    ┌────────┐   ┌────────┐          │
    │Correcto│   │Incorr. │          │
    └────┬───┘   └────┬───┘          │
         │            │               │
         └────┬───────┘               │
              │◄──────────────────────┘
              ▼
       ┌──────────────┐
       │ Actualizar   │
       │   Puntaje    │
       └──────┬───────┘
              │
       ┌──────┴─────────┐
       │                │
       ▼                ▼
┌─────────────┐  ┌─────────────┐
│ Hay más     │  │ No hay más  │
│ preguntas?  │  │ preguntas   │
└──────┬──────┘  └──────┬──────┘
       │                │
       │                ▼
       │         ┌─────────────┐
       │         │  Mostrar    │
       │         │ Resultados  │
       │         └──────┬──────┘
       │                │
       │                ▼
       │         ┌─────────────┐
       │         │    Fin      │
       │         └─────────────┘
       │
       └────> Volver a "Mostrar Pregunta N"
```

---

## 5. Diagrama de Componentes: Herramientas de Estudio

```
┌────────────────────────────────────────────────────────────────┐
│                    STUDYBOX APPLICATION                         │
└────────────────────────────────────────────────────────────────┘
                              │
           ┌──────────────────┼──────────────────┐
           │                  │                  │
           ▼                  ▼                  ▼
┌───────────────────┐ ┌───────────────────┐ ┌──────────────────┐
│   FileManager     │ │ ContentProcessor  │ │  StudyBoxApp     │
│                   │ │                   │ │  (Controller)    │
│ • upload_file()   │ │ • process_text()  │ │                  │
│ • list_files()    │ │ • clean_text()    │ │ • Coordina       │
│ • delete_file()   │ │ • extract_key()   │ │ • Integra        │
│ • get_path()      │ │ • summarize()     │ │ • Orquesta       │
└─────────┬─────────┘ └─────────┬─────────┘ └────────┬─────────┘
          │                     │                     │
          │                     │                     │
          └─────────────────────┴─────────────────────┘
                                │
                                │ usa
                                │
          ┌─────────────────────┴─────────────────────┐
          │                                            │
          ▼                                            ▼
┌───────────────────────────────────┐    ┌────────────────────────────┐
│      HERRAMIENTAS INTERACTIVAS    │    │   HERRAMIENTAS DE AUDIO    │
├───────────────────────────────────┤    ├────────────────────────────┤
│                                   │    │                            │
│  ┌─────────────────────────────┐ │    │  ┌──────────────────────┐ │
│  │     ChatbotTool             │ │    │  │  AudioGeneratorTool  │ │
│  ├─────────────────────────────┤ │    │  ├──────────────────────┤ │
│  │ • chat()                    │ │    │  │ • generate_audio()   │ │
│  │ • _prepare_context()        │ │    │  │ • _generate_script() │ │
│  │ • _generate_response()      │ │    │  │ • _save_script()     │ │
│  │ • _generate_summary()       │ │    │  │ • _convert_to_tts()  │ │
│  │ • _extract_concepts()       │ │    │  └──────────────────────┘ │
│  │ • _generate_examples()      │ │    │                            │
│  └─────────────────────────────┘ │    │  ┌──────────────────────┐ │
│                                   │    │  │  AudioPlayerTool     │ │
│  ┌─────────────────────────────┐ │    │  ├──────────────────────┤ │
│  │     FlashcardTool           │ │    │  │ • play_audio()       │ │
│  ├─────────────────────────────┤ │    │  │ • pause_audio()      │ │
│  │ • generate_flashcards()     │ │    │  │ • stop_audio()       │ │
│  │ • _generate_ai_flashcards() │ │    │  │ • list_files()       │ │
│  │ • _generate_simple()        │ │    │  └──────────────────────┘ │
│  │ • _save_flashcards()        │ │    │                            │
│  └─────────────────────────────┘ │    └────────────────────────────┘
│                                   │
│  ┌─────────────────────────────┐ │
│  │     QuizTool                │ │
│  ├─────────────────────────────┤ │
│  │ • generate_quiz()           │ │
│  │ • _generate_multiple()      │ │
│  │ • _generate_true_false()    │ │
│  │ • _generate_fill_blank()    │ │
│  │ • _generate_open()          │ │
│  │ • _generate_mixed()         │ │
│  │ • _save_quiz()              │ │
│  └─────────────────────────────┘ │
│                                   │
└───────────────────────────────────┘
```

---

## 6. Diagrama de Flujo: Procesamiento de Archivos

```
                    ┌─────────────┐
                    │   Inicio    │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │ Usuario sube│
                    │   archivo   │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │ FileManager │
                    │ valida tipo │
                    └──────┬──────┘
                           │
                    ┌──────┴──────┐
                    │             │
                ¿Válido?          │
                    │             │
              NO    │       SÍ    │
            ┌───────┘             │
            │                     │
            ▼                     ▼
     ┌─────────────┐       ┌─────────────┐
     │   Mostrar   │       │  Guardar en │
     │    Error    │       │   storage/  │
     └──────┬──────┘       └──────┬──────┘
            │                     │
            │                     ▼
            │              ┌─────────────┐
            │              │Usuario click│
            │              │  "Procesar" │
            │              └──────┬──────┘
            │                     │
            │                     ▼
            │              ┌─────────────┐
            │              │ContentProc. │
            │              │ lee archivo │
            │              └──────┬──────┘
            │                     │
            │              ┌──────┴──────┐
            │              │             │
            │          ¿Tipo?            │
            │              │             │
            │      ┌───────┼───────┐     │
            │      │       │       │     │
            │      ▼       ▼       ▼     │
            │   ┌────┐ ┌────┐ ┌────┐    │
            │   │PDF │ │TXT │ │WAV │    │
            │   └─┬──┘ └─┬──┘ └─┬──┘    │
            │     │      │      │        │
            │     │      │      ▼        │
            │     │      │   ┌────────┐  │
            │     │      │   │Speech  │  │
            │     │      │   │Recog.  │  │
            │     │      │   └───┬────┘  │
            │     │      │       │        │
            │     ▼      ▼       ▼        │
            │   ┌────────────────────┐   │
            │   │  Extraer texto     │   │
            │   └─────────┬──────────┘   │
            │             │               │
            │             ▼               │
            │      ┌─────────────┐        │
            │      │   ¿Usar IA? │        │
            │      └──────┬──────┘        │
            │             │               │
            │      ┌──────┴──────┐        │
            │      │             │        │
            │   SÍ │         NO  │        │
            │      │             │        │
            │      ▼             ▼        │
            │ ┌────────┐   ┌──────────┐  │
            │ │Gemini  │   │ Limpieza │  │
            │ │API     │   │  simple  │  │
            │ │limpia  │   └────┬─────┘  │
            │ └────┬───┘        │        │
            │      │            │        │
            │      └─────┬──────┘        │
            │            │               │
            │            ▼               │
            │     ┌─────────────┐        │
            │     │  Almacenar  │        │
            │     │  texto en   │        │
            │     │  memoria    │        │
            │     └──────┬──────┘        │
            │            │               │
            │            ▼               │
            │     ┌─────────────┐        │
            │     │   Mostrar   │        │
            │     │   éxito     │        │
            │     └──────┬──────┘        │
            │            │               │
            └────────────┼───────────────┘
                         │
                         ▼
                  ┌─────────────┐
                  │ Contenido   │
                  │ disponible  │
                  │ para herr.  │
                  └──────┬──────┘
                         │
                         ▼
                  ┌─────────────┐
                  │     Fin     │
                  └─────────────┘
```

---

## 7. Diagrama de Despliegue

```
┌──────────────────────────────────────────────────────────────────┐
│                      MÁQUINA DEL USUARIO                          │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │             Sistema Operativo (Windows/Linux/Mac)          │ │
│  └────────────────────────────────────────────────────────────┘ │
│                              │                                    │
│                              │                                    │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                   Python 3.13+ Runtime                      │ │
│  ├────────────────────────────────────────────────────────────┤ │
│  │                                                             │ │
│  │  ┌───────────────────────────────────────────────────────┐ │ │
│  │  │             StudyBox Application                      │ │ │
│  │  ├───────────────────────────────────────────────────────┤ │ │
│  │  │                                                        │ │ │
│  │  │  ┌──────────────┐         ┌──────────────┐           │ │ │
│  │  │  │  GUI Module  │         │  CLI Module  │           │ │ │
│  │  │  │  (Tkinter)   │         │  (Terminal)  │           │ │ │
│  │  │  └──────┬───────┘         └──────┬───────┘           │ │ │
│  │  │         │                        │                    │ │ │
│  │  │         └────────────┬───────────┘                    │ │ │
│  │  │                      │                                │ │ │
│  │  │              ┌───────▼────────┐                       │ │ │
│  │  │              │  Core Logic    │                       │ │ │
│  │  │              │  (app.py)      │                       │ │ │
│  │  │              └───────┬────────┘                       │ │ │
│  │  │                      │                                │ │ │
│  │  │         ┌────────────┼────────────┐                   │ │ │
│  │  │         │            │            │                   │ │ │
│  │  │    ┌────▼───┐  ┌────▼────┐  ┌───▼────┐              │ │ │
│  │  │    │File    │  │Content  │  │Tools   │              │ │ │
│  │  │    │Manager │  │Processor│  │Package │              │ │ │
│  │  │    └────────┘  └─────────┘  └────────┘              │ │ │
│  │  │                                                        │ │ │
│  │  └────────────────────────────────────────────────────── │ │ │
│  │                                                             │ │
│  │  ┌───────────────────────────────────────────────────────┐ │ │
│  │  │              Librerías de Python                      │ │ │
│  │  ├───────────────────────────────────────────────────────┤ │ │
│  │  │                                                        │ │ │
│  │  │  • google-generativeai  • pyttsx3    • pygame        │ │ │
│  │  │  • pdfplumber            • python-docx               │ │ │
│  │  │  • SpeechRecognition     • python-dotenv             │ │ │
│  │  │                                                        │ │ │
│  │  └────────────────────────────────────────────────────────┘ │ │
│  │                                                             │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                              │                                    │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │              Sistema de Archivos Local                     │ │
│  ├────────────────────────────────────────────────────────────┤ │
│  │                                                             │ │
│  │  📂 proyecto-aula-apoo/                                     │ │
│  │    ├── src/                                                 │ │
│  │    │   ├── storage/                                         │ │
│  │    │   │   ├── flashcards/                                  │ │
│  │    │   │   ├── quizzes/                                     │ │
│  │    │   │   ├── generated_audio/                             │ │
│  │    │   │   └── datos_estudiante.json                        │ │
│  │    │   └── tools/                                           │ │
│  │    ├── main.py                                              │ │
│  │    └── main_gui.py                                          │ │
│  │                                                             │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                   │
└────────────────────────────┬──────────────────────────────────────┘
                             │
                             │ Internet
                             │ (HTTPS)
                             │
                             ▼
          ┌────────────────────────────────────────┐
          │        SERVICIOS EN LA NUBE            │
          ├────────────────────────────────────────┤
          │                                         │
          │  ┌──────────────────────────────────┐  │
          │  │    Google Gemini API             │  │
          │  │    (generativelanguage.googleapis.com)
          │  ├──────────────────────────────────┤  │
          │  │                                   │  │
          │  │  • Generación de texto           │  │
          │  │  • Análisis de contenido         │  │
          │  │  • Respuestas de chatbot         │  │
          │  │  • Generación de preguntas       │  │
          │  │                                   │  │
          │  └──────────────────────────────────┘  │
          │                                         │
          └─────────────────────────────────────────┘
```

---

## 8. Diagrama de Paquetes

```
┌─────────────────────────────────────────────────────────────────┐
│                    proyecto-aula-apoo                            │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   main.py    │     │ main_gui.py  │     │   src/       │
│              │     │              │     │              │
│ • CLI entry  │     │ • GUI entry  │     │ • Core code  │
└──────────────┘     └──────────────┘     └──────┬───────┘
                                                  │
                    ┌─────────────────────────────┼────────────┐
                    │                             │            │
                    ▼                             ▼            ▼
           ┌──────────────┐            ┌──────────────┐  ┌─────────┐
           │    app.py    │            │  gui_app.py  │  │storage/ │
           │              │            │              │  │         │
           │ • StudyBox   │            │ • StudyBox   │  │ • Data  │
           │   App        │            │   GUI        │  │ • Files │
           └──────┬───────┘            └──────┬───────┘  └─────────┘
                  │                           │
        ┌─────────┼───────────┐              │
        │         │           │              │
        ▼         ▼           ▼              │
┌──────────┐ ┌────────┐ ┌──────────┐        │
│file_     │ │content_│ │ tools/   │        │
│manager.py│ │process │ │          │◄───────┘
│          │ │or.py   │ │          │
└──────────┘ └────────┘ └────┬─────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│chatbot_      │     │flashcard_    │     │quiz_tool.py  │
│tool.py       │     │tool.py       │     │              │
│              │     │              │     │              │
│• Chat logic  │     │• Flashcard   │     │• Quiz gen.   │
│• Context     │     │  generation  │     │• Types       │
│• AI calls    │     │• AI/Simple   │     │• Grading     │
└──────────────┘     └──────────────┘     └──────────────┘

        ▼                     ▼
┌──────────────┐     ┌──────────────┐
│audio_        │     │audio_        │
│generator_    │     │player_       │
│tool.py       │     │tool.py       │
│              │     │              │
│• TTS         │     │• pygame      │
│• Scripts     │     │• Controls    │
└──────────────┘     └──────────────┘
```

---

## 9. Diagrama de Casos de Uso

```
                        SISTEMA STUDYBOX

     ┌────────────────────────────────────────────────┐
     │                                                 │
     │                                                 │
     │  ┌────────────────────────────────┐            │
     │  │  Gestión de Archivos           │            │
     │  │                                 │            │
     │  │  • Subir archivo                │            │
     │  │  • Listar archivos              │◄───────┐   │
     │  │  • Eliminar archivo             │        │   │
     │  │  • Procesar archivos            │        │   │
     │  └────────────────────────────────┘        │   │
     │                                             │   │
     │  ┌────────────────────────────────┐        │   │
     │  │  Herramientas Interactivas     │        │   │
     │  │                                 │        │   │
     │  │  • Generar Flashcards           │        │   │
     │  │    - Automáticas                │        │   │
     │  │    - Conceptos                  │        │   │
     │  │    - Definiciones               │◄───────┤   │
     │  │                                 │        │   │
     │  │  • Generar Quiz                 │        │   │
     │  │    - Opción múltiple            │   ┌────────────┐
     │  │    - Verdadero/Falso            │   │            │
     │  │    - Completar espacios         │   │ Estudiante │
     │  │    - Preguntas abiertas         │   │  (Actor)   │
     │  │    - Mixto                      │   │            │
     │  │                                 │   └────────────┘
     │  │  • Chatbot                      │        │   │
     │  │    - Preguntar                  │        │   │
     │  │    - Solicitar resumen          │        │   │
     │  │    - Extraer conceptos          │◄───────┤   │
     │  │    - Generar ejemplos           │        │   │
     │  │                                 │        │   │
     │  │  • Extraer Conceptos Clave      │        │   │
     │  └────────────────────────────────┘        │   │
     │                                             │   │
     │  ┌────────────────────────────────┐        │   │
     │  │  Herramientas de Audio         │        │   │
     │  │                                 │        │   │
     │  │  • Generar Audio                │        │   │
     │  │    - Resumen narrado            │        │   │
     │  │    - Explicación conceptos      │        │   │
     │  │    - Lectura completa           │        │   │
     │  │    - Preguntas y respuestas     │◄───────┘   │
     │  │    - Historia/conversación      │            │
     │  │    - Guía de estudio            │            │
     │  │                                 │            │
     │  │  • Reproducir Audio             │            │
     │  │    - Play/Pause/Stop            │            │
     │  │    - Listar archivos            │            │
     │  └────────────────────────────────┘            │
     │                                                 │
     │                                                 │
     └─────────────────────────────────────────────────┘

                           │
                           │ <<extends>>
                           │
                           ▼
            ┌──────────────────────────┐
            │    Google Gemini API     │
            │    (Actor Externo)       │
            └──────────────────────────┘
```

---

## 10. Mapa Mental de Funcionalidades

```
                        STUDYBOX
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
  ┌─────────┐         ┌─────────┐         ┌─────────┐
  │  SUBIR  │         │PROCESAR │         │  USAR   │
  │ARCHIVOS │         │CONTENIDO│         │HERRAMI. │
  └────┬────┘         └────┬────┘         └────┬────┘
       │                   │                    │
       │                   │                    │
   ┌───┴───┐           ┌───┴───┐          ┌────┴────┐
   │       │           │       │          │         │
   ▼       ▼           ▼       ▼          ▼         ▼
 TXT     PDF        Extraer  Limpiar  Flashcards  Quiz
 DOCX    Audio      Texto    con IA   
 MD      Código                         Chatbot   Audio
                                        
                                        Conceptos
```

---

**FIN DE DIAGRAMAS VISUALES**

Para más información, consulta `MODELO_DEL_MUNDO.md`

