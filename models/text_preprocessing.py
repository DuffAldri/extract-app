import re
import numpy as np
import inflect
import nltk
from nltk.corpus import stopwords
import torch
from torch.utils.data import Dataset
from transformers import BertTokenizer
import contractions

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def preprocess_text(text, type="default"):

    if type == "bert":
        # Enter/New Line Normalization
        text = text.replace('\n', ' ').replace('\r', ' ')
        # Fungsi untuk menghapus karakter backslash (\)
        re.sub(r'\\', '', text)
        # Lowercase Normalization
        text = text.lower()
        # Expand Contractions before removing it
        text = contractions.fix(text)
        # Link or URL Normalization
        text = re.sub(r'http\S+|www\S+', '', text)
        # Repeated Character Normalization
        text = re.sub(r'(.)\1+', r'\1\1', text)
        # Remove non-alphanumeric characters (except spaces)
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        return text

    else:
        text = text.lower()
        # text = re.sub(r'\d+', '', text)
        text = re.sub(r'\d+', lambda match: inflect.engine().number_to_words(match.group()), text)
        text = re.sub(r'\.{2,}', ' ', text)
        text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s]', '', text)
        tokens = text.split()
        tokens = [word for word in tokens if word not in stop_words]
        return ' '.join(tokens)

def get_embeddings(texts, model):
    if model:
        return np.array([model.get_sentence_vector(text) for text in texts])
    else:
        print("FastText model is not defined.")
        return None

def preprocess_for_bert(texts, tokenizer, max_length=512):
    inputs = tokenizer(texts, return_tensors='pt', padding=True, truncation=True, max_length=max_length)
    return inputs

class TextClassifierDataset(Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        item = {key: (val[idx]).clone().detach() for key, val in self.encodings.items()}
        item["labels"] = torch.tensor(self.labels[idx])
        return item
