# -*- coding: utf-8 -*-
from flask import Flask, request, render_template

import comment_sentiment_analyze as analyze
import stepik_facade as stepik

app = Flask(__name__)

token = stepik.get_token('credentials')

card = """<div class="card text-center" style="margin-top: 5px">
  <div class="card-header" style="color: black">
    Comment
  </div>
  <div class="card-body" style="background-color: hsl({},100%,50%)">
    <h5 class="card-title" style="color: black">{}</h5>
    <p class="card-text" style="color: black; margin-bottom: 0pt">{}</p>
    {}
    <a href="#" class="btn btn-primary">Переход куда-нибудь</a>
  </div>  
</div>"""

list_of_cards = """<div id="list-of-cards">
                        <div class="table-wrapper-scroll-y my-custom-scrollbar h-100">
                        {}
                                </div>
                    </div>"""


@app.route('/analyze', methods=['POST'])
def analyze_text():
    print(request.form['s'])
    comments = sorted(stepik.get_comments(token, request.form['s']),
                      key=lambda x: res_prob(x),
                      reverse=True)

    cards = ""

    for comment in comments:
        prob = res_prob(comment)
        classy = "<text style=\"color: black\">Probability:" + ' ' + "{0:.2f}".format(
            prob) + "</text><br>"
        user = stepik.get_user(token, comment['user'])
        text = comment['text']

        cards += card.format(get_color(prob), user, text, classy)

    return list_of_cards.format(cards)


@app.route('/')
def hello_world():
    return render_template('index.html')


def get_color(prob):
    return (1 - prob) * 120


def f1_score(prob1, prob2):
    return 2 * (prob1 * prob2) / (prob1 + prob2)


def res_prob(comment):
    tweet_prob, step_prob = analyze.classify(comment)
    return f1_score(1 - tweet_prob[0], tweet_prob[1])


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
