import os
import re
import json
from flask import Flask, render_template, request, send_from_directory, make_response, url_for, redirect
import requests
from PyPDF2 import PdfReader

# Creates flask app
app = Flask(__name__)
answers = {}


def extract_answers(ms):
    """Takes the marking scheme as a parameter, goes through it, and stores all its contents in a 'dump'"""
    mcqanswers = ''
    with open(ms, 'rb') as file:
        reader = PdfReader(file)
        for pageno in range(1, len(reader.pages)):
            mcqanswers += (reader.pages[pageno]).extract_text()
    return mcqanswers


def ans_filter(raw):
    """Takes the dump generated in extract_answers() and filters it to extract all MCQ answers in a list (by extracting all individual letters through regex)"""
    raw_list = re.findall(r'\b[A-D]\b', raw)
    lst = [x for x in raw_list if len(x) == 1]
    return lst


def download_pdfs(subj, year, month, variant, ce, alevel):
    """Takes the inputs from the forms on the homepage and uses them to download the corresponding question paper and marking scheme."""
    root_dir = os.getcwd()

    if (ce is None or ce == 1) and alevel == 'a2-level':
        ce = '3'

    # Creates a URL based on the given variables to the papacambridge pdf and downloads the marking scheme and question paper
    url_qp = f"https://pastpapers.papacambridge.com/directories/CAIE/CAIE-pastpapers/upload/{subj}_{month}{str(year)}_qp_{ce}{variant}.pdf"
    url_ms = f"https://pastpapers.papacambridge.com/directories/CAIE/CAIE-pastpapers/upload/{subj}_{month}{str(year)}_ms_{ce}{variant}.pdf"

    response = requests.head(url_qp)
    if not (response.status_code == requests.codes.ok):
        return False

    for url, pdf_name in zip([url_ms, url_qp], ['ms.pdf', 'qp.pdf']):
        r = requests.get(url, allow_redirects=True)
        open(os.path.join(root_dir, 'static', 'pdf',
             pdf_name), 'wb').write(r.content)
    return True

def get_paper_name(subj, year, month, variant, ce, alevel):
    """Gets paper name, for statistics and pdf.html title"""
    if (ce is None or ce == 1) and alevel == 'a2-level':
        ce = '3'
    return f"{subj}_{month}{str(year)[2:4]}_qp_{ce}{variant}"


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
        pdf_link = download_pdfs(subj, year, month, variant, ce, alevel)

        if (pdf_link == False):
            return redirect(url_for('.index', flag=pdf_link))

        raw_mess = extract_answers('static/pdf/ms.pdf')
        answers = ans_filter(raw_mess)
        paper_name = get_paper_name(subj, year, month, variant, ce, alevel)

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
    """Page displaying all attempted papers and scores in them."""
    return render_template('statistics.html')


if __name__ == '__main__':
    app.run(debug=True)
