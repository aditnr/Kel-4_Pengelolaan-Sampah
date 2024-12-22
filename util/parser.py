import json
import pandas as pd
from random import choice
import difflib
class JSONParser:
    def __init__(self):
        self.text = []
        self.intents = []
        self.responses = {}
    def parse(self, json_path):
        with open(json_path) as data_file:
            self.data = json.load(data_file)
        if 'intents' not in self.data:
            raise KeyError("Key 'intents' not found in JSON data!")
        for intent in self.data['intents']:
            if 'tag' not in intent or 'patterns' not in intent or 'responses' not in intent:
                raise KeyError(f"Missing required keys in intent: {intent}")
            for pattern in intent['patterns']:
                self.text.append(pattern)
                self.intents.append(intent['tag'])
            for resp in intent['responses']:
                if intent['tag'] in self.responses:
                    if resp not in self.responses[intent['tag']]:
                        self.responses[intent['tag']].append(resp)
                else:
                    self.responses[intent['tag']] = [resp]
        self.df = pd.DataFrame({'text_input': self.text, 'intents': self.intents})
        print(f"[INFO] Data JSON converted to DataFrame with shape: {self.df.shape}")
    def get_dataframe(self):
        return self.df
    def get_response(self, user_input):
        highest_ratio = 0
        best_match_tag = None
        best_response = "Maaf, saya tidak mengerti intent ini."
        for intent in self.data['intents']:
            for pattern in intent['patterns']:
                ratio = difflib.SequenceMatcher(None, user_input.lower(), pattern.lower()).ratio()
                if ratio > highest_ratio:
                    highest_ratio = ratio
                    best_match_tag = intent['tag']
                    best_response = choice(intent['responses'])
        return best_response