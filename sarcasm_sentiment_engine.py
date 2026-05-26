import re
import sys
import spacy
from nltk.sentiment.vader import SentimentIntensityAnalyzer

class LexicalSentimentEngine:
    def __init__(self):
        # Initialize Core NLP Pipelines
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("\n[Error] spaCy 'en_core_web_sm' model not found. Run: python -m spacy download en_core_web_sm")
            sys.exit(1)
            
        import nltk
        try:
            self.sia = SentimentIntensityAnalyzer()
        except LookupError:
            nltk.download('vader_lexicon', quiet=True)
            self.sia = SentimentIntensityAnalyzer()
        
        # 1. Broad Tracking Infrastructure
        self.tracking_pronouns = {"he", "him", "his", "she", "her", "hers", "it", "its", "they", "them", "their", "theirs"}
        self.institutional_synonyms = {
            "administration", "leadership", "government", "party", "chamber", 
            "assembly", "municipal", "headquarters", "executive", "department"
        }
        
        # 2. Sarcasm Anchor Cues (Immediate Toggles)
        self.sarcasm_cues = {"oh great", "brilliant victory", "flawless masterclass", "perfectly timed", "so well!!"}

        # 3. Domain-Specific Political Lexicon Adjustments
        political_lexicon = {
            'filibuster': -1.5,
            'bypass': 1.5,
            'stagnation': -2.0,
            'deficit': -1.5,
            'oblivious': -2.0,
            'backlash': -2.0,
            'reconcile': 2.0,
            'diplomatic': 2.5,
            'ruin': -3.0,
            'crisis': -2.5,
            'breakthrough': 3.5,     
            'milestone': 2.0,
            'scandal': -2.5,
            'corruption': -3.0,
            'debacle': -2.5,
            'paralyzed': -2.0
        }
        self.sia.lexicon.update(political_lexicon)

    def analyze_conditional_sarcasm(self, text, base_score):
        """Detects and structurally flips conditional sarcasm."""
        low_text = text.lower()
        sarcasm_condition = re.search(r"\bif\b.*\b(ruin|collapse|disaster|failure|stagnation|crisis|destruction)\b", low_text)
        
        if sarcasm_condition and base_score > 0:
            return True, -abs(base_score) * 1.5
        return False, base_score

    def get_evidence(self, text, entity_name):
        """Extracts text evidence using contextual look-back and token-cleansed look-ahead."""
        doc = self.nlp(text)
        evidence = []
        entity_found = False
        memory_limit = 2
        counter = 0

        entity_exists_in_text = entity_name.lower() in text.lower()

        for sent in doc.sents:
            sent_text = sent.text.strip()
            low_sent = sent_text.lower()
            
            # Condition A: Directly mentions target
            if entity_name.lower() in low_sent:
                evidence.append(sent_text)
                entity_found = True
                counter = memory_limit  
                
            # Condition B: Look-back institutional context setup
            elif entity_exists_in_text and not entity_found and any(syn in low_sent for syn in self.institutional_synonyms):
                evidence.append(sent_text)
                
            # Condition C: Look-ahead smart pronoun tracking window
            elif entity_found and counter > 0:
                leading_chunk = low_sent[:65]
                words_in_chunk = set(leading_chunk.replace(',', ' ').replace('.', ' ').split())
                
                has_valid_pronoun_subject = any(p in words_in_chunk for p in self.tracking_pronouns)
                has_sarcasm_cue = any(cue in low_sent for cue in self.sarcasm_cues)
                
                # Check for structural sarcasm layout (all-caps markers + exclamation density)
                has_structural_sarcasm = "!!" in low_sent and any(word.isupper() and len(word) > 1 for word in sent_text.split())
                
                if has_valid_pronoun_subject or has_sarcasm_cue or has_structural_sarcasm:
                    evidence.append(sent_text)
                    counter = memory_limit  
                else:
                    counter = 0  
                    
        return evidence

    def process_article(self, text, entity_name):
        """Generates the comprehensive political sentiment report metrics."""
        sentences = self.get_evidence(text, entity_name)
        
        if not sentences:
            print(f"\nNo relevant narrative tracking evidence found for: {entity_name}")
            return

        report_data = []
        total_score = 0.0

        # Pass 1: Gather global backdrop to identify if article contains heavy negative tracking
        text_low = text.lower()
        has_negative_backdrop = any(w in text_low for w in ["scandal", "corruption", "debacle", "disaster", "crisis", "tension"])

        for sent in sentences:
            base_score = self.sia.polarity_scores(sent)['compound']
            low_sent = sent.lower()
            
            # Identify explicit sarcasm cues or structural markers
            is_sarcastic_cue = any(cue in low_sent for cue in self.sarcasm_cues)
            is_structural_sarcastic = "!!" in low_sent and any(word.isupper() and len(word) > 1 for word in sent.split())
            
            is_sarcastic = (is_sarcastic_cue or is_structural_sarcastic) and has_negative_backdrop
            
            if is_sarcastic and base_score > 0:
                base_score = -abs(base_score)
                if base_score > -0.5:
                    base_score = -0.70  # Standard irony floor penalty
                
            # Cross-reference with the advanced conditional structural sarcasm flipper
            conditional_triggered, final_score = self.analyze_conditional_sarcasm(sent, base_score)
            if conditional_triggered:
                is_sarcastic = True
                
            total_score += final_score
            
            if final_score >= 0.05:
                label = "POSITIVE"
            elif final_score <= -0.05:
                label = "NEGATIVE"
            else:
                label = "NEUTRAL"
                
            report_data.append({
                "text": sent,
                "sarcasm": "Yes" if is_sarcastic else "No",
                "label": label,
                "score": round(final_score, 4)
            })

        overall_average = round(total_score / len(sentences), 4)
        if overall_average >= 0.05:
            overall_stance = f"POSITIVE ({overall_average})"
        elif overall_average <= -0.05:
            overall_stance = f"NEGATIVE ({overall_average})"
        else:
            overall_stance = f"NEUTRAL ({overall_average})"

        print("\n" + "=" * 95)
        print(f"POLITICAL SENTIMENT REPORT: {entity_name.upper()}")
        print(f"OVERALL STANCE            : {overall_stance}")
        print("=" * 95)
        print(f"{'Sentence Evidence':<65} | {'Sarcasm?':<8} | {'Sentiment':<10} | Score")
        print("-" * 95)
        for row in report_data:
            truncated_text = row['text'] if len(row['text']) < 63 else f"{row['text'][:62]}.."
            print(f"{truncated_text:<65} | {row['sarcasm']:<8} | {row['label']:<10} | {row['score']}")
        print("=" * 95 + "\n")

if __name__ == "__main__":
    engine = LexicalSentimentEngine()
    print("--- Lexical Sentiment Engine Initialized ---")
    print("(Press 0 to exit at any time)")
    
    while True:
        try:
            print("\nEnter News Paragraph/Article Snippet:")
            user_text = input("> ").strip()
            if user_text == "0":
                print("\n\nExiting Sentiment Engine!")
                break
            if not user_text: continue
                
            print("\nEnter Political Entity (Person/Party/Country):")
            user_entity = input("> ").strip()
            if not user_entity: continue
                
            engine.process_article(user_text, user_entity)
        except (KeyboardInterrupt, EOFError):
            print("\n\nExiting Sentiment Engine!")
            break