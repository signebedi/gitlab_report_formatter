from flask import Flask, request, send_file
import requests
from xhtml2pdf import pisa
from io import BytesIO

app = Flask(__name__)

@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    # Extract the GitLab data from the POST request
    data = request.json
    private_token = data['private_token']
    project_id = data['project_id']
    merge_request_id = data['merge_request_id']

    # Fetch the discussions from the GitLab API
    response = requests.get(
        f'https://gitlab.example.com/api/v4/projects/{project_id}/merge_requests/{merge_request_id}/discussions',
        headers={'PRIVATE-TOKEN': private_token}
    )
    response.raise_for_status()
    discussions = response.json()

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

    # Return the PDF
    return send_file(pdf, attachment_filename="code_review.pdf")

if __name__ == "__main__":
    app.run(debug=True)