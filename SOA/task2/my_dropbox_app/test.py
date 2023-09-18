import requests
import json
import dropbox
from dropbox.exceptions import AuthError
import ipywidgets as widgets
from IPython.display import display, clear_output
from tkinter import Tk, filedialog  # Required for file dialog

# Default access token
default_access_token = ''
# Create widgets for buttons and input
use_default_button = widgets.Button(description='Use Default Access Token')
manual_button = widgets.Button(description='Manually Obtain Access Token')
instructions_button = widgets.Button(description='Show Manual Instructions')
authorization_code_input = widgets.Text(placeholder='Enter Authorization Code')
instructions_output = widgets.Output()

# Create a button for displaying account info
account_info_button = widgets.Button(description='Show Account Info')
account_info_output = widgets.Output()


# Create a button for file upload
upload_button = widgets.Button(description='Upload File')
upload_output = widgets.Output()

# Create an output widget for displaying messages
output = widgets.Output()

# Create a button to list files and folders
list_files_button = widgets.Button(description='List Files in Dropbox App Folder')
list_files_output = widgets.Output()


# Initialize dbx as None
dbx = None

# Function to list files and folders in the Dropbox app folder
def list_files(btn):
    global dbx
    if dbx:
        try:
            result = dbx.files_list_folder('')
            files_list = [entry.name for entry in result.entries]
            with list_files_output:
                clear_output()
                print("Files and Folders in Dropbox App Folder:")
                for item in files_list:
                    print(item)
        except Exception as e:
            with list_files_output:
                clear_output()
                print(f'Error listing files: {str(e)}')
    else:
        with list_files_output:
            clear_output()
            print('Please obtain an access token first.')


# Function to display instructions for manually obtaining an access token
def display_instructions(btn):
    with instructions_output:
        clear_output()
        APP_KEY = ''  # Replace with your app key
        REDIRECT_URL = 'http://localhost:.ipynb'  # Replace with your redirect URL

        print("To manually obtain an access token, follow these steps:")
        print(f"1. Go to the following URL in your web browser:")
        print(f"   https://www.dropbox.com/oauth2/authorize?client_id={APP_KEY}&response_type=code&redirect_uri={REDIRECT_URL}")
        print("2. Log in to your Dropbox account if you're not already logged in.")
        print("3. Authorize the app to access your Dropbox account.")
        print("4. After authorization, you will be redirected to a page with an authorization code.")

# Function to handle using the default access token
def use_default(btn):
    global access_token
    global dbx
    access_token = default_access_token
    try:
        # Check if the default access token authenticates properly
        dbx = dropbox.Dropbox(access_token)
        account_info = dbx.users_get_current_account()
        with output:
            clear_output()
            print("Using default access token.")
            print("...Successful!")
    except Exception as e:
        with output:
            clear_output()
            print("Default access token authentication failed. Please manually obtain an access token.")

# Function to handle manually obtaining an access token
def obtain_manually(btn):
    global access_token
    global dbx
    authorization_code = authorization_code_input.value.strip()

    if authorization_code:
        access_token = get_access_token_manually(authorization_code)
        if access_token:
            dbx = dropbox.Dropbox(access_token)
            with output:
                clear_output()
                print("Access token obtained successfully.")
        else:
            with output:
                clear_output()
                print("Could not obtain access token. Please try again.")
    else:
        with output:
            clear_output()
            print("Please enter the authorization code.")

# Function to manually obtain the access token
def get_access_token_manually(authorization_code):
    # Replace the following with your code to manually obtain the access token
    APP_KEY = ''  # Replace with your app key
    APP_SECRET = ''  # Replace with your app secret
    REDIRECT_URL = 'http://localhost:.ipynb'  # Replace with your redirect URL

    token_url = 'https://api.dropboxapi.com/oauth2/token'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        'code': authorization_code,
        'grant_type': 'authorization_code',
        'client_id': APP_KEY,
        'client_secret': APP_SECRET,
        'redirect_uri': REDIRECT_URL
    }

    response = requests.post(token_url, headers=headers, data=data)
    access_token = response.json().get('access_token')

    return access_token

# Function to handle file upload
def upload_file(btn):
    global dbx
    root = Tk()
    root.withdraw()  # Hide the main window

    file_path = filedialog.askopenfilename()  # Open a file dialog to select a file
    if file_path:
        with open(file_path, 'rb') as file:
            try:
                dbx.files_upload(file.read(), f'/your-dropbox-app-folder/{file_path}')
                with upload_output:
                    clear_output()
                    print(f'File "{file_path}" uploaded successfully.')
            except Exception as e:
                with upload_output:
                    clear_output()
                    print(f'Error uploading file: {str(e)}')
                    
# Function to display account information
def show_account_info(btn):
    global dbx
    if dbx:
        try:
            account_info = dbx.users_get_current_account()
            with account_info_output:
                clear_output()
                print(f'Account Info: {account_info}')
        except Exception as e:
            with account_info_output:
                clear_output()
                print(f'Error fetching account info: {str(e)}')
    else:
        with account_info_output:
            clear_output()
            print('Please obtain an access token first.')


# Attach functions to buttons
use_default_button.on_click(use_default)
manual_button.on_click(obtain_manually)
instructions_button.on_click(display_instructions)
account_info_button.on_click(show_account_info)

upload_button.on_click(upload_file)
list_files_button.on_click(list_files)


# Display the UI
display(use_default_button, manual_button, instructions_button)
display(authorization_code_input, instructions_output)
display(account_info_button, account_info_output)

display(upload_button, upload_output)
display(output)

display(list_files_button, list_files_output)
