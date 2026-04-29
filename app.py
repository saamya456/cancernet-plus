from flask import Flask, render_template, request, jsonify
import numpy as np
from PIL import Image
import os, uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Temporary dummy prediction (until model comes)
def dummy_predict():
    return "Benign", 87.5

def preprocess_image(image_path):
    img = Image.open(image_path).convert('RGB')
    img = img.resize((48, 48))
    img_array = np.array(img) / 255.0
    return np.expand_dims(img_array, axis=0)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    filename = str(uuid.uuid4()) + '.png'
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # TEMPORARY prediction
    label, confidence = dummy_predict()

    return jsonify({
        'label': label,
        'confidence': confidence,
        'image_path': filename,
    })

if __name__ == '__main__':
    os.makedirs('static/uploads', exist_ok=True)
    app.run(debug=True)