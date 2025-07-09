from flask import Flask, request, render_template, send_file
import os
import pandas as pd
from document_parsers.pdf_processor import parse_pdf
from document_parsers.docx_processor import parse_docx
from ai_modules.resume_analyzer import ResumeParser

app = Flask(__name__)
app.config['UPLOADS'] = 'temp_uploads'
os.makedirs(app.config['UPLOADS'], exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'resume' not in request.files:
        return "No file selected", 400
        
    file = request.files['resume']
    if file.filename == '':
        return "Empty file", 400

    save_path = os.path.join(app.config['UPLOADS'], file.filename)
    file.save(save_path)

    try:
        if file.filename.lower().endswith('.pdf'):
            text = parse_pdf(save_path)
        elif file.filename.lower().endswith('.docx'):
            text = parse_docx(save_path)
        else:
            return "Unsupported format", 400
    except Exception as e:
        return f"File processing error: {str(e)}", 500
    finally:
        if os.path.exists(save_path):
            os.remove(save_path)

    try:
        analyzer = ResumeParser()
        results = analyzer.extract_data(text)

        df = pd.DataFrame([results])
        output_path = 'outputs/analysis_results.xlsx'
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_excel(output_path, index=False, engine='openpyxl')

        return send_file(output_path, as_attachment=True)
    except Exception as e:
        return f"Analysis error: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
