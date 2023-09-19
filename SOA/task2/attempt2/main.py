from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from fastapi.responses import HTMLResponse
import dropbox
import os
from jinja2 import Environment, FileSystemLoader
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

app = FastAPI()

# Dropbox App key and secret
DROPBOX_APP_KEY = "6xi2mof9qvqtxjz"
DROPBOX_APP_SECRET = "lm0npp4haji7u8r"

# Initialize Dropbox OAuth2 flow
flow = dropbox.DropboxOAuth2FlowNoRedirect(DROPBOX_APP_KEY, DROPBOX_APP_SECRET, "http://localhost:8000/auth/callback")

# Store the access token obtained from the first step
stored_access_token = None

# Function to get the current user's Dropbox access token
def get_current_access_token():
    return stored_access_token

# Manually set the access token here
stored_access_token = "sl.BmUioBp2MR-jNOK8aP6fHCpLAznJqXhgyo_EZMmAQqCkAz01UZJjXviw-QZKv-zsRZQf_bAK8-w6mBpP5Xe04jtccb9KlAn2FH2yldtPQYHkPMhQW0SwzdNflSPz3eSIBkDMCELd7LjJjDe3RtMK6yE"

# Jinja2 template environment setup
templates_env = Environment(loader=FileSystemLoader("templates"))
templates = {
    "homepage": templates_env.get_template("homepage.html"),
    # "upload": templates_env.get_template("upload.html"),
    # "copy": templates_env.get_template("copy.html"),
    # "move": templates_env.get_template("move.html"),
    # "rename": templates_env.get_template("rename.html"),
    # "delete": templates_env.get_template("delete.html"),
}

# Function to render HTML templates
def render_template(template_name, **kwargs):
    template = templates.get(template_name)
    if template:
        return HTMLResponse(content=template.render(**kwargs))
    else:
        raise HTTPException(status_code=500, detail=f"Template {template_name} not found")

# Function to get user account information from Dropbox
def get_user_account_info():
    global stored_access_token
    try:
        if stored_access_token is None:
            raise HTTPException(status_code=401, detail="Access token not available. Please set the access token.")

        dbx = dropbox.Dropbox(stored_access_token)

        # Get current account information
        account_info = dbx.users_get_current_account()
        return account_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve user account information: {str(e)}")


# Function to render the homepage
@app.get("/", response_class=HTMLResponse)
async def homepage():
    account_info = get_user_account_info()
    return render_template("homepage", user_info=account_info)


# Function to upload a file to Dropbox
@app.post("/uploadfile/")
async def upload_file(file: UploadFile):
    global stored_access_token
    try:
        if stored_access_token is None:
            raise HTTPException(status_code=401, detail="Access token not available. Please set the access token.")

        dbx = dropbox.Dropbox(stored_access_token)
        
        # Save the uploaded file to Dropbox's root folder
        with file.file as f:
            dbx.files_upload(f.read(), f"/{file.filename}")
        
        return {"message": f"File '{file.filename}' uploaded to Dropbox successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload to Dropbox failed: {str(e)}")

# Function to copy a file in Dropbox
@app.post("/copyfile/")
async def copy_file(source_path: str = Form(...), destination_path: str = Form(...)):
    global stored_access_token
    try:
        if stored_access_token is None:
            raise HTTPException(status_code=401, detail="Access token not available. Please set the access token.")

        dbx = dropbox.Dropbox(stored_access_token)

        # Perform the copy operation
        dbx.files_copy(source_path, destination_path)

        return {"message": f"File copied from '{source_path}' to '{destination_path}' successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File copy operation failed: {str(e)}")
# Function to move a file in Dropbox
@app.post("/movefile/")
async def move_file(source_path: str = Form(...), destination_path: str = Form(...)):
    global stored_access_token
    try:
        if stored_access_token is None:
            raise HTTPException(status_code=401, detail="Access token not available. Please set the access token.")

        dbx = dropbox.Dropbox(stored_access_token)

        # Perform the move operation
        dbx.files_move(source_path, destination_path)

        return {"message": f"File moved from '{source_path}' to '{destination_path}' successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File move operation failed: {str(e)}")

# Function to delete a file in Dropbox
@app.post("/deletefile/")
async def delete_file(file_path: str = Form(...)):
    global stored_access_token
    try:
        if stored_access_token is None:
            raise HTTPException(status_code=401, detail="Access token not available. Please set the access token.")

        dbx = dropbox.Dropbox(stored_access_token)

        # Perform the delete operation
        dbx.files_delete(file_path)

        return {"message": f"File at '{file_path}' deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File delete operation failed: {str(e)}")

# Function to rename a file in Dropbox
@app.post("/renamefile/")
async def rename_file(file_path: str = Form(...), new_name: str = Form(...)):
    global stored_access_token
    try:
        if stored_access_token is None:
            raise HTTPException(status_code=401, detail="Access token not available. Please set the access token.")

        dbx = dropbox.Dropbox(stored_access_token)

        # Get the parent folder and construct the new path
        folder, _ = os.path.split(file_path)
        new_path = os.path.join(folder, new_name)

        # Perform the rename operation
        dbx.files_move(file_path, new_path)

        return {"message": f"File renamed to '{new_name}' successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File rename operation failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)