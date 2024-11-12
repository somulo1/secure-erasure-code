import os
import numpy as np
import librosa
import cv2
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def load_and_preprocess_data(file_path, file_type):
    if file_type == 'image':
        return load_and_preprocess_image(file_path)
    elif file_type == 'audio':
        return load_and_preprocess_audio(file_path)
    elif file_type == 'document':
        return load_and_preprocess_document(file_path)
    elif file_type == 'video':
        return load_and_preprocess_video(file_path)
    else:
        raise ValueError("Invalid file type. Supported types are 'image', 'audio', 'document', 'video'.")

def load_and_preprocess_image(image_file):
    image = cv2.imread(image_file)
    image = cv2.resize(image, (224, 224))  
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  
    image = image.astype(np.float32) / 255.0  
    return image

def load_and_preprocess_audio(audio_file, target_sr=22050, duration=10):
    y, sr = librosa.load(audio_file, sr=target_sr, duration=duration)
    mfccs = librosa.feature.mfcc(y=y, sr=sr)
    return mfccs

def load_and_preprocess_document(text_file):
    with open(text_file, 'r', encoding='utf-8') as file:
        text = file.read()
        tokens = text.split()
    return tokens

def load_and_preprocess_video(video_file, num_frames=5):
    cap = cv2.VideoCapture(video_file)
    frames = []
    for _ in range(num_frames):
        ret, frame = cap.read()
        if ret:
            frame = cv2.resize(frame, (224, 224))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = frame.astype(np.float32) / 255.0
            frames.append(frame)
    cap.release()
    return np.array(frames)

def extract_features(data):
    # Placeholder function to return the original data as features
    return data

def preprocess_and_extract_features(file_path, file_type):
    data = load_and_preprocess_data(file_path, file_type)
    # Perform feature extraction here
    features = extract_features(data)
    return features

def compare_features(features1, features2):
    mse = np.mean((features1 - features2) ** 2)
    return mse

def assess_integrity_level(mse_value, integrity_violated=False):
    if integrity_violated:
        return "Integrity Violated"
    elif mse_value < 1e-6:
        return "Very High"
    elif 1e-6 <= mse_value < 1e-4:
        return "High"
    elif 1e-4 <= mse_value < 1e-2:
        return "Medium"
    elif 1e-2 <= mse_value < 1:
        return "Low"
    else:
        return "Very Low or Integrity Violated"

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    file_type = request.form['type']  # Assuming 'type' field is sent with the request
    if file and file_type in ['image', 'audio', 'document', 'video']:
        # Save the uploaded file to a temporary location
        filename = secure_filename(file.filename)
        temp_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(temp_file_path)
        
        # Extract features from the uploaded file
        global original_features  # Define original_features as global variable
        original_features = preprocess_and_extract_features(temp_file_path, file_type)
        
        # Delete the temporary file
        os.remove(temp_file_path)
        
        # Return success message
        return jsonify({"message": "Upload successful"}), 200
    else:
        return jsonify({"error": "Invalid file or file type"}), 400

@app.route('/download', methods=['POST'])
def download():
    file = request.files['file']
    file_type = request.form['type']  # Assuming 'type' field is sent with the request
    if file and file_type in ['image', 'audio', 'document', 'video']:
        # Save the downloaded file to a temporary location
        filename = secure_filename(file.filename)
        temp_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(temp_file_path)
        
        # Extract features from the downloaded file
        comparison_features = preprocess_and_extract_features(temp_file_path, file_type)
        
        # Delete the temporary file
        os.remove(temp_file_path)
        
        # Compare features and assess integrity level
        mse = compare_features(original_features, comparison_features)
        integrity_level = assess_integrity_level(mse)
        
        return jsonify({"integrity_level": integrity_level}), 200
    else:
        return jsonify({"error": "Invalid file or file type"}), 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
