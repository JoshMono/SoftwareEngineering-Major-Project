import subprocess  # Imports the subprocess module to run external scripts/commands
import os          # Imports the os module to work with file and directory paths

def create_file(folder, filename, content):
    # Get the absolute path of the current Python file's directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
 
    # Build the full path to the batch file (assumed to be in the same directory)
    bat_script = os.path.join(current_dir, 'file_manager.bat')
 
    # Replace spaces with underscores in folder and filename
    folder = folder.replace(" ", "_")
    filename = filename.replace(" ", "_")
 
    # If the filename does not end with '.txt', append '.txt' to it
    if not filename.lower().endswith(".txt"):
        filename += ".txt"
 
    # Run the batch file with the folder name, filename, and content as arguments
    print(folder)

    subprocess.run([bat_script, folder, filename, content], shell=True)

def list_txt_files():
    # Get the base directory of the Django project (2 levels up from this file)
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
 
    # Path to the 'files' directory where batch script saves files
    files_dir = os.path.join(base_dir, 'files')
 
    txt_files = []
 
    # Walk through all folders under 'files' and collect .txt files
    for root, dirs, files in os.walk(files_dir):
        for file in files:
            if file.endswith(".txt"):
                # Get relative path from 'files' folder
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, files_dir)
                txt_files.append(rel_path)
 
    return txt_files


def search_word_in_file(rel_path, word):
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    full_path = os.path.join(base_dir, 'files', rel_path)
 
    script_path = os.path.join(os.path.dirname(__file__), 'SearchWord.bat')
 
    try:
        result = subprocess.run(
            [script_path, full_path, word],
            capture_output=True, text=True, shell=True
        )
        count = int(result.stdout.strip())
        return count
    except Exception as e:
        print(f"Batch script error: {e}")
        return 0