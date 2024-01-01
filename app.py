import os
import re
import json
from flask import Flask, render_template, request, send_from_directory, make_response
import requests
from PyPDF2 import PdfReader

# Creates flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)
answers = {}
papers = {}
subject_mapping = {
    '0455': 'IGCSE/Economics (0455)',
    '0610': 'IGCSE/Biology (0610)',
    '0620': 'IGCSE/Chemistry (0620)',
    '0625': 'IGCSE/Physics (0625)',
    '0653': 'IGCSE/Science - Combined (0653)',
    '2281': 'O Level/Economics (2281)',
    '5054': 'O Level/Physics (5054)',
    '5070': 'O Level/Chemistry (5070)',
    '5090': 'O Level/Biology (5090)',
    '5129': 'O Level/Science Combined (5129)',
    '9700': 'AS and A Level/Biology (9700)',
    '9701': 'AS and A Level/Chemistry (9701)',
    '9702': 'AS and A Level/Physics (9702)',
    '9706': 'AS and A Level/Accounting (9706)',
    '9708': 'AS and A Level/Economics (9708)'
}


def extract_answers(ms):
    """Takes the marking scheme as a parameter, goes through it, and stores all its contents in a 'dump'."""
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


def download_pdfs(subj, year, month, variant, ce):
    """Takes the inputs from the forms on the homepage and uses them to download the corresponding question paper and marking scheme."""
    root_dir = os.getcwd()

    # Levels/CE is sometimes returned as 'None' when the user changes the value in the form, but then switches to a subject for which it is not available
    if ce is None:
        ce = 1

    # Creates a URL based on the given variables to the papacambridge pdf and downloads the marking scheme and question paper
    url_qp = f"https://docs.google.com/viewer?url=https://pastpapers.papacambridge.com/directories/CAIE/CAIE-pastpapers/upload/{subj}_{month}{str(year)}_qp_{ce}{variant}.pdf&embedded=true"
    url_ms = f"https://pastpapers.papacambridge.com/directories/CAIE/CAIE-pastpapers/upload/{subj}_{month}{str(year)}_ms_{ce}{variant}.pdf"
    print(url_qp)
    r = requests.get(url_ms, allow_redirects=True)
    open(os.path.join(root_dir, 'static', 'pdf', 'ms.pdf'), 'wb').write(r.content)
    return url_qp


def get_paper_name(subj, year, month, variant, ce):
    """Gets paper name, for statistics and pdf.html title"""

    if ce is None:
        ce = 1

    return f"{subj}_{month}{str(year)[2:4]}_qp_{ce}{variant}"


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/pdf", methods=['GET', 'POST'])
def pdf_display():
    if request.method == 'GET':
        return "The URL / is accessed directly. Try going to '/' to submit the form."

    subj = request.form.get('subject')
    year = request.form.get('year')
    month = request.form.get('month')
    variant = request.form.get('variant')
    ce = request.form.get('level')

    if request.method == 'POST':
        pdf_link = download_pdfs(subj, year, month, variant, ce)
        raw_mess = extract_answers('static/pdf/ms.pdf')
        answers = ans_filter(raw_mess)
        paper_name = get_paper_name(subj, year, month, variant, ce)

        question_number = 0
        score = 0  # Initialize the score to 0

        papers_json = request.cookies.get('papers_scores')
        papers = json.loads(papers_json) if papers_json else {}

        resp = make_response(render_template('pdf.html', question_number=question_number, answers=answers, score=score, pdf_link=pdf_link, paper_name=paper_name))
        resp.set_cookie('papers_scores', json.dumps(papers))

        return resp


@app.route('/static/pdf/<path:filename>')
def serve_pdf(filename):
    root_dir = os.getcwd()
    return send_from_directory(os.path.join(root_dir, 'static', 'pdf'), filename)


@app.route("/pdf_answers", methods=['POST'])
def pdf_answers():
    pdf_link = request.form.get('pdf_link')
    question_number = int(request.form.get('question_number'))
    user_answer = request.form.get('user_answer')
    paper_name = request.form.get('paper_name')

    raw_mess = extract_answers('static/pdf/ms.pdf')
    correct_answers = ans_filter(raw_mess)

    papers_json = request.cookies.get('papers_scores')
    papers = json.loads(papers_json) if papers_json else {}

    answers[question_number] = user_answer
    # Compare user's answer with the correct answer
    if user_answer.lower() == correct_answers[question_number].lower():
        # Correct answer
        score = int(request.form.get('score')) + 1
        feedback = "Correct!"
    else:
        # Incorrect answer
        score = int(request.form.get('score'))
        feedback = "Incorrect."

    next_question_number = question_number + 1

    if next_question_number >= len(correct_answers):
        papers[paper_name] = round((score/len(correct_answers))*100, 1)

        resp = make_response(render_template('pdf_score.html', score=score, total_questions=len(
            correct_answers), answers=answers, correct_answers=correct_answers))
        resp.set_cookie('papers_scores', json.dumps(papers))

        return resp
    resp = make_response(render_template('pdf.html', question_number=next_question_number,
                         answers=correct_answers, score=score, feedback=feedback, pdf_link=pdf_link, paper_name=paper_name))
    resp.set_cookie('papers_scores', json.dumps(papers))

    return resp


@app.route('/statistics')
def statistics():
    papers_json = request.cookies.get('papers_scores')
    papers = json.loads(papers_json) if papers_json else {}

    return render_template('statistics.html', papers=papers, subject_mapping=subject_mapping)

if __name__ == '__main__':
    app.run(debug=True)
