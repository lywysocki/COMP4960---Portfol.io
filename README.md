# Portfol.io
A web application which uses stock historical data to make a price prediction for the user based on the ticker which they have imputed into the application.

## Prerequisites
You will need: Python (recommend latest version or 3.11), pip, a few hours for database download
1. Clone the repository 
2. https://dev.mysql.com/downloads/mysql/ Head to this link, select the OS corresponding to your machine, and download. If on Windows, install the version labeled "mysql-installer-web-community-X.X.XX.X.msi".  During the install, if prompted for additional features, click "No thanks, just start my download." Accept all default settings. When prompted to enter a password for the root user enter “Portfol.io2023”
3. Open the root directory of the repository and call `python project_setup.py` from the terminal.
4. Call `python manage.py runserver_plus --cert-file cert.crt` to run the project with HTTPS.
5. Open a browser window to https://127.0.0.1:8000 and skip any trustworthiness warnings. These happen because browsers don't trust self-signed certificates, but it'll be fine. 
