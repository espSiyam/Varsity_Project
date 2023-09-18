from flask import Flask, request, redirect, url_for, jsonify, abort
import dropbox

app = Flask(__name__)

# Dropbox App key and secret
DROPBOX_APP_KEY = "6xi2mof9qvqtxjz"
DROPBOX_APP_SECRET = "lm0npp4haji7u8r"

# Redirect URL for Dropbox OAuth2
DROPBOX_REDIRECT_URI = "http://localhost:5000/auth/callback"

# Initialize Dropbox OAuth2 flow
flow = dropbox.DropboxOAuth2FlowNoRedirect(DROPBOX_APP_KEY, DROPBOX_APP_SECRET, DROPBOX_REDIRECT_URI)

# Store the access token obtained from the first step
stored_access_token = None

# Function to get the current user's Dropbox access token
def get_current_access_token():
    return stored_access_token

# Function to start the Dropbox OAuth2 authentication
@app.route("/auth/start", methods=["POST"])
def start_auth():
    authorize_url = flow.start()
    return jsonify({"authorize_url": authorize_url})

# Function to complete the Dropbox OAuth2 flow by manually entering the code
@app.route("/auth/callback", methods=["GET"])
def auth_callback():
    global stored_access_token
    try:
        code = request.args.get("code")
        if code:
            access_token, user_id = flow.finish(code)

            # Store the access token
            stored_access_token = access_token

            return jsonify({"message": "Authorization completed successfully"})
        else:
            return abort(400, "Authorization code not provided")
    except Exception as e:
        return abort(401, "Authentication failed")

# Function to upload a file to Dropbox
@app.route("/uploadfile", methods=["POST"])
def upload_file():
    global stored_access_token
    try:
        if stored_access_token is None:
            return abort(401, "Access token not available. Please complete the authorization process.")

        dbx = dropbox.Dropbox(stored_access_token)

        # Example: Save the uploaded file to Dropbox's root folder
        with open("example.txt", "rb") as f:
            dbx.files_upload(f.read(), "/example.txt")

        return jsonify({"message": "File uploaded to Dropbox successfully"})
    except Exception as e:
        return abort(500, f"File upload to Dropbox failed: {str(e)}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)