#!/bin/bash

echo "========================================"
echo "   StudyBox - Instalación de Dependencias"
echo "========================================"
echo

echo "[1/3] Instalando dependencias principales..."
python3 -m pip install -r requirements.txt

echo
echo "[2/3] Verificando instalación..."
python3 -c "import google.generativeai; print('✅ Google Generative AI: OK')"
python3 -c "import pyttsx3; print('✅ pyttsx3 (TTS): OK')"
python3 -c "import requests; print('✅ requests: OK')"
python3 -c "from dotenv import load_dotenv; print('✅ python-dotenv: OK')"

echo
echo "[3/3] Configuración final..."
echo
echo "📝 IMPORTANTE: Configura tu archivo .env con:"
echo "   GEMINI_API_KEY=tu_api_key_aqui"
echo "   ELEVENLABS_API_KEY=tu_api_key_aqui (opcional)"
echo
echo "🚀 ¡StudyBox listo para usar!"
echo "   Ejecuta: python3 main.py"
echo
