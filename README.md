# Parkomate Parking Analytics Dashboard Backend

This is the backend for the project.
<br>
Frontend - https://github.com/BE-Project-Parkomate/dashboard-frontend

Clone the project-
```
git clone https://github.com/BE-Project-Parkomate/dashboard-backend
```

Install dependencies-
```
pip install -r requirements.txt
```

Create env file for MySQL credentials-
```
Create a .env file in the project folder with the following fields:
DB_NAME = <db_name>
DB_USER = <db_user>
DB_PASSWORD = <db_password>
DB_HOST = <db_host>
DB_PORT = <db_port>
SUPERUSER_ORGANIZATION = 2f939198-3102-448b-92ea-e56eef1272c5
```

Migrate the project-
```
python manage.py migrate
```

Run local server-
```
python manage.py runserver
```
