from flask import Flask, render_template, request, send_from_directory
import requests
import os
from PyPDF2 import PdfReader
import re

app = Flask(__name__)

def extract_answers(ms):
    """Takes the marking scheme as a parameter, goes through it, and stores all its contents in a string."""
    answers = ''
    with open(ms, 'rb') as file:
        reader = PdfReader(file)

        for pageno in range(1, len(reader.pages)):
            page = reader.pages[pageno]
            text = page.extract_text()
            answers += text

    return answers

def ans_filter(raw):
    """Takes the string generated in extract_answers() and filters it to extract all MCQ answers in a list (by extracting all individual letters)"""
    raw_list = re.findall("[a-zA-Z]+", raw)
    lst = [x for x in raw_list if len(x) == 1] 
    return lst

def download_pdfs(subj, year, month, variant, ce):
    """Takes the inputs from the forms on the homepage and uses them to download the corresponding question paper and marking scheme."""
    subj_code = ''
    flag = False
    root_dir = os.getcwd()

    # Extracts subject code from subject
    for char in subj:
        if char == '(':
            flag = True
            continue
        if char == ')':
            flag = False
        if flag == True:
            subj_code+=char
     
    url_ms = f"https://papers.gceguide.com/Cambridge IGCSE/{subj}/{year}/{subj_code}_{month}{str(year)[2:4]}_ms_{ce}{variant}.pdf"
    url_qp = f"https://papers.gceguide.com/Cambridge IGCSE/{subj}/{year}/{subj_code}_{month}{str(year)[2:4]}_qp_{ce}{variant}.pdf"
    r = requests.get(url_qp, allow_redirects=True)
    open(os.path.join(root_dir, 'static', 'pdf', 'qp.pdf'), 'wb').write(r.content)
    r = requests.get(url_ms, allow_redirects=True)
    open(os.path.join(root_dir, 'static', 'pdf', 'ms.pdf'), 'wb').write(r.content)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/pdf", methods=['POST', 'GET'])
def pdf_display():
    if request.method == 'GET':
        return "The URL / is accessed directly. Try going to '/' to submit the form."

    elif request.method == 'POST':
        subj = request.form.get('subject')
        year = request.form.get('year')
        month = request.form.get('month')
        variant = request.form.get('variant')
        ce = request.form.get('level')

        download_pdfs(subj, year, month, variant, ce)
        raw_mess = extract_answers('static/pdf/ms.pdf')
        answers = ans_filter(raw_mess)
        
        question_number = 0
        score = 0  # Initialize the score to 0
        return render_template('pdf.html', question_number=question_number, answers=answers, score=score)

@app.route('/static/pdf/<path:filename>')
def serve_pdf(filename):
    root_dir = os.getcwd()
    return send_from_directory(os.path.join(root_dir, 'static', 'pdf'), filename)

@app.route("/pdf_answers", methods=['POST'])
def pdf_answers():
    question_number = int(request.form.get('question_number'))
    user_answer = request.form.get('user_answer')
    
    # Load the correct answers from the marking scheme
    raw_mess = extract_answers('static/pdf/ms.pdf')
    correct_answers = ans_filter(raw_mess)
    print(user_answer) 
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
        return render_template('pdf_score.html', score=score, total_questions=len(correct_answers))
    print(score)
    return render_template('pdf.html', question_number=next_question_number, answers=correct_answers, score=score, feedback=feedback)

if __name__ == '__main__':
    app.run(debug=True)
