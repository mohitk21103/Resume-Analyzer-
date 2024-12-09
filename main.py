import json
import os
import PyPDF2
import docx2txt
import google.generativeai as genai
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename

from analysis import ResumeAnalyzer

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

key = os.environ.get("myGemKey")

genai.configure(api_key=key)
model = genai.GenerativeModel("gemini-1.5-flash", generation_config={"response_mime_type": "application/json"})
analyzer = ResumeAnalyzer()


def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text


def extract_text_from_docx(file_path):
    return docx2txt.process(file_path)


def extract_text_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def extract_text(file_path):
    if file_path.endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        return extract_text_from_docx(file_path)
    elif file_path.endswith('.txt'):
        return extract_text_from_txt(file_path)
    else:
        return ""


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'


@app.route("/")
def matchresume():
    # Render template with an empty report or None if it's a GET request
    return render_template('index.html', report=None)


# @app.route('/matcher', methods=['POST', 'GET'])
@app.route('/matcher', methods=['POST'])
def matcher():
    if request.method == 'POST':
        # Get job description
        job_description = request.form.get('job_description', '').strip()
        if not job_description:
            return render_template('index.html', error_message="Job description is required.")

        # Get resume file
        resume_file = request.files.get('resume')
        if not resume_file:
            return render_template('index.html', error_message="Resume file is required.")

        # Save the uploaded file
        try:
            filename = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(resume_file.filename))
            resume_file.save(filename)
        except Exception as e:
            return render_template('index.html', error_message="Failed to save the resume file.")

        # Extract text from the resume
        try:
            resume_txt = extract_text(filename)
        except Exception as e:
            return render_template('index.html', error_message="Failed to extract text from the resume.")

        # Generate prompt
        try:
            prompt = analyzer.generate_prompt(job_description, resume_txt)
        except Exception as e:
            return render_template('index.html', error_message="Failed to generate prompt.")

        # Generate response from the model
        try:
            response = model.generate_content(prompt)
            analysis_result = response.text
            analysis_dict = json.loads(analysis_result)
        except Exception as e:
            return render_template('index.html', error_message="Failed to analyze the resume.")

        # Return the analysis results to be rendered in the template

        return render_template('index.html', report=analysis_dict)

    return render_template('index.html', error_message="Invalid request method.")


if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
