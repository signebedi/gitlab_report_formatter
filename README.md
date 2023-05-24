# gitlab_report_formatter



You will need to fetch gitlab data in the client, and pass it to the server.

```python
import requests


# API key for this application
api_key = "your_project_api_key"

# Fetch the discussions from the GitLab API
private_token = 'your_private_token'
project_id = 'your_project_id'
merge_request_id = 'your_merge_request_id'
response = requests.get(
    f'https://gitlab.example.com/api/v4/projects/{project_id}/merge_requests/{merge_request_id}/discussions',
    headers={'PRIVATE-TOKEN': private_token}
)
response.raise_for_status()
discussions = response.json()

# Send the discussions to the Flask application
flask_response = requests.post(
    'http://flask_app.example.com/generate_pdf',
    json={'discussions': discussions, 'name': "YOUR_PROJECT_NAME Code Review"},
    headers={"X-API-KEY": api_key}
)
flask_response.raise_for_status()

# Save the PDF
with open('code_review.pdf', 'wb') as f:
    f.write(flask_response.content)

```