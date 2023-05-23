import logging
from flask import Flask, request, Response
from xhtml2pdf import pisa
from io import BytesIO

app = Flask(__name__)

# Initialize logger
logger = logging.getLogger('api')
handler = logging.FileHandler('api.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

VALID_API_KEYS = ['key1', 'key2', 'key3']

def generate_code_review_pdf(discussions):
    html = """
    <!DOCTYPE html>
    <html>
    <body>
    <h1>Code Review Comments</h1>
    """

    for discussion in discussions:
        html += f'<p><strong>{discussion["id"]}</strong>: {discussion["notes"][0]["body"]}</p>'

    html += """
    </body>
    </html>
    """

    pdf = BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=pdf)

    return pdf

@app.route('/generate_pdf', methods=['POST'])
def handle_generate_pdf():
    api_key = request.headers.get('X-API-KEY')
    if api_key not in VALID_API_KEYS:
        logger.info('Invalid API key used: {}'.format(api_key))
        return {'error': 'Invalid API key'}, 401

    logger.info('API key used: {}'.format(api_key))

    if not request.json:
        return {'error': 'Missing body in request'}, 400

    data = request.json
    if 'discussions' not in data:
        return {'error': 'Missing discussions in request'}, 400
    discussions = data['discussions']

    pdf = generate_code_review_pdf(discussions)
    pdf.seek(0)

    return send_pdf_response(pdf, "code_review.pdf")

def send_pdf_response(pdf_bytes, filename):
    response = Response(pdf_bytes.read(),
                        mimetype="application/pdf",
                        headers={"Content-disposition":
                                     f"attachment; filename={filename}"})
    return response

if __name__ == "__main__":
    app.run(debug=True)