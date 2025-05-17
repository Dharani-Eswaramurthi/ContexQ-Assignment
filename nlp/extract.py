import spacy
from spacy.matcher import Matcher
from transformers import pipeline
import logging

class NLPProcessor:
    def __init__(self, spacy_model_name="en_core_web_trf", sentiment_model_name="distilbert-base-uncased-finetuned-sst-2-english"):
        try:
            self.nlp = spacy.load(spacy_model_name)
            logging.info(f"Loaded spaCy model: {spacy_model_name}")
        except Exception as e:
            logging.warning(f"Failed to load {spacy_model_name}: {e}. Falling back to en_core_web_sm.")
            self.nlp = spacy.load("en_core_web_sm")

        self.matcher = Matcher(self.nlp.vocab)
        # More robust pattern for acquisition events (optional: can be extended)
        pattern = [
            {"ENT_TYPE": "ORG"},
            {"LEMMA": {"IN": ["acquire", "acquires", "acquired", "buy", "bought", "purchase", "purchased"]}},
            {"ENT_TYPE": "ORG"}
        ]
        self.matcher.add("ACQUISITION", [pattern])

        try:
            self.sentiment = pipeline("sentiment-analysis", model=sentiment_model_name)
            logging.info(f"Loaded sentiment model: {sentiment_model_name}")
        except Exception as e:
            logging.warning(f"Failed to load sentiment model {sentiment_model_name}: {e}. Sentiment analysis will be disabled.")
            self.sentiment = None

    def extract_entities_and_events(self, text):
        if not text or not text.strip():
            return [], []

        try:
            doc = self.nlp(text)
            ents = [(ent.text, ent.label_) for ent in doc.ents]
            events = []
            for match_id, start, end in self.matcher(doc):
                span = doc[start:end]
                events.append((span.text, self.nlp.vocab.strings[match_id]))
            return ents, events
        except Exception as e:
            logging.error(f"Error in entity/event extraction: {e}")
            return [], []

    def analyze_sentiment(self, text):
        if not self.sentiment or not text or len(text.strip()) < 5:
            return "NEUTRAL", 0.0
        try:
            # Truncate to model max length safely
            truncated_text = text[:512]
            result = self.sentiment(truncated_text)[0]
            label = result.get("label", "NEUTRAL")
            score = float(result.get("score", 0.0))
            return label, score
        except Exception as e:
            logging.error(f"Error in sentiment analysis: {e}")
            return "NEUTRAL", 0.0
