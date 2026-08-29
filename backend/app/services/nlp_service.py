import spacy
import re
from typing import List, Dict


class NLPService:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')

    def extract_entities(self, text: str) -> List[Dict]:
        doc = self.nlp(text)
        entities = []
        seen = set()

        for ent in doc.ents:
            if ent.text not in seen:
                seen.add(ent.text)
                entities.append({
                    'name': ent.text,
                    'entity_type': ent.label_,
                    'confidence': 0.85
                })

        return entities

    def extract_claims(self, text: str) -> List[Dict]:
        sentences = re.split(r'(?<=[.!?])\s+', text)
        claims = []

        claim_indicators = [
            'is', 'are', 'was', 'were', 'has', 'have', 'had',
            'according to', 'research shows', 'study found',
            'data indicates', 'evidence suggests', 'report states'
        ]

        for sent in sentences:
            sent = sent.strip()
            if len(sent) < 20:
                continue

            sent_lower = sent.lower()
            if any(indicator in sent_lower for indicator in claim_indicators):
                claims.append({
                    'claim_text': sent,
                    'claim_type': 'factual',
                    'confidence': 0.7
                })

        return claims

    def extract_statistics(self, text: str) -> List[Dict]:
        stats = []

        number_patterns = [
            (r'\d+\.?\d*\s*%', 'percentage'),
            (r'\$\s*\d+\.?\d*', 'monetary'),
            (r'\d{1,3}(?:,\d{3})*(?:\.\d+)?', 'number'),
        ]

        for pattern, stat_type in number_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                stats.append({
                    'value': match.group(),
                    'type': stat_type,
                    'position': match.start()
                })

        return stats

    def process_chunk(self, text: str) -> Dict:
        entities = self.extract_entities(text)
        claims = self.extract_claims(text)
        statistics = self.extract_statistics(text)

        return {
            'entities': entities,
            'claims': claims,
            'statistics': statistics,
            'word_count': len(text.split()),
            'sentence_count': len(re.split(r'[.!?]+', text))
        }
