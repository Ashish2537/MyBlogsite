from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone

db = SQLAlchemy()

# User Model
class UserModel(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    blogs = db.relationship('BlogModel', backref='author', lazy=True)
    comments = db.relationship('BlogComment', backref='commenter', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# Category Model
class CategoryMaster(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), nullable=False, unique=True)
    
    blogs = db.relationship('BlogModel', backref='category', lazy=True)


# Blog Model
class BlogModel(db.Model):
    __tablename__ = 'blogs'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    
    image = db.Column(db.String(255), nullable=True) 

    comments = db.relationship('BlogComment', backref='blog', lazy=True)


# Comment + Rating Model
class BlogComment(db.Model):
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    blog_comment = db.Column(db.Text, nullable=False)
    blog_rating = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)