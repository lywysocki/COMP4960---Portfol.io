# Portfol.io
A web application which uses stock historical data to make a price prediction for the user based on the ticker which they have imputed into the application.

## Prerequisites
You will need: Python 3 (recommend latest version or 3.11), pip, a few hours for database download
1. Clone the repository and switch to the "Josh" branch
2. pip install -r REQUIREMENTS.txt
3. Download mySQL server. For windows, use this link: https://dev.mysql.com/downloads/ and the "MySQL installer for windows" link at the bottom.
4. Run readfile.py in the Database folder to download the database
5. Switch back to the main directory and call python manage.py runserver_plus --cert-file cert.crt  This will generate an HTTPS certificate for the website.
6. Open a browser window to https://127.0.0.1:8000 and skip any trustworthiness warnings. These happen because browsers don't trust self-signed certificates, but it'll be fine. 
