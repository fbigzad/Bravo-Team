# Campus Scheduler Planner
A simple Django web app for students to plan classes, work shifts, study time, and personal tasks.  
It includes **Daily / Weekly / Monthly** calendar views, a **schedule item detail page**, and basic CRUD actions (create + view + delete).

## Features

- User authentication: **signup, login, logout**
- Dashboard with quick navigation
- Create schedule items (title, date, time, duration, type, notes)
- Calendar views:
  - **Daily** (24-hour timeline)
  - **Weekly** (grid by hour/day)
  - **Monthly** (full calendar month grid)
- Click any event to open a **details page**
- Delete/remove schedule items

## Tech Stack

- Python (local dev: 3.13.x)
- Django (project uses a recent Django version locally)
- SQLite (local + PythonAnywhere demo)
- HTML templates + CSS (no front-end framework)


## Run on Your PC (Local Development)

1. Clone the github Repository:
   ```bash
   git clone https://github.com/fbigzad/Bravo-Team.git
2. Enter the Project Folder:
   ```bash
   cd Bravo_Team
3. create a virtual Environment
   ```bash
   python -m venv venv
   venv\Scripts\Activate
4. Open `settings.py` file to change `DEBUG` value for local development
   - Path: `scheduler/settings.py`
5. Set `DEBUG` value to `True` for local development
   - `DEBUG = True`
   - Click **Save**
5. Install requirements.txt
   ```bash
   pip install -r requirements.txt
6. Run migrations (creates database tables)
   ```bash
   python manage.py migrate
7. Create admin user (optional)
	```bash
	python manage.py createsuperuser
8. Start the Django server
   ```bash
   python manage.py runserver

Then open:

http://127.0.0.1:8000/

## Deploy on PythonAnywhere (Demo)
This project can be deployed on **PythonAnywhere** using **SQLite** for a simple 

### 1) Create a PythonAnywhere account
- Sign up at PythonAnywhere and log in.
- Open a **Bash console** from the **Consoles** tab.

### Step 1) Create the Web App (Python 3.10)
1. Go to **PythonAnywhere → Web**
2. Click **Add a new web app**
3. Choose:
   - **Manual configuration**
   - **Python 3.10**
4. After it creates the app, stay on the **Web** tab (we will edit settings there).



### Step 2) Open a Bash Console
1. Go to **Consoles**
2. Start a **Bash** console

---
### Step 3) Clone the repo on PythonAnywhere
	
		cd ~
		git clone https://github.com/fbigzad/Bravo-Team.git
		cd Bravo-Team
3. Create a Python 3.10 virtualenv
   ```bash
   python3.10 -m venv venv
4. Activate the Virtual Environment
   ```bash
   source venv/bin/activate
5. Upgrade pip
   ```bash
   python -m pip install --upgrade pip
6. Install requirements
   ```bash
   pip install -r requirements.txt

## Step 4) Update settings.py for PythonAnywhere
	nano scheduler/settings.py

1. Make sure these are set:


		DEBUG = False

		ALLOWED_HOSTS = [
		    "YOURUSERNAME.pythonanywhere.com",
		]
		
		CSRF_TRUSTED_ORIGINS = [
		    "https://YOURUSERNAME.pythonanywhere.com",
		]
		
		STATIC_URL = "/static/"
		STATIC_ROOT = BASE_DIR / "staticfiles"


Save nano:

Press CTRL + O then Enter

Press CTRL + X

## Step 5) Run migrations (SQLite database)

		
		python manage.py migrate
## Step 6) Collect static files (so CSS works)
	python manage.py collectstatic --noinput

## Step 7) Set PythonAnywhere Web tab settings

Go to Web tab and set:

A) Virtualenv

In the Virtualenv field, enter:

	/home/YOURUSERNAME/Bravo-Team/venv

B) Source code

Set Source code to:

	/home/YOURUSERNAME/Bravo-Team

## Step 8) Configure the WSGI file

On the Web tab, click the WSGI file link and replace its contents with:

		import os
		import sys
		
		path = "/home/YOURUSERNAME/Bravo-Team"
		if path not in sys.path:
		    sys.path.insert(0, path)
		
		os.environ["DJANGO_SETTINGS_MODULE"] = "scheduler.settings"
		
		from django.core.wsgi import get_wsgi_application
		application = get_wsgi_application()


Save the file.

## Step 9) Add Static Files mapping (Web tab)

On the Web tab → Static files, add:

URL:

	/static/


Directory:

	/home/YOURUSERNAME/Bravo-Team/staticfiles

## Step 10) Reload the Web App

On the Web tab, click:

Reload

Then open:

	https://YOURUSERNAME.pythonanywhere.com

# Common Issues (Fast Fixes)
## 1) "No module named django"

Your web app is not using the same virtualenv you installed packages into.

Confirm Web tab Virtualenv is:
	/home/YOURUSERNAME/Bravo-Team/venv

In Bash:

	source ~/Bravo-Team/venv/bin/activate
	pip install -r requirements.txt

## 2) "TemplateDoesNotExist"

Linux is case-sensitive. Example:

signUp.html is NOT the same as signup.html
Make sure your template filename matches exactly what your view renders.

## 3) Static files not loading

Run:

	python manage.py collectstatic --noinput


And confirm Static files mapping is added in the Web tab.

## 4) 500 error after reload

Open the Error log in the Web tab and check the traceback.
Most of the time it’s:

wrong WSGI path

wrong virtualenv path

missing migrations

			
# Installation / Access Instructions

To start using the application, you will need:

- A modern web browser (Chrome, Firefox, Safari, or Edge)
- An internet connection

### Access the Application

1. Open a web browser.
2. Enter the following URL into the browser address bar: [https://frb.pythonanywhere.com](https://frb.pythonanywhere.com)

### Open the Application

- The Campus Scheduler Planner will load automatically.
- You will be directed to the **Login page**.

### Create an Account

1. From the Login page, select the option to create an account.
2. Enter the required registration information.

### Log In and Use the Application


1. After creating an account, return to the Login page.
2. Enter your credentials to log in.
3. You will now have access to the Campus Scheduler Planner features.

### Tips

- For better performance, use an up-to-date browser.
- No downloads or installations are required since the application is hosted online.
- The application is designed to be user-friendly and accessible for users with minimal technical knowledge.
