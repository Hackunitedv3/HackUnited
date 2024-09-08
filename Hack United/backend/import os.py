import os
import openai
def find_unnamed_files(directory):
    unnamed_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if "Untitled" in file or "New Document" in file or file.startswith("Document"):
                file_path = os.path.join(root, file)
                unnamed_files.append(file_path)
    return unnamed_files

def suggest_file_name(file_content):
    openai.api_key = 'your-openai-api-key'  # Open AI key here
    
    response = openai.Completion.create(
        engine="text-davinci-003", 
        prompt=f"Suggest a meaningful file name based on the following content: {file_content}",
        max_tokens=10
    )
    return response.choices[0].text.strip()
