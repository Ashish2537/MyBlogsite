from routes import app, db
from models import UserModel, BlogModel, BlogComment, CategoryMaster

# Create tables within app context
with app.app_context():
    db.create_all()

print("Database tables created successfully!")

