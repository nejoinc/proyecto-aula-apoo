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
- 📂 Soporte para TXT, MD, PY, JSON, CSV y audio (MP3/WAV)
- 📝 Extracción y limpieza de texto
- 🤖 Chat para preguntas sobre tu propio contenido
- 🎵 Generación de scripts y audio local
- 🃏 Flashcards automáticas
- 🎯 Conceptos clave

---

## Tecnologías
- Frontend: Next.js + TypeScript (web)
- Backend: FastAPI (opcional para web)
- CLI: Python 3.13+
- IA: Google Gemini (opcional)
- TTS: pyttsx3 (local) y ElevenLabs (opcional)

---

## Instalación rápida
Requisitos:
- Python 3.13+
- Node.js 18+ (solo si usarás el frontend)

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

Opción 1: CLI
```bash
py main.py
python3 main.py
```

Opción 2: Web (Frontend + Backend)
```bash
cd backend
python run_server.py

cd studybox-frontend
npm run dev
```

**Acceso:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Documentación API: http://localhost:8000/docs

---

## Arquitectura (resumen)
- Ingesta → extrae texto
- Procesado → limpieza y mejoras
- Salidas → resúmenes, flashcards, quiz, audio
- Web → interfaz Next.js (opcional)

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
- [x] Interfaz web
- [ ] Exportación (PDF, CSV, Anki)
- [ ] Modo colaborativo
- [ ] App móvil
- [ ] Chat en tiempo real
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
