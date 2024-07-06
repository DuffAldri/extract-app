import torch
import pandas as pd
import numpy as np
from transformers import AutoModelForSequenceClassification, BertTokenizer

def predict_with_model(X_test, tokenizer, model, device, threshold=0.5):
    if isinstance(X_test, pd.DataFrame):
        X_test = X_test['Review'].tolist()

    model.to(device)
    all_probabilities = []

    for text in X_test:
        inputs = tokenizer(text, padding=True, truncation=True, return_tensors="pt")
        if 'token_type_ids' in inputs:
            del inputs['token_type_ids']  # Remove token_type_ids if using DistilBERT
        inputs = inputs.to(device)

        with torch.no_grad():
            outputs = model(**inputs)

        logits = outputs.logits
        probabilities = torch.sigmoid(logits)
        all_probabilities.append(probabilities.cpu().numpy().flatten())

    all_probabilities_array = np.vstack(all_probabilities)  # Ensure it's a 2D array

    if threshold is None:
        return all_probabilities_array

    return (all_probabilities_array >= threshold).astype(int)
