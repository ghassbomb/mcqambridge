# MCQambridge

MCQambridge is an automated MCQ past paper solving application for Cambridge A-levels & IGCSE. I created this app to save myself the tedious ‘problem’ of having to check my answers between the question paper and marking scheme, counting scores, and calculating percentages. I’ve now expanded it to include a large amount of [subjects](#Subjects) and plan to expand it [further](#features). For now, the app is pretty barebones. You can select your paper, solve it, and you get the results. I plan to add creature comforts soon enough. 

## Installation & Usage

1. Clone the repository with: `   git clone https://github.com/ghassbomb/mcqambridge.git`
2. Change into the project directory: `cd mcqambridge`
3. Install the required dependencies using pip: `pip install -r requirements.txt`
4. Start the Flask development server: `python app.py`
5. Enjoy!

## Features

MCQambridge is pretty barebones currently. You select your paper, answer questions, and are presented with your score and percentage. I intend to add:

- Statistics and tracking for your results
- AI integration

I’m open to requests for features!

### Subjects

Currently, MCQambridge supports the following subjects:

- **IGCSE**
  - Economics (0455)
  - Biology (0610)
  - Chemistry (0620)
  - Physics (0625)
  - Science Combined (0653)
  
- **A-Levels**
  - Biology (9700)
  - Chemistry (9701)
  - Physics (9702)
  - Accounting (9706)
  - Economics (9708)

But the framework for processing other subjects and years is there, and I intend to add all subjects possible (after I’m done fixing the existing selection). Note that **not all subjects or papers may work**. If there is an error, see the [contribution](#contributions) section for reporting it.

## Contributing

Contributions are welcome! If you have any suggestions, improvements, or bug fixes, please create a pull request. For major changes, please open an issue to discuss the changes beforehand. You can also contact me at `ghass.shahzad@gmail.com` for any requests and such, but you should ideally open an issue.

## License

This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).