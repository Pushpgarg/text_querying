# app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

from flask import Flask, request, render_template
from transformers import pipeline
import os

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
# Load the question-answering pipeline
qa_pipeline = pipeline("question-answering")

def ask_general_question(text, question):
    result = qa_pipeline(question=question, context=text)
    return result['answer']

@app.route('/')
def index():
    return render_template('index.html')

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
        return render_template('results.html', text=text_data)

    return "No text provided", 400

@app.route('/query', methods=['POST'])
def query():
    context = request.form['context']
    question = request.form['question']

    if context:
        answer = ask_general_question(context, question)
        return {'answer': answer}

    return "No context provided", 400

if __name__ == '__main__':
    app.run(debug=True)
