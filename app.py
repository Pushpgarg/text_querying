from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Load the question-answering pipeline
qa_pipeline = pipeline("question-answering")

# Function to handle question-answering
def ask_general_question(text, question):
    result = qa_pipeline(question=question, context=text)
    return result['answer']

# Endpoint for the API root
@app.route('/')
def index():
    return jsonify({"message": "Welcome to the QA API"}), 200

# API endpoint to upload text data
@app.route('/upload', methods=['POST'])
def upload():
    text_data = None
    if 'file' in request.files:
        file = request.files['file']
        if file.filename != '':
            text_data = file.read().decode('utf-8')
    if 'text' in request.form:
        text_data = request.form['text'] if request.form['text'] else text_data

    if text_data:
        return jsonify({"text": text_data}), 200

    return jsonify({"error": "No text provided"}), 400

# API endpoint to handle queries
@app.route('/query', methods=['POST'])
def query():
    context = request.json.get('context')
    question = request.json.get('question')

    if context and question:
        answer = ask_general_question(context, question)
        return jsonify({"answer": answer}), 200

    return jsonify({"error": "Context or question missing"}), 400

if __name__ == '__main__':
    app.run(debug=True)
