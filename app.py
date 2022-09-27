from flask import Flask,render_template
import marko
import os

app = Flask(__name__)

@app.route("/")
def index():
    with open('markdown_files/text1.md', 'r') as file:
        data = file.read()
    return render_template('base.html', data = marko.convert(data))
