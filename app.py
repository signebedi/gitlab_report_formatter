from flask import Flask, request, send_file
from xhtml2pdf import pisa
from io import BytesIO

app = Flask(__name__)

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
    # Extract the discussions from the POST request
    data = request.json
    discussions = data['discussions']

    # Generate the PDF
    pdf = generate_code_review_pdf(discussions)

    # Return the PDF
    return send_file(pdf, attachment_filename="code_review.pdf", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)