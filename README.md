mkdir pipeline_daddy
cd pipeline_daddy

python -m venv venv
source venv/bin/activate

# install dependencies

pip install flask flask_sqlalchemy flask_login

pip freeze > requirement.txt

📁 1.3 Project Folder Structure (simple version)
csharp
Copy
Edit
project_dashboard/
│
├── app.py                  # Main Flask app
├── requirements.txt
├── venv/
│
├── templates/              # HTML files (frontend)
│   ├── layout.html         # Base layout
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│
└── static/                 # CSS/JS files
    └── styles.css
