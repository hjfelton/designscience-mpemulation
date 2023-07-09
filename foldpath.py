# Get path for results folder

def foldpathmain(model):

    # Import datetime to create folder name
    from datetime import datetime

    # Import path to create folder
    from pathlib import Path
    import os

    # Import regex for string sub
    import re
    import string

    # Get current cd
    cwd = os.getcwd()

    # Overwrite cwd so results are saved in a consistent location on spare SSD
    # cwd = "I:/PhD_Results"

    # Get current time
    now = datetime.now()

    # Convert to string
    now = str(now)
    chars = re.escape(string.punctuation)
    now = re.sub(r'['+chars+']', '_', now)
    now = re.sub(r' ', '_', now)

    # Folder path
    foldpath = cwd + "/results/" + str(model) + "_" + str(now)

    # Create path if it doesn't exist
    Path(foldpath).mkdir(parents=True, exist_ok=True)

    return foldpath

if __name__ == "__main__":

    foldpathmain()