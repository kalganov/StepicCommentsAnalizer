# -*- coding: utf-8 -*-
import comment_sentiment_analyze as analyze
from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/analyze', methods=['POST'])
def analyze_text():
    print(request.form['s'])
    res = analyze.classify(request.form['s'])
    print(res)
    return "<text>" + res.split('\n')[0] + "<br>" + res.split('\n')[1] + "</text>"


@app.route('/')
def hello_world():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
