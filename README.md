# MyBlogsite  

A full-featured Blog Application built with **Python(Flask), SQLite, and WTForms**.
<br>
This app enables secure Authentication, Blog creation, Comments & Rating, Filtering, and interactive user engagement.  

## Features
• **Authentication** → User registration, login & logout with Flask-Login and password hashing
<br>
• **Blog Management** → Create, edit, and delete blog posts with optional image uploads
<br>
• **Categories & Filters** → Browse blogs by category or search by title
<br>
• **Comments & Ratings** → Engage with posts through feedback and ratings
<br>
• **Database** → SQLite powered with SQLAlchemy ORM 

## Live Demo  *(click the link to open the deployed app)* 
• Azure App Service → [View Deployment](flaskblogapp-cuekdkh3btcyaaeb.centralindia-01.azurewebsites.net)
<br>
• Render → [View Deployment](https://myblogsite-x307.onrender.com)   

## Tech Stack  
• **Language** → Pyhton
• **Backend:** → Flask, Flask-SQLAlchemy, Flask-Login, Flask-WTF  
• **Frontend:** → HTML, Bootstrap5  
• **Database:** → SQLite3
• **Deployment:** → Azure App Service, Render, Gunicorn

## Installation (Local Setup)
```bash
# Clone the repo
git clone https://github.com/Ashish2537/MyBlogsite.git
cd MyBlogsite

# Create virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python routes.py
