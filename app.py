from flask import Flask, request, jsonify
from flask_cors import CORS
import speech_recognition as sr
from deep_translator import GoogleTranslator  # For translation
from flask import render_template

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

@app.route('/')
def index():
    return render_template('index.html')  # Assuming 'index.html' is in a 'templates' folder


@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio_file = request.files['audio']
    language = request.form.get('language', 'en-US')

    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
            transcription = recognizer.recognize_google(audio_data, language=language)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'transcription': transcription})


@app.route('/translate', methods=['POST'])
def translate_text():
    data = request.get_json()
    text = data.get('text')
    target_language = data.get('target_language', 'en')

    if not text:
        return jsonify({'error': 'No text provided for translation'}), 400

    try:
        # Translate the text using deep_translator
        translated_text = GoogleTranslator(source='auto', target=target_language).translate(text)
        return jsonify({'translation': translated_text})
    except Exception as e:
        return jsonify({'error': f"Translation failed: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)
