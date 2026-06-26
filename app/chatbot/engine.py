from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import math
from app.chatbot.knowledge import loading_intents

class Chatbot:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()

        load_knowledgebase(self)

        self.stop_words = set(stopwords.words("english"))
        self.weak_words = {
            "what", "how", "why", "is", "are", "do", "does", "can", "tell", "me", "about"
        }
        self.noise_words = self.stop_words - self.weak_words
        self.threshold = 0.75

        cache_pattern(self)

    def preprocess(self, text):
        lower_text = text.lower()
        tokens = word_tokenize(lower_text)

        tagged = pos_tag(tokens)

        weights = {}
        for word, tag in tagged:
            if not word.isalnum():
                continue

            lemma = self.lemmatizer.lemmatize(word, self.get_wordnet_pos(tag))
            w = self.get_word_weight(lemma, tag)

            weights[lemma] = max(weights.get(lemma, 0), w)
        
        expanded = {}
        for word, base_weight in weights.items():
            syns = self.expand_word(word)

            for syn, syn_weight in syns.items():
                expanded[syn] = max(expanded.get(syn, 0), base_weight * syn_weight)

        return expanded
    
    def expand_word(self, word):
        words = {word: 1.0}  # keep original strongest

        if word in self.stop_words:
            return words

        for syn in wordnet.synsets(word)[:2]:
            for lemma in syn.lemmas():
                syn_word = lemma.name().lower().replace("_", " ")

                # lower weight for synonyms
                words[syn_word] = 0.6

        return words
    
    def get_wordnet_pos(self, treebank_tag):
        if treebank_tag.startswith('J'):
            return wordnet.ADJ
        elif treebank_tag.startswith('V'):
            return wordnet.VERB
        elif treebank_tag.startswith('N'):
            return wordnet.NOUN
        elif treebank_tag.startswith('R'):
            return wordnet.ADV
        else:
            return wordnet.NOUN  # default
        
    def get_word_weight(self, word, tag):
        
        if word in self.stop_words:
            if word in self.weak_words:
                return 0.3   # structural signal
            else:
                return 0.05  # near-noise
        
        # POS weight
        if tag.startswith('N'):
            pos_w = 1.0
        elif tag.startswith('V'):
            pos_w = 0.9
        elif tag.startswith('J'):
            pos_w = 0.8
        elif tag.startswith('R'):
            pos_w = 0.7
        else:
            pos_w = 0.5

        return pos_w

    def confidence(self, user_tokens, pattern):
        pattern_tokens = self.pattern_cache[pattern]

        if not user_tokens or not pattern_tokens:
            return 0
        
        # dot product
        dot = 0
        for w in user_tokens:
            if w in pattern_tokens:
                dot += user_tokens[w] * pattern_tokens[w]

        # L2 norms
        user_norm = math.sqrt(sum(v*v for v in user_tokens.values()))
        pattern_norm = math.sqrt(sum(v*v for v in pattern_tokens.values()))

        if user_norm == 0 or pattern_norm == 0:
            return 0

        return dot / (user_norm * pattern_norm)
    
    def is_frame_only(self, text):
        tokens = word_tokenize(text.lower())
        tagged = pos_tag(tokens)

        if not tokens:
            return True

        content_words = 0
        pos_types = set()

        for w, t in tagged:
            if not w.isalnum():
                continue

            pos_types.add(t[0])

            if w not in self.stop_words and t.startswith(("NN", "VB", "JJ", "RB")):
                content_words += 1

        content_ratio = content_words / len(tokens)
        pos_diversity = len(pos_types)

        return content_ratio < 0.25 and pos_diversity <= 2
    
    def respond(self, user_input):
        best_score = 0
        best_response = None

        if not self.is_frame_only(user_input):
            user_tokens = self.preprocess(user_input)

            for pattern, response in self.intents.items():
                score = self.confidence(user_tokens, pattern)
                if score > best_score:
                    best_score = score
                    best_response = response

            if best_score > self.threshold:
                return best_response, best_score

        return "Sorry, I can only answer questions related to Artificial Intelligence.", best_score
    
def load_knowledgebase(self):
    self.intents = loading_intents()

def cache_pattern(self):
    self.pattern_cache = {
        pattern: self.preprocess(pattern)
        for pattern in self.intents
    }