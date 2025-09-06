@echo off
echo ========================================
echo    StudyBox - Instalacion de Dependencias
echo ========================================
echo.

echo [1/3] Instalando dependencias principales...
py -m pip install -r requirements.txt

echo.
echo [2/3] Verificando instalacion...
py -c "import google.generativeai; print('✅ Google Generative AI: OK')"
py -c "import pyttsx3; print('✅ pyttsx3 (TTS): OK')"
py -c "import requests; print('✅ requests: OK')"
py -c "from dotenv import load_dotenv; print('✅ python-dotenv: OK')"

echo.
echo [3/3] Configuracion final...
echo.
echo 📝 IMPORTANTE: Configura tu archivo .env con:
echo    GEMINI_API_KEY=tu_api_key_aqui
echo    ELEVENLABS_API_KEY=tu_api_key_aqui (opcional)
echo.
echo 🚀 ¡StudyBox listo para usar!
echo    Ejecuta: py main.py
echo.
pause
