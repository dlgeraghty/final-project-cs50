from flask import Flask
import marko

app = Flask(__name__)

@app.route("/")
def index():
    with open('markdown_files/text1.md', 'r') as file:
        data = file.read()
    return marko.convert(data)
