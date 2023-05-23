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
    # Start the HTML string
    html = """
    <!DOCTYPE html>
    <html>
    <body>
    <h1>Code Review Comments</h1>
    """

    # Add each discussion to the HTML
    for discussion in discussions:
        note = discussion['notes'][0]
        author = note['author']
        avatar_url = author['avatar_url']
        timestamp = note['created_at']
        username = author['username']
        web_url = author['web_url']
        name = author['name']

        html += f'''
        <hr>
        <div style="display: flex; justify-content: space-between; align-items: start;">
            <div style="flex-grow: 1;">
                <p><strong>{discussion["id"]}</strong>: {note["body"]}</p>
                <p>{name} <a href="{web_url}">@{username}</a></p>
            </div>
            <div style="text-align: right;">
                <img src="{avatar_url}" alt="Avatar" style="height: 50px; width: 50px;">
                <p>{timestamp}</p>
            </div>
        </div>
        '''
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