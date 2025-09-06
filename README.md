# 📚 StudyBox  
*A complete system for studying — by students, for students.*

---

## ✨ Overview  
StudyBox is an **interactive study application** designed to help students learn more effectively using only the materials they upload.  
Instead of relying on external sources, the app transforms **text, audio, and other formats** into customized learning tools:  
- Summaries  
- Diagrams  
- Flashcards  
- Quizzes & Exams  

Our goal is simple: make studying **personalized, verifiable, and collaborative**.

---

## 🚀 Features (MVP)  
- 📂 Upload multiple file types (PDF, DOCX, TXT, JSON, CSV, audio).  
- 📝 Automatic text extraction & transcription with AI.  
- 🤖 Interactive chatbot for Q&A about your content.  
- 🎵 Audio generation for different study formats.  
- 📑 Summaries at different levels of detail.  
- 🃏 Flashcards and question generators (with traceability to source text).  
- 🎯 Key concepts extraction.  
- 🔒 Privacy first: your files stay private by default.  

---

## 🛠️ Tech Stack  
- **Backend:** Python 3.13+  
- **AI Integration:** Google Gemini API  
- **Text-to-Speech:** pyttsx3 (local), ElevenLabs (premium)  
- **File Processing:** Custom processors for multiple formats  
- **Storage:** Local file system with organized structure  

---

## 📦 Installation & Setup

### Prerequisites
- Python 3.13+ installed
- Google Gemini API key (optional but recommended)

### Quick Start

#### Windows:
```bash
# Clone the repository
git clone <repository-url>
cd proyecto-aula-apoo

# Install dependencies automatically
install_requirements.bat

# Or install manually
py -m pip install -r requirements.txt
```

#### Linux/Mac:
```bash
# Clone the repository
git clone <repository-url>
cd proyecto-aula-apoo

# Install dependencies automatically
chmod +x install_requirements.sh
./install_requirements.sh

# Or install manually
python3 -m pip install -r requirements.txt
```

### Configuration
1. Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=tu_api_key_aqui
ELEVENLABS_API_KEY=tu_api_key_aqui  # Optional for premium audio
```

2. Get your Gemini API key:
   - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Add it to your `.env` file

### Running StudyBox
```bash
# Windows
py main.py

# Linux/Mac
python3 main.py
```

---

## 🧩 Architecture (High Level)  
- **Ingestor** → Extracts text from files (OCR/ASR).  
- **Processors** → Generate summaries, flashcards, quizzes.  
- **Outputs** → Stored with source traceability.  
- **Frontend** → Intuitive dashboard for managing study projects.  

---

## 👥 Team  
This project is developed by three students:  
- **José Manuel Jaramillo**  
- **Samuel Romaña**  
- **Nicolás Peña**  

---

## 📌 Roadmap  
- [x] File upload & text extraction  
- [x] AI-powered content processing  
- [x] Interactive chatbot for Q&A  
- [x] Audio generation (multiple formats)  
- [x] Key concepts extraction  
- [x] Summaries (short / medium / detailed)  
- [x] Flashcard generator (enhanced)  
- [x] Quiz/exam generator (enhanced)  
- [ ] Export options (PDF, CSV, Anki)  
- [ ] Collaborative study mode  
- [ ] Web interface  
- [ ] Mobile app  

---

## 🤝 Contributing  
We welcome contributions!  
1. Fork the repository  
2. Create your feature branch (`git checkout -b feature/new-feature`)  
3. Commit your changes (`git commit -m 'Add new feature'`)  
4. Push to the branch (`git push origin feature/new-feature`)  
5. Open a Pull Request  

---

## 📜 License  
This project is licensed under the **MIT License**.  
See [LICENSE](./LICENSE) for details.  

---
