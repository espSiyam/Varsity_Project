from fastapi import FastAPI, HTTPException, File, UploadFile, Form 
import dropbox
from pydantic import BaseModel
import os
import logging
import requests
import subprocess 

# Initialize logging
logging.basicConfig(level=logging.DEBUG)

app = FastAPI()

# Dropbox App key and secret
DROPBOX_APP_KEY = "6xi2mof9qvqtxjz"
DROPBOX_APP_SECRET = "lm0npp4haji7u8r"

# Initialize Dropbox OAuth2 flow
flow = dropbox.DropboxOAuth2FlowNoRedirect(DROPBOX_APP_KEY, DROPBOX_APP_SECRET, "http://localhost:5000/auth/callback")

# Store the access token obtained from the first step
stored_access_token = None

# Function to get the current user's Dropbox access token
def get_current_access_token():
    return stored_access_token

# Manually set the access token here
stored_access_token = "sl.BmQB_9RAY9i3ibgNf3uhEs_WO6065ULnkh02TGsANo9k6x9WHp4e0dlDVwKGGbZbQVGv1MvRxjATYqA6Jdo-fBalUomoMo39W3YC1dUr3b04JqclWpu01D8hB2w8mQvvcU_6Vepkk6WH_Sb2NtVLJtY"


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


# # Model for the request body
# class ConvertToPDFRequest(BaseModel):
#     url: str
#     file_path: str
#     output_pdf_path: str

# # Function to convert a document file to PDF using an external service
# @app.post("/convertpdf/")
# async def convert_to_pdf(request_body: ConvertToPDFRequest):
#     global stored_access_token
#     try:
#         if stored_access_token is None:
#             raise HTTPException(status_code=401, detail="Access token not available. Please set the access token.")

#         # Define the path to save the downloaded source document using the file_path from the request
#         source_document_path = request_body.file_path  # Use the file_path from the request

#         # Define the path to save the converted PDF using the output_pdf_path from the request
#         output_pdf_path = request_body.output_pdf_path  # Use the output_pdf_path from the request

#         # Download the source document from the URL provided in the request
#         response = requests.get(request_body.url)
#         if response.status_code != 200:
#             return {"message": "Failed to download the source document"}

#         # Save the downloaded document to the specified temporary file path
#         with open(source_document_path, "wb") as temp_file:
#             temp_file.write(response.content)

#         # Convert the downloaded document to PDF using an external tool or service
#         # Example: Use unoconv to convert to PDF (make sure unoconv is installed)
#         conversion_command = ["unoconv", "--format", "pdf", "-o", output_pdf_path, source_document_path]
#         subprocess.run(conversion_command, check=True)

#         # Upload the converted PDF to Dropbox using the file path provided in the request
#         dbx = dropbox.Dropbox(stored_access_token)
#         with open(output_pdf_path, "rb") as pdf_file:
#             dbx.files_upload(pdf_file.read(), request_body.file_path)

#         return {"message": f"File '{request_body.file_path}' converted to PDF and uploaded to Dropbox"}
#     except Exception as e:
#         return {"message": f"File conversion to PDF and upload failed: {str(e)}"}
    
# # url: https://www.dropbox.com/scl/fi/jskx2ahmfbrvgb3qqoo0w/goals.docx?rlkey=0la4uwmkj6uidqk2jbrj0ajv6&dl=0
# # 
# # # filepath = /uploads/goals.docx

	
