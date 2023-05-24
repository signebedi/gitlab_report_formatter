# gitlab_report_formatter

### Simple Usage

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


### Adding tkinter

If you want an interface that can deal abstractly with multiple projects, you can try running with a tkinter.

```python
import requests
from tkinter import *
from tkinter import messagebox

def send_request():
    try:
        # Fetch the discussions from the GitLab API
        response = requests.get(
            f'https://gitlab.example.com/api/v4/projects/{project_id.get()}/merge_requests/{merge_request_id.get()}/discussions',
            headers={'PRIVATE-TOKEN': private_token.get()}
        )
        response.raise_for_status()
        discussions = response.json()

        # Send the discussions to the Flask application
        flask_response = requests.post(
            'http://flask_app.example.com/generate_pdf',
            json={'discussions': discussions, 'name': f"{project_name.get()} Code Review"},
            headers={"X-API-KEY": api_key.get()}
        )
        flask_response.raise_for_status()

        # Save the PDF
        with open('code_review.pdf', 'wb') as f:
            f.write(flask_response.content)

        root.destroy()  # Close the dialog box after the request is sent
    except Exception as e:
        messagebox.showerror("Error", str(e))

def close_app():
    root.quit()  # stops mainloop

def main():
    global root

    root = Tk()

    # Set the width of the dialog box to 25 percent the screen size
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    dialog_width = screen_width * 0.25
    dialog_height = screen_height * 0.25

    root.geometry(f"{int(dialog_width)}x{int(dialog_height)}")

    global api_key, private_token, project_id, merge_request_id, project_name

    Label(root, text="API Key:").pack()
    api_key = Entry(root)
    api_key.pack()

    Label(root, text="Private Token:").pack()
    private_token = Entry(root)
    private_token.pack()

    Label(root, text="Project ID:").pack()
    project_id = Entry(root)
    project_id.pack()

    Label(root, text="Merge Request ID:").pack()
    merge_request_id = Entry(root)
    merge_request_id.pack()

    Label(root, text="Project Name:").pack()
    project_name = Entry(root)
    project_name.pack()

    Button(root, text="Generate PDF", command=send_request).pack()
    Button(root, text="Close", command=close_app).pack()  # added a close button

    root.mainloop()

if __name__ == "__main__":
    main()
```