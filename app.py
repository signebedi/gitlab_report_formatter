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

from datetime import datetime
import pytz

def convert_utc_to_est(utc_timestamp_str):
    # Parse the UTC timestamp string to a datetime object
    utc_timestamp = datetime.strptime(utc_timestamp_str, "%Y-%m-%dT%H:%M:%S.%fZ")

    # Set the timezone of the timestamp to UTC
    utc_timestamp = utc_timestamp.replace(tzinfo=pytz.UTC)

    # Convert to Eastern Time
    est_timestamp = utc_timestamp.astimezone(pytz.timezone('America/New_York'))

    # Format the timestamp
    formatted_timestamp = est_timestamp.strftime("%Y-%m-%d %H:%M:%S")

    return formatted_timestamp


def generate_code_review_pdf(discussions):
    # Start the HTML string
    html = f'''
    <!DOCTYPE html>
    <html>
    <body>
    <h1>Code Review Comments</h1>
    <p style="text-align: right;">{datetime.now(pytz.timezone('America/New_York')).strftime("%Y-%m-%d %H:%M:%S")}</p>
    '''

    for discussion in discussions:
        notes = discussion['notes']
        first_note = notes[0]
        author = first_note['author']
        avatar_url = author['avatar_url']
        timestamp = convert_utc_to_est(first_note['created_at'])
        username = author['username']
        web_url = author['web_url']
        name = author['name']

        # Unfortunately, a great deal of styles are not supported by xhtml2pdf...
        # https://xhtml2pdf.readthedocs.io/en/latest/reference.html#supported-css-properties

        html += f'''
        <hr>
        <table style="width: 100%;">
            <tr>
                <td style="width: 30px; padding-right: 10px; vertical-align: top;">
                    <div style="height: 30px; width: 30px; overflow: hidden;">
                        <img src="{avatar_url}" alt="Avatar" style="height: 30px; width: 30px;">
                    </div>
                </td>
                <td style="vertical-align: top;">
                    <p>{name} <a href="{web_url}">@{username}</a></p>
                    <p><strong>{discussion["id"]}</strong>: {first_note["body"]}</p>
        '''

        for note in notes[1:]:

            _author = note['author']
            _avatar_url = author['avatar_url']
            _timestamp = convert_utc_to_est(note['created_at'])
            _username = author['username']
            _web_url = author['web_url']
            _name = author['name']

            html += f'''
                    <hr style="border-top: 1px dotted #000; color: transparent; background-color: transparent; height: 1px; width:100%;">
                    <table>
                        <tr>
                            <td style="width: 30px;"><img src="{_avatar_url}" alt="Avatar" style="height: 10px; width: 10px;"></td>
                            <td>{_name} <a href="{_web_url}">@{_username}</a></td>
                            <td style="text-align: right; vertical-align: top;">{_timestamp}</td>
                        </tr>
                        <tr>
                            <td colspan="3">{note["body"]}</td>
                        </tr>
                    </table>
                    '''

        html += f'''
                </td>
                <td style="text-align: right; vertical-align: top;">
                    <p>{timestamp}</p>
                </td>
            </tr>
        </table>
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