# CIS4004 Semester Project

A website which allows users to choose from a selection of games and catalogue what they own and enjoy.

## Local Setup Instructions
This project was built using Python 3.9.7

### Database
Create a locally hosted MySQL database running on port 3306.
- Database name: cis4004
- Collation: utf8mb3_general_ci

Create a user with all privileges on cis4004.
- Username: cis4004
- Password: webgame

### Local Server
Create a virtual environment:
```
py -3 -m venv .venv
.venv\scripts\activate
```

Ensure that pip is installed and up-to-date:
```
python -m pip install --upgrade pip
```

Install the following packages:
```
pip install djangorestframework 
pip install django 
pip install mysqlclient 
pip install beautifulsoup4 
pip install requests
```

Migrate the database using:
```
py manage.py migrate
```

Run the local test server using:
```
py manage.py runserver
```

### Further Reading
Consult this Doc for a more in-depth guide: https://docs.google.com/document/d/15E4MhbAkSb9zbP7Djznj4_MQ7iQaBfwsL1yQyfRsVvw/edit?usp=sharing