# 📚 Guía de Uso - Interfaz Gráfica StudyBox

## Inicio Rápido

### Ejecutar la Aplicación
```bash
# Windows
py main_gui.py

# Linux/Mac
python3 main_gui.py
```

---

## Interfaz Principal

La interfaz de StudyBox está dividida en tres áreas principales:

### 1️⃣ Panel Lateral (Izquierda)
Aquí encontrarás todos los botones para acceder a las diferentes funcionalidades:

#### 📂 Gestión de Archivos
- **📤 Subir Archivo**: Abre un diálogo para seleccionar archivos de tu computadora
- **⚙️ Procesar Archivos**: Procesa los archivos subidos con IA
- **📋 Listar Archivos**: Muestra todos los archivos almacenados
- **🗑️ Eliminar Archivo**: Elimina archivos del almacenamiento

#### 🎓 Herramientas de Estudio
- **🤖 Chatbot**: Chatea con IA sobre tu contenido
- **🃏 Flashcards**: Genera tarjetas de estudio automáticas
- **🎯 Quiz**: Crea quizzes personalizados
- **🎵 Generar Audio**: Convierte texto a audio
- **🎧 Reproducir Audio**: Reproduce audios generados
- **💡 Conceptos Clave**: Extrae conceptos importantes

### 2️⃣ Área de Contenido (Centro)
Aquí se muestra toda la información y resultados de tus acciones.

### 3️⃣ Barra de Estado (Abajo)
Muestra el estado actual de la aplicación y mensajes informativos.

---

## Flujo de Trabajo Recomendado

### Paso 1: Subir Archivos 📤
1. Haz clic en "📤 Subir Archivo"
2. Selecciona un archivo de tu computadora (TXT, PDF, DOCX, MD, etc.)
3. El archivo se guardará automáticamente

### Paso 2: Procesar Archivos ⚙️
1. Haz clic en "⚙️ Procesar Archivos"
2. Selecciona los archivos que quieres procesar (usa los checkboxes)
3. Haz clic en "⚙️ Procesar Seleccionados"
4. Espera a que se complete el procesamiento

**⚠️ IMPORTANTE**: Debes procesar archivos antes de usar las herramientas de estudio.

### Paso 3: Usar Herramientas de Estudio 🎓

#### 🤖 Chatbot Interactivo
1. Haz clic en "🤖 Chatbot"
2. Se abrirá una ventana de chat
3. Escribe tus preguntas en el campo de texto
4. Presiona Enter o haz clic en "Enviar"

**Comandos especiales**:
- `resumen` - Genera un resumen del contenido
- `conceptos` - Extrae conceptos clave
- `ejemplos` - Genera ejemplos prácticos

#### 🃏 Flashcards
1. Haz clic en "🃏 Flashcards"
2. Selecciona el tipo de flashcards:
   - **Automáticas**: Genera flashcards generales
   - **Conceptos**: Enfocadas en conceptos clave
   - **Definiciones**: Enfocadas en definiciones
3. Espera a que se generen
4. Revisa las flashcards en pantalla

#### 💡 Conceptos Clave
1. Haz clic en "💡 Conceptos Clave"
2. La aplicación extraerá automáticamente los conceptos principales
3. Revisa la lista de conceptos únicos encontrados

#### 🎵 Generador de Audio
1. Haz clic en "🎵 Generar Audio"
2. Selecciona el tipo de audio que deseas generar:
   - **Resumen narrado**: Resume los conceptos principales
   - **Explicación de conceptos**: Explica conceptos detalladamente
   - **Lectura completa**: Lee todo el contenido
   - **Preguntas y respuestas**: Genera Q&A sobre el tema
   - **Historia o conversación**: Convierte el contenido en narrativa
   - **Guía de estudio**: Crea una guía paso a paso
3. Espera a que se genere el audio (se muestra el progreso)
4. Los archivos se guardan automáticamente y puedes reproducirlos después

#### 🎧 Reproductor de Audio
1. Haz clic en "🎧 Reproducir Audio"
2. Se abrirá una ventana con la lista de archivos de audio disponibles
3. Selecciona un archivo y haz clic en "▶ Reproducir"
4. Usa los controles para pausar/reanudar o detener
5. También puedes hacer doble clic en un archivo para reproducirlo directamente

#### 🎯 Quiz Interactivo
1. Haz clic en "🎯 Quiz"
2. Selecciona el tipo de quiz:
   - **Opción Múltiple**: Preguntas con varias opciones
   - **Verdadero/Falso**: Afirmaciones para verificar
   - **Completar Espacios**: Completa palabras faltantes
   - **Preguntas Abiertas**: Requieren respuestas elaboradas
   - **Quiz Mixto**: Combinación de tipos
3. Selecciona el número de preguntas (3-15)
4. Responde cada pregunta y verifica tu respuesta
5. Al final verás tu puntaje y porcentaje

---

## Tipos de Archivos Soportados

### Documentos de Texto
- `.txt` - Archivos de texto plano
- `.md` - Archivos Markdown
- `.pdf` - Documentos PDF
- `.docx` / `.doc` - Documentos de Word

### Código Fuente
- `.py` - Python
- `.js` - JavaScript
- `.java` - Java
- `.cpp` / `.c` - C/C++
- `.json` - JSON
- `.csv` - CSV

### Audio
- `.mp3` - Audio MP3
- `.wav` - Audio WAV

---

## Características de la Interfaz

### 🎨 Diseño Moderno
- Colores agradables y profesionales
- Botones con efectos hover
- Íconos intuitivos para cada función

### 📱 Responsive
- La ventana se puede redimensionar
- El contenido se ajusta automáticamente
- Scroll automático para contenido largo

### ⚡ Procesamiento en Segundo Plano
- Las operaciones pesadas no bloquean la interfaz
- Puedes seguir usando la aplicación mientras procesa
- Mensajes de estado actualizados en tiempo real

### 🔄 Actualización Automática
- Las listas de archivos se actualizan automáticamente
- Los resultados se muestran inmediatamente
- Notificaciones visuales de éxito o error

### 🎮 Interactividad Completa
- Todas las funcionalidades están integradas en la GUI
- No se requiere usar la consola
- Quiz interactivo con feedback inmediato
- Generador de audio con progreso en tiempo real

---

## Consejos de Uso

### ✅ Buenas Prácticas

1. **Procesa archivos antes de usar herramientas**
   - Las herramientas de estudio requieren contenido procesado
   - Puedes procesar múltiples archivos a la vez

2. **Usa nombres descriptivos para tus archivos**
   - Facilita identificarlos en las listas
   - Ayuda a organizar mejor tu contenido

3. **Aprovecha el chatbot**
   - Haz preguntas específicas
   - Usa los comandos especiales
   - El historial se mantiene durante la sesión

4. **Genera diferentes tipos de flashcards**
   - Cada tipo se enfoca en aspectos diferentes
   - Puedes generar múltiples sets para estudiar mejor

### ⚠️ Limitaciones

1. **API de Gemini requerida para funcionalidad completa**
   - Sin API, funciona en modo simulado
   - Configura tu `.env` con `GEMINI_API_KEY` para funcionalidad completa

2. **Tamaño de archivos**
   - Archivos muy grandes pueden tardar en procesarse
   - PDF con muchas imágenes pueden ser lentos

3. **Generación de contenido con IA**
   - Requiere conexión a internet cuando se usa la API de Gemini
   - La generación de audio y quiz puede tomar unos segundos

---

## Solución de Problemas

### La ventana no se abre
```bash
# Verifica que Tkinter esté instalado
python -m tkinter

# Si no funciona, reinstala Python con soporte Tkinter
```

### Error al subir archivos
- Verifica que el archivo exista
- Comprueba que sea un formato soportado
- Asegúrate de tener permisos de lectura

### Error al procesar
- Verifica tu conexión a internet (si usas IA)
- Comprueba tu API key de Gemini en `.env`
- Revisa que los archivos no estén corruptos

### El chatbot no responde bien
- Asegúrate de tener `GEMINI_API_KEY` configurada
- Verifica tu conexión a internet
- Sin API, funcionará en modo simulado (respuestas básicas)

---

## Atajos de Teclado

### En el Chatbot
- `Enter` - Enviar mensaje
- `Esc` - Cerrar ventana (próximamente)

### General
- Haz clic en cualquier botón del menú lateral para navegar
- Usa el scroll del mouse para desplazarte por contenido largo

---

## Configuración Avanzada

### Configurar API de Gemini

1. Ve a [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Crea una API key
3. Crea un archivo `.env` en la raíz del proyecto:
```env
GEMINI_API_KEY=tu_api_key_aqui
```
4. Reinicia la aplicación

### Cambiar Colores (para desarrolladores)

Edita el diccionario `self.colors` en `src/gui_app.py`:
```python
self.colors = {
    'primary': '#2C3E50',    # Color principal
    'secondary': '#3498DB',  # Color secundario
    'accent': '#E74C3C',     # Color de acento
    # ... más colores
}
```

---

## Recursos Adicionales

- **Documentación completa**: Ver `README.md`
- **Versión CLI**: Ejecuta `python main.py`
- **Reporte de bugs**: Crea un issue en el repositorio

---

## Preguntas Frecuentes (FAQ)

### ¿Necesito internet para usar StudyBox?
No necesariamente. Las funciones básicas (subir, listar, eliminar archivos) funcionan offline. Sin embargo, para las funciones de IA (chatbot, generación de flashcards inteligentes) necesitas internet y una API key de Gemini.

### ¿Puedo usar StudyBox sin API de Gemini?
Sí, la aplicación funcionará en "modo simulado" con respuestas básicas. Para funcionalidad completa, se recomienda configurar la API.

### ¿Los archivos se quedan en mi computadora?
Sí, todos los archivos se almacenan localmente en la carpeta `src/storage/`. No se suben a ningún servidor externo.

### ¿Puedo exportar las flashcards?
Actualmente las flashcards se guardan en formato JSON en `src/storage/flashcards/`. La exportación a otros formatos está en desarrollo.

### ¿La aplicación funciona en Mac/Linux?
Sí, StudyBox es multiplataforma. Funciona en Windows, Mac y Linux.

---

## Contacto y Soporte

Proyecto desarrollado por:
- José Manuel Jaramillo
- Samuel Romaña
- Nicolás Peña

Para reportar problemas o sugerencias, abre un issue en el repositorio del proyecto.

---

**¡Disfruta estudiando con StudyBox! 📚✨**


