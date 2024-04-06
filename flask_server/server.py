from flask import Flask, request, render_template, redirect, jsonify
import os
import json

# Note: static folder means all files from there will be automatically served over HTTP
app = Flask(__name__, static_folder="public")
app.secret_key = "miau".encode("utf-8")

DATABASE_FILE = "database.json"


@app.route("/")
def index():
    return render_template("index.html")



@app.route("/chat")
def chat():
    return render_template("/chatbot.html")

@app.route("/submit_text", methods=['POST'])
def submit_text():
    text = request.form['text']
    # Process the text (you can perform any processing here)
    response_text = "You submitted: {text}"
    return jsonify({'response': response_text})

@app.errorhandler(404)
def error404(code):
    # bonus: make it show a fancy HTTP 404 error page, with red background and bold message ;)
    return "HTTP Error 404 - Page Not Found"


# Run the webserver (port 5000 - the default Flask port)
if __name__ == "__main__":
    app.run(debug=True, port=5000)
