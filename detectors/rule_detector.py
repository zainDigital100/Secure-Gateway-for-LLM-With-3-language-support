from utils.language_utils import get_multilingual_keywords, detect_language

class RuleDetector:
    def __init__(self):
        self.keyword_map = get_multilingual_keywords()

    def detect(self, text):
        lang = detect_language(text)
        text_lower = text.lower()
        score = 0.0

        keywords = self.keyword_map.get(lang, self.keyword_map['en'])
        matches = [kw for kw in keywords if kw in text_lower]
        
        if matches:
            # Score grows with number of keywords found
            score = min(len(matches) * 0.25, 1.0)
            
        return score, lang