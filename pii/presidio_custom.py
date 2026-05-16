from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern
from presidio_anonymizer import AnonymizerEngine

class EnhancedPresidio:
    def __init__(self):
        self.analyzer = AnalyzerEngine()
        self.anonymizer = AnonymizerEngine()
        self._add_custom_recognizers()

    def _add_custom_recognizers(self):
        # 1. Custom Recognizer: Pakistan CNIC
        cnic_pattern = Pattern(name="cnic", regex=r"\d{5}-\d{7}-\d", score=0.85)
        cnic_recognizer = PatternRecognizer(
            supported_entity="CNIC", 
            patterns=[cnic_pattern],
            context=["cnic", "identity card", "national id"]
        )

        # 2. Custom Recognizer: Student ID (FA21-BCS-123)
        sid_pattern = Pattern(name="student_id", regex=r"[A-Z]{2}\d{2}-[A-Z]{3}-\d{3}", score=0.9)
        sid_recognizer = PatternRecognizer(
            supported_entity="STUDENT_ID",
            patterns=[sid_pattern],
            context=["id", "registration", "student", "roll"]
        )

        # 3. Custom Recognizer: API Key
        key_pattern = Pattern(name="api_key", regex=r"sk-[a-zA-Z0-9]{32,}", score=0.95)
        key_recognizer = PatternRecognizer(
            supported_entity="API_KEY",
            patterns=[key_pattern],
            context=["key", "token", "auth", "secret"]
        )

        self.analyzer.registry.add_recognizer(cnic_recognizer)
        self.analyzer.registry.add_recognizer(sid_recognizer)
        self.analyzer.registry.add_recognizer(key_recognizer)

    def analyze(self, text):
        # Context-aware: Presidio automatically boosts scores if context words match
        results = self.analyzer.analyze(
            text=text, 
            language="en", 
            entities=["PERSON", "EMAIL_ADDRESS", "PHONE_NUMBER", "CNIC", "STUDENT_ID", "API_KEY"]
        )
        return results

    def anonymize(self, text, results):
        return self.anonymizer.anonymize(text=text, analyzer_results=results).text