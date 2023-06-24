import requests

def url_exists(url):
    # Send a HEAD request to check if the URL exists
    response = requests.head(url)
    return response.status_code == requests.codes.ok

subjects = [
    # IGCSE
    "Cambridge IGCSE/Economics (0455)",
    "Cambridge IGCSE/Biology (0610)",
    "Cambridge IGCSE/Chemistry (0620)",
    "Cambridge IGCSE/Physics (0625)",
    "Cambridge IGCSE/Science - Combined (0653)",

    # O-Levels
    "O Levels/Economics (2281)",
    "O Levels/Physics (5054)",
    "O Levels/Chemistry (5070)",
    "O Levels/Biology (5090)",
    "O Levels/Science - Combined (5129)",

    # A-Levels
    "A Levels/Biology (9700)",
    "A Levels/Chemistry (9701)",
    "A Levels/Physics (9702)",
    "A Levels/Accounting (9706)",
    "A Levels/Economics (9708)"
]

years = ['2018', '2019', '2020', '2021', '2022']
months = ['m', 's', 'w']
levels = ['1', '2']
variants = ['1', '2', '3']

for subject in subjects:
    for year in years:
        for month in months:
            for level in levels:
                for variant in variants:
                    # Skip certain combinations based on conditions
                    if (
                        (subject not in ["Cambridge IGCSE/Physics (0625)", "Cambridge IGCSE/Chemistry (0620)", "Cambridge IGCSE/Biology (0610)", "Cambridge IGCSE/Science - Combined (0653)", "O Levels/Biology (5090)", "O Levels/Chemistry (5070)", "O Levels/Physics (5054)", "O Levels/Science - Combined (5129)"])
                        and (level == '2')
                    ):
                        continue
                    if year == '2022' and month == 'w':
                        continue
                    if (
                        (subject in ["O Levels/Biology (5090)", "O Levels/Chemistry (5070)", "O Levels/Physics (5054)", "O Levels/Science - Combined (5129)", "O Levels/Economics (2281)"])
                        and (month == 'm')
                    ):
                        print("heelo")
                        continue
                    if (
                        (subject in ["O Levels/Biology (5090)", "O Levels/Chemistry (5070)", "O Levels/Physics (5054)", "O Levels/Science - Combined (5129)", "O Levels/Economics (2281)"])
                        and (month == 's' and variant == '3')
                    ):
                        print("hlo")
                        continue
                    if (
                        (subject in ["O Levels/Biology (5090)", "O Levels/Chemistry (5070)", "O Levels/Physics (5054)", "O Levels/Science - Combined (5129)", "O Levels/Economics (2281)"])
                        and (month == 'w' and variant == '1')
                    ):
                        print("helo")
                        continue
                    if variant != '2' and month == 'm':
                        continue
                    if (
                        (subject in ["O Levels/Biology (5090)", "O Levels/Chemistry (5070)", "O Levels/Physics (5054)", "O Levels/Science - Combined (5129)"])
                        and (month == 'w' and variant == '3')
                    ):
                        continue
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
                    
                    # Construct the URL
                    url = f"https://papers.gceguide.com/{subject}/{year}/{subj_code}_{month}{str(year)[2:4]}_ms_{level}{variant}.pdf"
                    
                    # Check if the URL exists
                    if url_exists(url):
                        pass
                    else:
                        print(f"Error - {url}, {subject}, {year}, {month}, {year}, {level}, {variant}")