from flask import Flask, request, jsonify, redirect, send_file
from werkzeug.utils import secure_filename
import os
from sentiment_analysis import SentimentAnalyzer
from Keyword_cloud_generator import KeywordGenerator
from topic_detection import TopicDetection
import uuid
from flasgger import Swagger
import nltk
# from config import swagger_config

app = Flask(__name__)

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('vader-lexicon')
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "title": 'Text Analysis',  # This is the title that will appear
    "version": '0.0.1',
    "description": 'Description of your API',
    "termsOfService": 'TOS',
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidoc/"
}

swagger = Swagger(app, config=swagger_config)
analyzer = SentimentAnalyzer()
generator = KeywordGenerator()
detector = TopicDetection()


UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/sentiment-analyze', methods=['POST'])
def analyze_sentiment():
    """
    Sentiment Analysis
    ---
    parameters:
      - name: file
        in: formData
        type: file
        required: true
        description: Upload a text file. Example - 'example.txt'
      - name: chunk_size
        in: query
        type: integer
        required: false
        default: 1000
        description: Size of the chunk.

    responses:
      200:
        description: Sentiment Analysis Result
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    chunk_size = int(request.args.get('chunk_size', 1000))

    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400

    filename = secure_filename(file.filename)

    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    sentiment = analyzer.analyze_sentiment(file_path, chunk_size)

    return jsonify(sentiment)

@app.route('/keyword-cloud', methods=['POST'])
def generate_keywords():
    """
    Keyword Cloud Generation
    ---
    parameters:
      - name: file
        in: formData
        type: file
        required: true
        description: Upload a text file. Example - 'example.txt'
      - name: max_words
        in: query
        type: integer
        default: 40
        required: false
        description: Maximum number of words to be included in keyword cloud
      - name: chunk_size
        in: query
        type: integer
        required: false
        default: 1000
        description: Size of the chunk.
      - name: generate_picture
        in: query
        type: boolean
        required: false
        default: false
        description: Whether to generate a picture or not.

    responses:
      200:
        description: Keyword Cloud Result
    """

    # file is not provided
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400
    
    filename = secure_filename(file.filename)
    
    unique_id = str(uuid.uuid4())
    unique_filename = f"{unique_id}_{filename}"

    file_path = os.path.join('uploads', unique_filename)
    file.save(file_path)

    # handling parameters 
    max_words = int(request.args.get('max_words', 40))
    chunk_size = int(request.args.get('chunk_size', 1000))
    generate_picture = request.args.get('generate_picture', 'false').lower() == 'true'

    words = generator.generate_keyword_cloud(file_path, max_words, chunk_size)
    if generate_picture:
        image_path = f"wordcloud_{unique_filename}.png"
        generator.generate_picture(words, image_path)
        return send_file(image_path, mimetype='image/png')
    else:
        return jsonify({"Keywords":generator.generate_keyword_cloud_dict(words)})


@app.route('/topic-detection', methods=['POST'])
def topic_detection():
    """
    Topic Detection
    ---
    parameters:
      - name: file
        in: formData
        type: file
        required: true
        description: Upload a text file. Example - 'example.txt'
      - name: chunk_size
        in: query
        type: integer
        required: false
        default: 1000
        description: Size of the chunk.

    responses:
      200:
        description: Topic Detection Result
    """

    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400

    chunk_size = int(request.args.get('chunk_size', 1000))
    
    filename = secure_filename(file.filename)


    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)
    sentiment = detector.detect_topics(file_path, chunk_size)


    os.remove(file_path)
    return jsonify(sentiment)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return redirect("/apidoc/")

if __name__ == '__main__':
    app.run()