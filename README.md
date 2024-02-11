# Parkomate Parking Analytics Dashboard (Backend)

Frontend - https://github.com/BE-Project-Parkomate/dashboard-frontend

Clone the project-
```
git clone https://github.com/BE-Project-Parkomate/dashboard-backend
```

Create env file-
```
Create a .env file in the project folder with the following fields:
DB_NAME = <db_name>
DB_USER = <db_user>
DB_PASS = <db_password>
DB_HOST = <db_host>
DB_PORT = <db_port>
EMAIL = <email>
EMAIL_PASSWORD = <email_app_password>
```

Build/Start docker images-
```
./run.sh start-dev
```

Migrate the project-
```
./run.sh interactive-dev
python manage.py migrate
```

Stop docker images-
```
./run.sh stop-dev
```
