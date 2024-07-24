import json
from flask import Blueprint, request, redirect, url_for, session, jsonify, render_template, current_app
import pandas as pd
import os
import numpy as np
import torch
import uuid
from datetime import datetime
from models import preprocess_text, get_embeddings, preprocess_for_bert, ensemble_model, fasttext_model, bert_model, tokenizer
from models.bert_prediction import predict_with_model

prediction_bp = Blueprint('prediction', __name__)

def generate_unique_filename(filename):
    ext = filename.split('.')[-1]
    unique_id = uuid.uuid4().hex
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    unique_filename = f"{timestamp}_{unique_id}.{ext}"
    return unique_filename

@prediction_bp.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        if file:
            unique_filename = generate_unique_filename(file.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(filepath)
            session['filepath'] = filepath

        filepath = session.get('filepath', None)
        if filepath:
            try:
                df = pd.read_excel(filepath)
            except Exception as e:
                return jsonify({'error': 'Gagal membaca file excel'}), 400
            
            algorithm = request.form['algorithm']
            
            # df = pd.read_excel(filepath)
            if 'review' not in df.columns:
                return jsonify({'error': "Kolom 'review' gagal ditemukan. Periksa kembali template!"}), 400
            
            if df['review'].dropna().empty:
                return jsonify({'error': "Kolom 'review' kosong. Periksa kembali file yang diupload!"}), 400
            
            try:
                
                texts = df['review'].apply(lambda x: preprocess_text(x, algorithm)).tolist()
            except Exception as e:
                return jsonify({'error': 'Gagal melakukan praproses teks'}), 400

            if algorithm == 'bert':
                if bert_model is None or tokenizer is None:
                    return jsonify({'error': 'Gagal memuat model dan tokenizer BERT'}), 400
                try:
                    predictions = predict_with_model(texts, tokenizer, bert_model, device='cpu', threshold=0.35)
                except Exception as e:
                    return jsonify({'error': 'Gagal melakukan prediksi dengan BERT'}), 400
            else:
                if fasttext_model is None:
                    return jsonify({'error': 'Gagal memuat model FastText'}), 400
                try:
                    embeddings = get_embeddings(texts, fasttext_model)
                except Exception as e:
                    return jsonify({'error': 'Gagal melakukan embedding dengan model FastText,1'}), 400
                if embeddings is None:
                    return jsonify({'error': 'Gagal melakukan embedding dengan model FastText,2'}), 400
                if ensemble_model is None:
                    return jsonify({'error': 'Gagal memuat model Ensemble'}), 400
                try:
                    if algorithm == 'ensemble':
                        model = ensemble_model
                except Exception as e:
                    return jsonify({'error': 'Gagal memuat model Fakhri'}), 400
                predictions = model.predict(embeddings)


            label_columns = ["Dep", "Per", "Sup", "Usa", "Mis"]
            if algorithm != 'bert':
                # predictions = predictions.reshape(-1, len(label_columns))
                return jsonify({"error": predictions.tolist()})


            # predicted_labels = mlb.inverse_transform(predictions)
            one_hot_labels = np.array(predictions)

            total_reviews = int(len(df))
            total_labels = int(one_hot_labels.sum().sum())
            single_labeled_reviews = int((one_hot_labels.sum(axis=1) == 1).sum())
            multi_labeled_reviews = int((one_hot_labels.sum(axis=1) > 1).sum())

            one_hot_labels_display = np.where(one_hot_labels == 1, '✓', '')
            one_hot_df_display = pd.DataFrame(one_hot_labels_display, columns=label_columns)
            result_df = pd.concat([df, one_hot_df_display], axis=1)

            result_json_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename + 'predictions.json')
            result_df.to_json(result_json_path, orient='records', default_handler=str)

            session['result_json_path'] = result_json_path
            session['algorithm'] = algorithm
            session['total_reviews'] = total_reviews
            session['total_labels'] = total_labels
            session['single_labeled_reviews'] = single_labeled_reviews
            session['multi_labeled_reviews'] = multi_labeled_reviews

            return redirect(url_for('prediction.results'))
        else:
            return "No file uploaded."
    else:
        return 'not post'

@prediction_bp.route('/results')
def results():
    result_json_path = session.get('result_json_path', None)
    if result_json_path:
        return render_template(
            'predictions.html',
            result_json_path=result_json_path,
            algorithm=session.get('algorithm', 'N/A'),
            total_reviews=session.get('total_reviews', 0),
            total_labels=session.get('total_labels', 0),
            single_labeled_reviews=session.get('single_labeled_reviews', 0),
            multi_labeled_reviews=session.get('multi_labeled_reviews', 0)
        )
    else:
        return "No predictions to show."

@prediction_bp.route('/api/predictions', methods=['GET'])
def api_predictions():
    result_json_path = session.get('result_json_path', None)
    if result_json_path:
        with open(result_json_path, 'r') as file:
            data = json.load(file)
        return jsonify(data)
    else:
        return jsonify({"error": "No predictions available"}), 404
