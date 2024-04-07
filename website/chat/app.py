import subprocess
from flask import Flask, request, jsonify, render_template
from model import get_answer_from_RAG_romanian

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("/chatgpt-clone.html")

@app.route('/execute-python-script' , methods=['POST'])
def execute_python_script():
    options = request.json
    print(options)
    try:
        # result = subprocess.run(['python3', 'static/app.py', options['input']], capture_output=True, text=True)
        result = get_answer_from_RAG_romanian(query=options['input'])
        output = result
        return jsonify({'output': output})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/submit_text", methods=['POST'])
def submit_text():
    text = request.form['text']
    # Process the text (you can perform any processing here)
    response_text = "You submitted: {text}"
    return jsonify({'response': response_text})

if __name__ == '__main__':
    app.run(debug=True)