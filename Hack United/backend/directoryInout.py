# # import os

# # def scan_files(directory):
# #     files_to_rename = []
# #     for file in os.listdir(directory):
# #         if file.startswith("untitled") or file.startswith("unnamed") or file.startswith("New Document"):
# #             files_to_rename.append(file)
# #     return files_to_rename
# # def read_file_content(filepath):
# #     with open(filepath, 'r') as file:
# #         content = file.read()
# #     return content
# # import requests

# # def suggest_file_name_groqcloud(content):
# #     url = "https://console.groq.com/docs/quickstart"  # Replace with actual GroqCloud endpoint
# #     headers = {
# #         'Authorization': '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',  # Replace with your GroqCloud API key
# #         'Content-Type': 'application/json'
# #     }
# #     data = {
# #         "content": content[:500], 
# #         "max_tokens": 10          
# #     }

# #     response = requests.post(url, headers=headers, json=data)

# #     # Check if the API call was successful
# #     if response.status_code == 200:
# #         return response.json().get("suggested_name", "").strip()  # Parse suggested name
# #     else:
# #         print(f"Error: {response.status_code} - {response.text}")
# #         return None
# # def rename_file(directory, old_name, new_name):
# #     old_path = os.path.join(directory, old_name)
# #     new_path = os.path.join(directory, f"{new_name}.txt")

# #     # Ensure the new file name doesn't already exist
# #     if not os.path.exists(new_path):
# #         os.rename(old_path, new_path)
# #     else:
# #         print(f"File {new_name}.txt already exists. Skipping.")
# # def manage_files(directory):
# #     files = scan_files(directory)
# #     for file in files:
# #         filepath = os.path.join(directory, file)
# #         content = read_file_content(filepath)
# #         suggested_name = suggest_file_name_groqcloud(content)

# #         if suggested_name:
# #             print(f"Renaming {file} to {suggested_name}.txt")
# #             rename_file(directory, file, suggested_name)
# #         else:
# #             print(f"Could not generate a name for {file}")

# # # Example usage
# # manage_files('/path/to/your/directory')
# import os
# import requests
# # Function to suggest a name from GroqCloud
# def suggest_file_name_groqcloud(content):
#     url = "https://api.groqcloud.com/v1/generate-file-name"
#     headers = {
#         'Authorization': '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',  # Use your actual GroqCloud API key
#         'Content-Type': 'application/json'
#     }
#     data = {"content": content[:500], "max_tokens": 10}

#     response = requests.post(url, headers=headers, json=data)
    
#     if response.status_code == 200:
#         return response.json().get("suggested_name", "").strip()
#     else:
#         print(f"Error: {response.status_code} - {response.text}")
#         return None

# # Function to scan files and rename them
# def scan_and_rename_files(directory):
#     for filename in os.listdir(directory):
#         if filename.startswith("untitled") or filename.startswith("unnamed"):
#             filepath = os.path.join(directory, filename)

#             # Read file content
#             with open(filepath, 'r') as file:
#                 content = file.read()

#             # Get a suggested name from GroqCloud
#             new_name = suggest_file_name_groqcloud(content)
#             if new_name:
#                 new_filepath = os.path.join(directory, f"{new_name}.txt")
#                 os.rename(filepath, new_filepath)
#                 print(f"Renamed '{filename}' to '{new_name}.txt'")
#             else:
#                 print(f"Failed to rename '{filename}'.")

# # Define the directory to scan
# directory = "./test_files"  # Change this to your actual directory
# scan_and_rename_files(directory)

import os
import docx
import requests

# Set your Groq Cloud API key
groq_api_key = "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"
groq_endpoint = "https://api.groq.com/v1/suggest-filename"

# Function to list untitled files
def list_untitled_files(directory):
    untitled_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if any(keyword in file.lower() for keyword in ["untitled", "new document", "new file", "document"]):
                file_path = os.path.join(root, file)
                untitled_files.append(file_path)
    return untitled_files

# Function to read TXT files
def read_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

# Function to read DOCX files
def read_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

# Function to suggest a new file name using Groq Cloud API
def suggest_file_name_groq(content):
    headers = {
        "Authorization": f"Bearer {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}",
        "Content-Type": "application/json"
    }
    
    data = {
        "text": content[:1000]  # Send only the first 1000 characters to avoid too long input
    }
    
    response = requests.post(groq_endpoint, json=data, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        return result.get("suggested_name", "Unnamed_Suggestion")
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

# Function to rename a file
def rename_file(file_path, new_name):
    directory = os.path.dirname(file_path)
    extension = os.path.splitext(file_path)[1]
    new_path = os.path.join(directory, new_name + extension)
    
    if not os.path.exists(new_path):  # Avoid overwriting files
        os.rename(file_path, new_path)
        print(f"File renamed to: {new_path}")
    else:
        print(f"File with name {new_name} already exists.")

# Function to extract content based on file type
def extract_content(file_path):
    extension = os.path.splitext(file_path)[1].lower()
    if extension == ".txt":
        return read_txt(file_path)
    elif extension == ".docx":
        return read_docx(file_path)
    else:
        print(f"Unsupported file type: {extension}")
        return None

# Main function
def main(directory):
    # Step 1: Find untitled files
    untitled_files = list_untitled_files(directory)
    
    if not untitled_files:
        print("No untitled files found.")
        return
    
    # Step 2: Process each file
    for file_path in untitled_files:
        print(f"\nProcessing file: {file_path}")
        
        # Extract content from the file
        content = extract_content(file_path)
        
        if content:
            # Step 3: Get Groq AI suggestion for new file name
            suggested_name = suggest_file_name_groq(content)
            print(f"Suggested new name: {suggested_name}")
            
            # Step 4: Rename the file
            rename_file(file_path, suggested_name)

# Set the directory you want to scan
directory = "/path/to/your/directory"

# Run the program
main(directory)
