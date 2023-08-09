# Appstore Service

## Run The Project In Local Environment

0. Create a .env file from [`.env.sample`](./.env.sample) and update environment variables.

```sh
$ cp .env.sample .env
```

1. Go to the project folder and Create virtualenv.
```
python3 -m virtualenv venv
```
2. Active environment.
```
source venv/bin/activate 
```
3. Install requirements.
```
pip install -r requirements.txt
```
4. Make migrations
```
python manage.py makemigrations
```
5. Migrate model to database
```
python manage.py migrate  
```
6. Run development server
```
python manage.py runserver 
```

## Verify Your Environment Variables

The project provides default environment settings in [`setting.py`](./Appstore/settings.py).
While you can use the default settings, [it's recommended](https://12factor.net/config) to create a `.env` file to store your settings outside of your production code. E.g.:

```config
# .env

DEBUG=1
SECRET_KEY=secret_key

DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1   
REACT_APP_HOST=
CORS_ORIGIN_ALLOW_ALL=0


SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=appstore
SQL_USER=database_username
SQL_PASSWORD=database_password
SQL_HOST=backend
SQL_PORT=5432
```

To get an overview of the environment variables you can set, check the [`setting.py`](./Appstore/settings.py) file.

> ☝️ **Note:** You should never add the `.env` file to your version control system. 

## Visit The Admin Panel For Verifying Apps
You should run this command to create an admin user for this app:
```
python manage.py createsuperuser
```
Now you can access to the admin panel with this link:
- http://127.0.0.1:8000/api/admin/

## Visit The Documentation

You can visit the documentation in Postman Collection:

- https://app.getpostman.com/join-team?invite_code=6969936138bf04f69a178b0435a12a38&target_code=73c73034a213eac86a1b802b60be1ba5

## Dashboard Service

You can visit [`Dashboard Service PDF`](./DashboardService.pdf), about how implement a dashboard service for getting analitycs about users and apps.


## About The Author

Mohammad Amin Parvanian - Email: amin_prvn@outlook.com
