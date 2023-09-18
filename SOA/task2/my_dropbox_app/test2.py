import dropbox
import os

# Replace with your access token
ACCESS_TOKEN = 'sl.BmSOmQp5iXfHM9CrW2mR3AHKOTalt4WVWeTaoa_g_PBOxew_gIEUSFIJnfTWlf2POyM0T7oYfaVhwDPhHbeoR_bvzdXXIgRBt4Sgi3lhH60RExBR1p6P7CiLOJZleoYlTKzEpaBhZ8o1ancmOmBjI-U'

def upload_file(file_path, dropbox_path):
    try:
        # Initialize Dropbox client
        dbx = dropbox.Dropbox(ACCESS_TOKEN)

        # Check if the file exists
        if os.path.exists(file_path):
            # Open the file for reading in binary mode
            with open(file_path, 'rb') as file:
                # Upload the file to Dropbox
                dbx.files_upload(file.read(), dropbox_path)

            print(f"File '{file_path}' uploaded to Dropbox as '{dropbox_path}'")
        else:
            print(f"File '{file_path}' does not exist.")

    except dropbox.exceptions.AuthError as e:
        print(f"Authentication failed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Specify the local file path and the Dropbox destination path
    local_file_path = './data/test.txt'
    dropbox_destination_path = local_file_path

    upload_file(local_file_path, dropbox_destination_path)
