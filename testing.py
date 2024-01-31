import os
import requests
import json
from docx.api import Document
from pdf2docx import Converter

ROOT_DIR = os.getcwd()
final_json = {}

subjects = [
    # IGCSE
    "Cambridge IGCSE/Economics (0455)",
    "Cambridge IGCSE/Biology (0610)",
    "Cambridge IGCSE/Chemistry (0620)",
    "Cambridge IGCSE/Physics (0625)",
    "Cambridge IGCSE/Science - Combined (0653)",
    "IGCSE/Economics (0455)",
    "IGCSE/Biology (0610)",
    "IGCSE/Chemistry (0620)",
    "IGCSE/Physics (0625)",
    "IGCSE/Science - Combined (0653)",

    # O-Levels
    "O Levels/Economics (2281)",
    "O Levels/Physics (5054)",
    "O Levels/Chemistry (5070)",
    "O Levels/Biology (5090)",
    "O Levels/Science - Combined (5129)",
    "O Level/Economics (2281)",
    "O Level/Physics (5054)",
    "O Level/Chemistry (5070)",
    "O Level/Biology (5090)",
    "O Level/Science Combined (5129)",

    # A-Levels
    "A Levels/Biology (9700)",
    "A Levels/Chemistry (9701)",
    "A Levels/Physics (9702)",
    "A Levels/Accounting (9706)",
    "A Levels/Economics (9708)"
    "AS and A Level/Biology (9700)",
    "AS and A Level/Chemistry (9701)",
    "AS and A Level/Physics (9702)",
    "AS and A Level/Accounting (9706)",
    "AS and A Level/Economics (9708)"
]

years = ['2018', '2019', '2020', '2021', '2022', '2023']
months = ['m', 's', 'w']
levels = ['1', '2', '3']
variants = ['1', '2', '3']


def url_exists(url):
    # Send a HEAD request to check if the URL exists
    response = requests.head(url)
    return response.status_code == requests.codes.ok


def extract_answers(file):
    # Converts given pdf 'file' to DOCX, extracts MCQ answers, and returns them as a list
    data = []
    WF = 'markingscheme.docx'
    cv = Converter(file)
    cv.convert(WF)
    wf_cont = Document(WF)

    for table in wf_cont.tables:
        for i, row in enumerate(table.rows):
            text = [cell.text for cell in row.cells]
            if i == 0:
                keys = tuple(text)
                continue
            row_data = dict(zip(keys, text))
            if 'Answer ' in row_data.keys():
                data.append(row_data['Answer '].strip())
            elif 'Answer' in row_data.keys():
                data.append(row_data['Answer'].strip())

    cv.close()
    return data


for subject in subjects:
    for year in years:
        for month in months:
            for level in levels:
                for variant in variants:
                    # Skip certain combinations based on conditions

                    # Extended only exists for certain science subjects in IGCSE
                    if (
                        (subject not in ["IGCSE/Physics (0625)", "IGCSE/Chemistry (0620)",
                         "IGCSE/Biology (0610)", "IGCSE/Science Combined (0653)"])
                        and (level == '2')
                    ):
                        continue

                    # level 3 only exists for A level subjects
                    if (subject != 'AS and A Level/Economics (9708)' and level == '3'):
                        continue

                    # Only variant 2s in Feb/March papers for IGCSE
                    if variant != '2' and month == 'm' and 'IGCSE' in subject:
                        continue

                    # No Feb/March papers for O level subjects
                    if (
                        ('O Level' in subject)
                        and (month == 'm')
                    ):
                        continue

                    # No variant 3s in May/June papers for O level subjects
                    if (
                        ('O Level' in subject)
                        and (month == 's' and variant == '3')
                    ):
                        continue

                    # No variant 3s in Oct/Nov papers for most O level subjects, and no variant 1s for Econ
                    if (
                        (subject in ["O Level/Biology (5090)", "O Level/Chemistry (5070)",
                         "O Level/Physics (5054)", "O Level/Science Combined (5129)"])
                        and (month == 'w' and variant == '3')
                    ):
                        continue

                    if "O Level/Economics (2281)" in subject and (month == 'w' and variant == '1'):
                        continue

                    # Only variant 2s in Feb/March in AS levels
                    if month == 'm' and variant != 2 and level == 1 and subject in ["AS and A Level/Biology (9700)", "AS and A Level/Chemistry (9701)", "AS and A Level/Physics (9702)", "AS and A Level/Accounting (9706)", "AS and A Level/Economics (9708)"]:
                        continue

                    # Only variant 2s in Feb/March in A2 levels for Econ
                    if subject in ["AS and A Level/Economics (9708)"] and month == 'm' and level == 3 and variant != 2:
                        continue

                    if (level is None or level == 1) and alevel == 'a2-level':
                        level = '3'

                    # Extract the subject code from the subject string
                    subj_code = ''
                    flag = False
                    for char in subject:
                        if char == '(':
                            flag = True
                            continue
                        if char == ')':
                            flag = False
                        if flag:
                            subj_code += char

                    # Construct the filename, and ms URL
                    file_name = f"{subj_code}_{month}{str(year)[2:4]}_ms_{level}{variant}.pdf"

                    url_ms = f"https://pastpapers.papacambridge.com/directories/CAIE/CAIE-pastpapers/upload/{file_name}"

                    # Check if the URL exists
                    if url_exists(url_ms):
                        # Download it as 'ms.pdf'
                        r = requests.get(url_ms, allow_redirects=True)
                        open(os.path.join(ROOT_DIR, 'ms.pdf'),
                             'wb').write(r.content)
                        # Extract answers and add them to final_json
                        final_json[file_name] = extract_answers('ms.pdf')
                    else:
                        # Throw error
                        print(
                            f"Error - {file_name}, {subject}, {year}, {month}, {level}, {variant}")

with open('answers.json', 'w') as f:
    json.dump(final_json, f)
