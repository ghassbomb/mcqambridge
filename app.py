import os
import json
from flask import Flask, render_template, request, make_response, url_for, redirect

# Creates flask app
app = Flask(__name__)

ROOT_DIR = os.getcwd()
answers = {}

def get_answers(ms_name):
    """Takes the marking scheme name as a parameter, goes through JSON file to find matching name, and grabs the associated answers list"""
    f = open(os.path.join(ROOT_DIR, 'static', 'answers.json'))
    data = json.load(f)
    print(ms_name)
    if ms_name in data.keys():
        return data[ms_name]
    else:
        return False


def get_paper_name(subj, year, month, variant, ce, alevel):
    """Gets paper name, for statistics and pdf.html title"""
    if (ce is None or ce == 1) and alevel == 'a2-level':
        ce = '3'
    return f"{subj}_{month}{str(year)}_ms_{ce}{variant}"


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/pdf", methods=['GET', 'POST'])
def pdf_display():
    if request.method == 'GET':
        return "The URL / is accessed directly. Try going to '/' to submit the form."

    subj, year, month, variant, ce, alevel = request.form.get('subject', ''), request.form.get('year', ''), request.form.get(
        'month', ''), request.form.get('variant', ''), request.form.get('level', ''), request.form.get('alevel', '')

    if request.method == 'POST':
        paper_name = get_paper_name(subj, year, month, variant, ce, alevel)
        answers = get_answers(paper_name)

        if (answers == False):
            return redirect(url_for('.index', flag=answers))

        resp = make_response(render_template(
            'pdf.html', answers=answers, paper_name=paper_name))
        return resp

@app.route('/pdf_score', methods=['POST'])
def pdf_score():
    paper_name, correct_answers, user_answers = request.form.get('paper_name', ''), request.form.get(
        'correct_answers', '').split(","), request.form.get('user_answers', '').split(",")
    if request.method == 'POST':
        resp = make_response(render_template('pdf_score.html', paper_name=paper_name,
                             correct_answers=correct_answers, user_answers=user_answers))
        return resp

@app.route('/statistics')
def statistics():
    """Page displaying all user attempted papers and scores in them."""
    return render_template('statistics.html')

if __name__ == '__main__':
    app.run(debug=True)
