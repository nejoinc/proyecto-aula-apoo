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
- 📂 Upload multiple file types (PDF, DOCX, TXT, audio).  
- 📝 Automatic text extraction & transcription.  
- 📑 Summaries at different levels of detail.  
- 🃏 Flashcards and question generators (with traceability to source text).  
- 📤 Export to PDF, CSV, or Anki.  
- 🔒 Privacy first: your files stay private by default.  

---

## 🛠️ Tech Stack  
- **Backend:** Python (FastAPI) / Node.js (NestJS)  
- **Frontend:** React + TypeScript + TailwindCSS  
- **Database:** PostgreSQL  
- **AI Models:** Whisper (audio), Tesseract (OCR), LLMs for processing (OpenAI, local models, etc.)  
- **Deployment:** Docker  

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
- [ ] File upload & text extraction  
- [ ] Summaries (short / medium / detailed)  
- [ ] Flashcard generator  
- [ ] Quiz/exam generator  
- [ ] Export options  
- [ ] Collaborative study mode  

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
