# Django Projects
This are webs application built with the Django framework.

# Requirements
Python 3.x
pip
Virtual environment (recommended)

# Installation
## Clone the repository
git clone <your-repo-url>
cd <your-project-folder>

# Create virtual environment for each project
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies for each project
pip install -r requirements.txt

# Run the Project for each project
python manage.py migrate
python manage.py runserver

# for each project, Open your browser and go to :
http://127.0.0.1:8000/

# License
This project is licensed under the Apache License 2.0.
