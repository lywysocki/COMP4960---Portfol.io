import os

# get requirements
os.system("pip install -r REQUIREMENTS.txt")

# set up database
readfile_path = os.path.abspath("./Database/readfile.py")
with open(readfile_path) as readfile:
    exec(readfile.read())
