# import os

# def scan_files(directory):
#     files_to_rename = []
#     for file in os.listdir(directory):
#         if file.startswith("untitled") or file.startswith("unnamed") or file.startswith("New Document"):
#             files_to_rename.append(file)
#     return files_to_rename
# def read_file_content(filepath):
#     with open(filepath, 'r') as file:
#         content = file.read()
#     return content
# import requests

# def suggest_file_name_groqcloud(content):
#     url = "https://console.groq.com/docs/quickstart"  # Replace with actual GroqCloud endpoint
#     headers = {
#         'Authorization': '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',  # Replace with your GroqCloud API key
#         'Content-Type': 'application/json'
#     }
#     data = {
#         "content": content[:500], 
#         "max_tokens": 10          
#     }

#     response = requests.post(url, headers=headers, json=data)

#     # Check if the API call was successful
#     if response.status_code == 200:
#         return response.json().get("suggested_name", "").strip()  # Parse suggested name
#     else:
#         print(f"Error: {response.status_code} - {response.text}")
#         return None
# def rename_file(directory, old_name, new_name):
#     old_path = os.path.join(directory, old_name)
#     new_path = os.path.join(directory, f"{new_name}.txt")

#     # Ensure the new file name doesn't already exist
#     if not os.path.exists(new_path):
#         os.rename(old_path, new_path)
#     else:
#         print(f"File {new_name}.txt already exists. Skipping.")
# def manage_files(directory):
#     files = scan_files(directory)
#     for file in files:
#         filepath = os.path.join(directory, file)
#         content = read_file_content(filepath)
#         suggested_name = suggest_file_name_groqcloud(content)

#         if suggested_name:
#             print(f"Renaming {file} to {suggested_name}.txt")
#             rename_file(directory, file, suggested_name)
#         else:
#             print(f"Could not generate a name for {file}")

# # Example usage
# manage_files('/path/to/your/directory')
import os
import requests

# Function to suggest a name from GroqCloud
def suggest_file_name_groqcloud(content):
    url = "https://api.groqcloud.com/v1/generate-file-name"
    headers = {
        'Authorization': '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',  # Use your actual GroqCloud API key
        'Content-Type': 'application/json'
    }
    data = {"content": content[:500], "max_tokens": 10}

    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json().get("suggested_name", "").strip()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

# Function to scan files and rename them
def scan_and_rename_files(directory):
    for filename in os.listdir(directory):
        if filename.startswith("untitled") or filename.startswith("unnamed"):
            filepath = os.path.join(directory, filename)

            # Read file content
            with open(filepath, 'r') as file:
                content = file.read()

            # Get a suggested name from GroqCloud
            new_name = suggest_file_name_groqcloud(content)
            if new_name:
                new_filepath = os.path.join(directory, f"{new_name}.txt")
                os.rename(filepath, new_filepath)
                print(f"Renamed '{filename}' to '{new_name}.txt'")
            else:
                print(f"Failed to rename '{filename}'.")

# Define the directory to scan
directory = "./test_files"  # Change this to your actual directory
scan_and_rename_files(directory)

