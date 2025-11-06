class SummaryTool:
    @staticmethod
    def generate_summary(text, level="medium"):
        return f"[Resumen-{level}] {text[:60]}..."
