class SummaryTool:
    @staticmethod
    def generate_summary(text, level="medium"):
        """
        Genera un resumen simulado según el nivel.
        level puede ser: short, medium, detailed
        """
        return f"[Resumen-{level}] {text[:60]}..."
