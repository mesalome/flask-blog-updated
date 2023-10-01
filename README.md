# Flask Project README

This is a simple Flask project that serves as a starting point for your web application. 
It includes instructions on how to set up and run the project.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3 installed
- pip3 installed
- A code editor (e.g., Visual Studio Code, Sublime Text)

## Getting Started

To get this project up and running, follow these steps:

1. Clone the repository to your local machine:

   ```bash
   git clone <repository_url>
   cd <project_directory>
   ```

2. Create a virtual environment to isolate project dependencies:

   ```bash
   python3 -m venv .venv
   ```

3. Activate the virtual environment:

   On macOS and Linux:
   ```bash
   source .venv/bin/activate
   ```

   On Windows (Command Prompt):
   ```bash
   .venv\Scripts\activate
   ```

4. Install Flask and other project dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   ```pip freeze > requirements.txt```

5. Create a local PostgreSQL database named flask_db with the following settings:

   Host: localhost <br /> 
   Port: 5432 <br /> 
   User: postgres <br /> 
   Password: password <br /> 
   Database: flask_db <br /> 
6. In terminal run
   ```bash
   psql postgresql://postgres:password@localhost/flask_db
   CREATE TABLE invalidtokens(token VARCHAR(255),blacklisted_on  VARCHAR(255));
   ```
## Running the Application
7. Ensure that the database settings in your `config.py` file match the configuration of your local PostgreSQL database (`flask_db`). You can find the `config.py` file in your Flask application's codebase.

8. Run the following commands to apply migrations and create database tables: <br /> 
(you might be asked to run ```export APP_SETTINGS=config.Config``` before this  )

   ```bash 
   flask db init
   flask db migrate
   flask db upgrade 
   ```

9.  Go to file migrations/alembic and after  [alembic] add
   ```bash
   sqlalchemy.url = postgresql://postgres:password@localhost:5432/flask_db
   ```
10. run commands:
```bash 
   flask db migrate -m "Initial migration"
   flask db upgrade 
   ```
To start the Flask application, run the following commands:

```bash
export FLASK_ENV=development
export FLASK_APP=run.py
export APP_SETTINGS=config.Config  
flask --app app run --debug
```
OR
``` 
   chmod start.sh
   bash start.sh
```

Your Flask application should now be running at `http://127.0.0.1:5000/`.
