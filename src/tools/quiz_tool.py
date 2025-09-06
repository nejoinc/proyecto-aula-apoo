class QuizTool:
    @staticmethod
    def generate_quiz(text, num_questions=3):
        """
        Genera un examen simulado.
        Más adelante: IA para crear preguntas con contexto real.
        """
        quiz = []
        for i in range(1, num_questions + 1):
            quiz.append({
                "Q": f"Pregunta {i} basada en el texto: {text[:30]}...",
                "Options": ["A", "B", "C", "D"],
                "Answer": "A"
            })
        return quiz
