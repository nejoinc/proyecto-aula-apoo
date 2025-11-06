# 🚀 StudyBox - Inicio Rápido

## ¿Qué es StudyBox?

StudyBox es una aplicación inteligente de estudio que te ayuda a procesar tus materiales de aprendizaje y convertirlos en herramientas de estudio interactivas usando IA.

---

## 📦 Instalación

### 1. Instalar Dependencias

```bash
# Windows
pip install -r requirements.txt

# Linux/Mac
pip3 install -r requirements.txt
```

### 2. (Opcional) Configurar IA

Para funcionalidad completa, crea un archivo `.env` en la raíz:

```env
GEMINI_API_KEY=tu_api_key_aqui
```

Obtén tu API key gratis en: https://makersuite.google.com/app/apikey

**Nota**: La aplicación funciona sin API key, pero con funcionalidad limitada (modo simulado).

---

## 🎯 2 Formas de Usar StudyBox

### 💻 Opción 1: Interfaz Gráfica (GUI Desktop) ⭐ RECOMENDADO

**Ventajas**:
- ✅ Aplicación nativa de escritorio
- ✅ No requiere navegador
- ✅ Interfaz moderna con Tkinter
- ✅ Chatbot en ventana dedicada

**Cómo ejecutar**:

```bash
# Windows
python main_gui.py

# Linux/Mac
python3 main_gui.py
```

**Guía completa**: Ver `GUIA_GUI.md`

---

### ⌨️ Opción 2: Línea de Comandos (CLI)

**Ventajas**:
- ✅ Rápido y eficiente
- ✅ Perfecto para usuarios avanzados
- ✅ Bajo consumo de recursos

**Cómo ejecutar**:

```bash
# Windows
python main.py

# Linux/Mac
python3 main.py
```

---

## 📚 Funcionalidades Principales

### 1. 📤 Subir Archivos
Sube tus materiales de estudio:
- Documentos: TXT, PDF, DOCX, MD
- Código: PY, JS, JAVA, CPP, JSON, CSV
- Audio: MP3, WAV

### 2. ⚙️ Procesar con IA
El contenido se limpia, estructura y mejora automáticamente con IA.

### 3. 🤖 Chatbot Inteligente
Pregúntale al chatbot sobre tu contenido:
- Explicaciones de conceptos
- Resúmenes
- Ejemplos prácticos
- Preguntas específicas

**Comandos especiales**:
- `resumen` - Genera resumen
- `conceptos` - Extrae conceptos
- `ejemplos` - Genera ejemplos

### 4. 🃏 Flashcards Automáticas
Genera tarjetas de estudio:
- **Automáticas**: Contenido general
- **Conceptos**: Enfocadas en conceptos clave
- **Definiciones**: Términos importantes

### 5. 🎯 Quiz Interactivo
Genera quizzes para evaluar tu conocimiento:
- Preguntas de opción múltiple
- Verdadero/Falso
- Preguntas abiertas

### 6. 💡 Conceptos Clave
Extrae automáticamente los conceptos más importantes de tu material.

### 7. 🎵 Generación de Audio
Convierte texto a audio para estudiar mientras haces otras cosas.

---

## 📊 Comparativa de Interfaces

| Característica | GUI 💻 | CLI ⌨️ |
|----------------|--------|--------|
| **Acceso** | App nativa | Terminal |
| **Instalación** | Python + Tkinter | Python |
| **Interfaz** | Moderna | Texto |
| **Rendimiento** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Facilidad de uso** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |

---

## 🎓 Flujo de Trabajo Típico

1. **Subir archivos** → Sube tus materiales de estudio
2. **Procesar** → Deja que la IA procese y mejore el contenido
3. **Estudiar** → Usa las herramientas:
   - Chatea con el bot para resolver dudas
   - Genera flashcards para repasar
   - Haz quizzes para autoevaluarte
   - Revisa conceptos clave
   - Escucha el contenido en audio

---

## 🔧 Solución de Problemas Comunes

### Python no se encuentra (Windows)

**Error**: `'python' no se reconoce como comando`

**Solución**:
1. Instala Python desde python.org
2. Durante instalación, marca "Add Python to PATH"
3. O usa `py` en lugar de `python`:
   ```bash
   py main_gui.py
   py run_web.py
   ```

### ModuleNotFoundError

**Error**: `No module named 'fastapi'` o similar

**Solución**:
```bash
pip install -r requirements.txt
```

### El chatbot no responde bien

**Causa**: API key de Gemini no configurada

**Solución**:
1. Crea archivo `.env` con tu API key
2. O usa en modo simulado (respuestas básicas)

---

## 📖 Documentación Adicional

- **Guía GUI**: `GUIA_GUI.md` - Guía completa de la interfaz gráfica
- **README**: `README.md` - Documentación técnica completa

---

## 💡 Consejos

1. **Procesa archivos primero**: Antes de usar herramientas de estudio, asegúrate de haber procesado tus archivos.

2. **Configura la API de Gemini**: Para mejor experiencia, configura tu API key (es gratis).

3. **Guarda tus flashcards**: Se guardan automáticamente en `src/storage/flashcards/`

4. **Prueba diferentes tipos de flashcards**: Cada tipo se enfoca en aspectos diferentes del contenido.

---

## 🎯 Próximos Pasos

1. ✅ Elige tu interfaz preferida (Web, GUI o CLI)
2. ✅ Sube algunos archivos de estudio
3. ✅ Procesa los archivos
4. ✅ Comienza a usar las herramientas

---

## 📞 Ayuda

Si necesitas ayuda:

1. Revisa la guía específica (`GUIA_GUI.md`)
2. Consulta el `README.md`
3. Abre un issue en el repositorio

---

## 👥 Créditos

Desarrollado por:
- José Manuel Jaramillo
- Samuel Romaña
- Nicolás Peña

---

**¡Feliz estudio! 📚✨**

Comienza ahora con:
```bash
# GUI Desktop (recomendado)
python main_gui.py

# CLI
python main.py
```


