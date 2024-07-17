from flask import Flask, request, jsonify
from googletrans import Translator
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
translator = Translator()

@app.route('/translate', methods=['POST'])
def translate_text():
    data = request.get_json()
    text = data.get('text')
    target_language = data.get('target_language')

    if not text or not target_language:
        return jsonify({'error': 'Invalid input'}), 400

    try:
        translated = translator.translate(text, dest=target_language)
        translated_text = translated.text

        # Translate back to English to get phonetic transcription
        transliterated = translator.translate(translated_text, src=target_language, dest='en')
        transliterated_text = transliterated.pronunciation or transliterated.text

        return jsonify({'translated_text': translated_text, 'transliterated_text': transliterated_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)
