from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
from PyPDF2 import PdfReader

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/scan-pdf', methods=['POST'])
def scan_pdf():
    if 'pdf' not in request.files or 'keywords' not in request.form:
        return jsonify({"error": "PDF file and keywords are required"}), 400

    # Get the PDF file and keywords
    pdf_file = request.files['pdf']
    keywords = request.form['keywords'].split(',')

    # Load the PDF file
    reader = PdfReader(pdf_file)
    num_pages = len(reader.pages)

    results = []

    # Search through the PDF
    for i in range(num_pages):
        page = reader.pages[i]
        text = page.extract_text()
        
        for keyword in keywords:
            if keyword.lower() in text.lower():
                start = max(0, text.lower().find(keyword.lower()) - 30)
                end = min(len(text), start + 60)
                excerpt = text[start:end]
                results.append({
                    "keyword": keyword,
                    "page": i + 1,
                    "excerpt": excerpt
                })

    return jsonify({"results": results})

if __name__ == '__main__':
    app.run(debug=True)
