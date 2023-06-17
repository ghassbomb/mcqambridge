from flask import Flask, render_template, request, send_from_directory
import requests
import os
from PyPDF2 import PdfReader
import re


# Creates flask app
app = Flask(__name__)
answers = {}

def extract_answers(ms):
    """Takes the marking scheme as a parameter, goes through it, and stores all its contents in a 'dump'."""
    answers = ''
    with open(ms, 'rb') as file:
        reader = PdfReader(file)
        for pageno in range(1, len(reader.pages)):
            answers += (reader.pages[pageno]).extract_text()
    return answers


def ans_filter(raw):
    """Takes the dump generated in extract_answers() and filters it to extract all MCQ answers in a list (by extracting all individual letters)"""
    raw_list = re.findall(r'\b[A-D]\b', raw)
    lst = [x for x in raw_list if len(x) == 1]
    return lst

def download_pdfs(subj, year, month, variant, ce):
    """Takes the inputs from the forms on the homepage and uses them to download the corresponding question paper and marking scheme."""
    subj_code = ''
    flag = False
    root_dir = os.getcwd()

    # Extracts subj_code from subj
    for char in subj:
        if char == '(':
            flag = True
            continue
        if char == ')':
            flag = False
        if flag == True:
            subj_code += char
    
    # Levels/CE is sometimes returned as 'None' when the user changes the value in the form, but then switches to a subject for which it is not available
    if ce is None:
        ce = 1

    # Creates a URL based on the given variables to gceguide.com and downloads the marking scheme and question paper
    url_ms = f"https://papers.gceguide.com/{subj}/{year}/{subj_code}_{month}{str(year)[2:4]}_ms_{ce}{variant}.pdf"
    url_qp = f"https://docs.google.com/viewer?url=https://papers.gceguide.com/{subj}/{year}/{subj_code}_{month}{str(year)[2:4]}_qp_{ce}{variant}.pdf&embedded=true"
    r = requests.get(url_ms, allow_redirects=True)
    open(os.path.join(root_dir, 'static', 'pdf', 'ms.pdf'), 'wb').write(r.content)
    return url_qp


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/pdf", methods=['GET', 'POST'])
def pdf_display():
    global pdf_link
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

        question_number = 0
        score = 0  # Initialize the score to 0
        return render_template('pdf.html', question_number=question_number, answers=answers, score=score, pdf_link=pdf_link)


@app.route('/static/pdf/<path:filename>')
def serve_pdf(filename):
    root_dir = os.getcwd()
    return send_from_directory(os.path.join(root_dir, 'static', 'pdf'), filename)


@app.route("/pdf_answers", methods=['POST'])
def pdf_answers():
    pdf_link = request.form.get('pdf_link')
    question_number = int(request.form.get('question_number'))
    user_answer = request.form.get('user_answer')

    raw_mess = extract_answers('static/pdf/ms.pdf')
    correct_answers = ans_filter(raw_mess)

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
        # The user has answered all the questions
        return render_template('pdf_score.html', score=score, total_questions=len(correct_answers), answers=answers, correct_answers=correct_answers)
    return render_template('pdf.html', question_number=next_question_number, answers=correct_answers, score=score, feedback=feedback, pdf_link=pdf_link)

if __name__ == '__main__':
    app.run(debug=True)