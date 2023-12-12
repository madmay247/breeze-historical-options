import requests
import os
import zipfile

def master_symbol_downloader():
    
    # Define the URL of the file to download
    url = "https://directlink.icicidirect.com/NewSecurityMaster/SecurityMaster.zip"

    # Define the folder name
    folder_name = "master_symbols"

    # Create the folder if it doesn't exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Get the filename from the URL
    file_name = url.split("/")[-1]

    # Define the path where the file will be saved
    file_path = os.path.join(folder_name, file_name)

    # Check if the file already exists
    if os.path.exists(file_path):
        print(f"The file '{file_name}' already exists in the '{folder_name}' folder.")
    else:
        # Download the file
        response = requests.get(url)
        if response.status_code == 200:
            with open(file_path, "wb") as file:
                file.write(response.content)
            print(f"File '{file_name}' has been downloaded and saved to the '{folder_name}' folder.")

            # Extract the ZIP file
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(folder_name)
            print(f"ZIP file '{file_name}' has been extracted.")

            # Remove the ZIP file
            os.remove(file_path)
            print(f"ZIP file '{file_name}' has been deleted.")
        else:
            print(f"Failed to download the file. Status code: {response.status_code}")