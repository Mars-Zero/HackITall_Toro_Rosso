from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("/chatgpt-clone.html")

@app.route("/submit_text", methods=['POST'])
def submit_text():
    text = request.form['text']
    # Process the text (you can perform any processing here)
    response_text = "You submitted: {text}"
    return jsonify({'response': response_text})

if __name__ == '__main__':
    app.run(debug=True)