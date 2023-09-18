from fastapi import FastAPI, Request, Form, File, UploadFile
from fastapi.templating import Jinja2Templates
import dropbox
from fastapi.staticfiles import StaticFiles 

# Initialize the FastAPI app
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize the Dropbox OAuth2 flow
app_key = "2l039laxiucjc1m"        # Replace with your Dropbox app key
app_secret = "9hhpxm2qc14gey9"  # Replace with your Dropbox app secret
flow = dropbox.DropboxOAuth2FlowNoRedirect(app_key, app_secret)

# Initialize Dropbox client (to be used for file upload)
access_token = ""  # Fill this in after authenticating
dbx = None

# Initialize templates
templates = Jinja2Templates(directory="templates")

# Landing page
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Route to start the Dropbox authentication flow
@app.get("/auth")
async def start_auth(request: Request):
    authorize_url = flow.start()
    return {"authorization_url": authorize_url}

# Callback route to handle Dropbox redirect after authentication
@app.get("/auth/callback")
async def auth_callback(request: Request, code: str = Form(...)):
    try:
        global dbx
        access_token, user_id, url_state = flow.finish(code)
        dbx = dropbox.Dropbox(access_token)
        return {"message": "Authentication successful. Access token obtained."}
    except Exception as e:
        return {"message": "Authentication failed. Error: " + str(e)}

# Route to upload a file to Dropbox
@app.post("/upload")
async def upload_file(request: Request, file: UploadFile = File(...)):
    if dbx is None:
        return {"message": "Please authenticate with Dropbox first."}
    
    try:
        file_data = await file.read()
        dbx.files_upload(file_data, f"/{file.filename}")
        return {"message": "File uploaded successfully."}
    except Exception as e:
        return {"message": "File upload failed. Error: " + str(e)}
