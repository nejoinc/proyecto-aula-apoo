class FlashcardTool:
    @staticmethod
    def generate_flashcards(text):
        """
        Genera tarjetas de estudio simuladas.
        Más adelante: NLP para dividir en preguntas/respuestas.
        """
        return [
            {"Q": "¿Qué dice el texto al inicio?", "A": text[:40]},
            {"Q": "¿Qué dice el texto al final?", "A": text[-40:]},
        ]
