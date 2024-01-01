import requests


def url_exists(url):
    # Send a HEAD request to check if the URL exists
    response = requests.head(url)
    return response.status_code == requests.codes.ok


subjects = [
    # IGCSE
    "IGCSE/Economics (0455)",
    "IGCSE/Biology (0610)",
    "IGCSE/Chemistry (0620)",
    "IGCSE/Physics (0625)",
    "IGCSE/Science - Combined (0653)",

    # O-Levels
    "O Level/Economics (2281)",
    "O Level/Physics (5054)",
    "O Level/Chemistry (5070)",
    "O Level/Biology (5090)",
    "O Level/Science Combined (5129)",

    # A-Levels
    "AS and A Level/Biology (9700)",
    "AS and A Level/Chemistry (9701)",
    "AS and A Level/Physics (9702)",
    "AS and A Level/Accounting (9706)",
    "AS and A Level/Economics (9708)"
]

years = ['2018', '2019', '2020', '2021', '2022', '2023']
months = ['m', 's', 'w']
levels = ['1', '2']
variants = ['1', '2', '3']

for subject in subjects:
    for year in years:
        for month in months:
            for level in levels:
                for variant in variants:
                    # Skip certain combinations based on conditions

                    # Extended only exists for certain science subjects in IGCSE/O-level
                    if (
                        (subject not in ["IGCSE/Physics (0625)", "IGCSE/Chemistry (0620)", "IGCSE/Biology (0610)", "IGCSE/Science Combined (0653)",
                         "O Level/Biology (5090)", "O Level/Chemistry (5070)", "O Level/Physics (5054)", "O Level/Science Combined (5129)"])
                        and (level == '2')
                    ):
                        continue

                    # Papers of this date have not been uploaded yet
                    if year == '2023' and month == 'w':
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

                    # Only variant 2s in Feb/March in A levels
                    if 'AS and A Level' in subject and variant != 2:
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

                    url = f"https://pastpapers.papacambridge.com/directories/CAIE/CAIE-pastpapers/upload/{subj_code}_{month}{str(year)[2:4]}_ms_{level}{variant}.pdf"

                    # Check if the URL exists
                    if url_exists(url):
                        pass
                    else:
                        print(
                            f"Error - {url}, {subject}, {year}, {month}, {year}, {level}, {variant}")
