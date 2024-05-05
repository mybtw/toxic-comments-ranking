from flask import Flask, request, jsonify
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Dense, Input, LSTM, Embedding, Dropout
from tensorflow.keras.layers import Bidirectional, GlobalMaxPool1D
from tensorflow.keras.models import Model
from tensorflow.keras.metrics import AUC
from preprocessor import preprocess_text

app = Flask(__name__)
tf.config.set_visible_devices([], 'GPU')
maxlen = 300

def get_model():
    embedding_matrix = load_embedding_matrix('embedding_matrix_fasttext_untrainableembedding.npy')
    inp = Input(shape=(maxlen,))
    x = Embedding(input_dim=embedding_matrix.shape[0], output_dim=embedding_matrix.shape[1], embeddings_initializer=tf.keras.initializers.Constant(embedding_matrix), trainable = False)(inp)
    x = Bidirectional(LSTM(50, return_sequences=True, dropout=0.1))(x)
    x = GlobalMaxPool1D()(x)
    x = Dense(50, activation="relu")(x)
    x = Dropout(0.1)(x)
    x = Dense(1, activation="sigmoid")(x)
    model = Model(inputs=inp, outputs=x)
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy', AUC(name='roc_auc', curve='ROC')])
    model.load_weights('bilstm.weights_untrainableembedding.h5')
    return model



def load_tokenizer(path):
    with open(path, 'rb') as handle:
        tokenizer = pickle.load(handle)
        return tokenizer

def load_embedding_matrix(path):
    return np.load(path)
    

model = get_model()
tokenizer = load_tokenizer('tokenizer_bilstm_untrainableembedding.pickle')


@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(force=True)
        test_sentences = data['sentences']
        # Обрабатываем каждое предложение перед его токенизацией
        processed_sentences = [preprocess_text(sentence) for sentence in test_sentences]
        test_sequences = tokenizer.texts_to_sequences(processed_sentences)
        test_padded = pad_sequences(test_sequences, maxlen=maxlen, padding='post', truncating='post')
        predictions = model.predict(test_padded).flatten()

        # Создание списка кортежей (предсказание, предложение)
        sentence_prediction_pairs = list(zip(predictions.tolist(), test_sentences))

        # Сортировка списка по убыванию предсказания
        sorted_pairs = sorted(sentence_prediction_pairs, key=lambda x: x[0], reverse=True)

        # Возвращение отсортированных данных
        return jsonify([{'sentence': pair[1], 'prediction': pair[0]} for pair in sorted_pairs])
    except Exception as e:
        return jsonify({"error": str(e)}), 500
