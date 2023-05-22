from flask import Flask, request, send_file, jsonify
from xhtml2pdf import pisa
from io import BytesIO

app = Flask(__name__)

# Replace this with your actual API keys
VALID_API_KEYS = ['key1', 'key2', 'key3']

def generate_code_review_pdf(discussions):
    # Start the HTML string
    html = """
    <!DOCTYPE html>
    <html>
    <body>
    <h1>Code Review Comments</h1>
    """

    # Add each discussion to the HTML
    for discussion in discussions:
        html += f'<p><strong>{discussion["id"]}</strong>: {discussion["notes"][0]["body"]}</p>'

    # End the HTML string
    html += """
    </body>
    </html>
    """

    # Convert the HTML to a PDF
    pdf = BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=pdf)

    return pdf

@app.route('/generate_pdf', methods=['POST'])
def handle_generate_pdf():
    # Check the API key
    api_key = request.headers.get('X-API-KEY')
    if api_key not in VALID_API_KEYS:
        return jsonify({'error': 'Invalid API key'}), 401

    # Ensure there is a body in the request
    if not request.json:
        return jsonify({'error': 'Missing body in request'}), 400

    # Extract the discussions from the POST request
    data = request.json
    if 'discussions' not in data:
        return jsonify({'error': 'Missing discussions in request'}), 400
    discussions = data['discussions']

    # Generate the PDF
    pdf = generate_code_review_pdf(discussions)

    # Return the PDF
    return send_file(pdf, attachment_filename="code_review.pdf", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
