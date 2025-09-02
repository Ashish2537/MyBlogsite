# MyBlogsite  

A full-featured Blog Application built with **Flask**, **SQLite**, and **WTForms**, supporting user authentication, blog creation, comments, ratings, and image uploads.  

## Features
-> User Registration & Login (Flask-Login + Password Hashing)  
-> Create, Edit, Delete Blog Posts  
-> Categories & Filters  
-> Comments & Ratings  
-> SQLite Database with SQLAlchemy ORM  

## Live Demo  
👉 [MyBlogsite on Render](https://myblogsite-x307.onrender.com)  

*(click the link to open the deployed app)*  

## Tech Stack  
-> **Backend:** Flask, Flask-SQLAlchemy, Flask-Login, Flask-WTF  
-> **Frontend:** HTML, Bootstrap  
-> **Database:** SQLite3  
-> **Deployment:** Render + Gunicorn  

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
