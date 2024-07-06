import joblib
import fasttext
import torch
from transformers import BertTokenizer, BertForSequenceClassification, AutoModelForSequenceClassification

try:
    ensemble_model = joblib.load('models/load_models/ensemble_model.pkl')
    print("Ensemble model loaded successfully.")
except Exception as e:
    print(f"Error loading Ensemble model: {e}")
    ensemble_model = None

# Load FastText model
try:
    fasttext_model = fasttext.load_model('models/load_models/cc.en.300.bin')
    print("FastText model loaded successfully.")
except Exception as e:
    print(f"Error loading FastText model: {e}")
    fasttext_model = None

# Load MultiLabelBinarizer
try:
    mlb = joblib.load('models/load_models/mlb.pkl')
    print("MultiLabelBinarizer loaded successfully.")
except Exception as e:
    print(f"Error loading MultiLabelBinarizer: {e}")
    mlb = None

# Load BERT model and tokenizer
try:
    bert_model = AutoModelForSequenceClassification.from_pretrained(
        'distilbert-base-uncased',
        num_labels=4  # Ensure this matches the number of output labels the model was trained on
    )
    bert_model.load_state_dict(torch.load('models/load_models/bert_best_model.pth', map_location=torch.device('cpu')))
    tokenizer = BertTokenizer.from_pretrained('distilbert-base-uncased')
    bert_model.eval()  # Set the model to evaluation mode
    print("BERT model and tokenizer loaded successfully.")
except Exception as e:
    print(f"Error loading BERT model or tokenizer: {e}")
    bert_model, tokenizer = None, None
