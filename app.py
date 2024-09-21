from flask import Flask, request, jsonify
import fitz  # PyMuPDF to handle PDFs

app = Flask(__name__)

@app.route('/scan-pdf', methods=['POST'])
def scan_pdf():
    if 'pdf' not in request.files or 'keywords' not in request.form:
        return jsonify({"error": "PDF file and keywords are required"}), 400

    pdf_file = request.files['pdf']
    keywords = request.form['keywords'].split(',')

    # Load the PDF
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    
    results = []

    # Search for keywords across all pages
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text = page.get_text("text")

        for keyword in keywords:
            if keyword.lower() in text.lower():
                # Extract a small excerpt
                index = text.lower().find(keyword.lower())
                excerpt = text[max(0, index - 50):index + len(keyword) + 50]
                
                results.append({
                    "keyword": keyword,
                    "page": page_num + 1,  # Page numbers are 1-indexed
                    "excerpt": excerpt.strip()
                })

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
