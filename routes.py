from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from models import db, UserModel, BlogModel, CategoryMaster, BlogComment
from forms import RegisterForm, LoginForm, BlogForm, CommentForm, FilterForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mysite.db'
app.config['SECRET_KEY'] = 'yoursecretkey'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(UserModel, int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = UserModel(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Registration successful. Please log in.")
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = UserModel.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('view_all_blogs'))
        flash("Invalid email or password.")
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/create_blog', methods=['GET', 'POST'])
@login_required
def create_blog():
    form = BlogForm()
    form.category.choices = [(c.id, c.category_name) for c in CategoryMaster.query.all()]

    if form.validate_on_submit():
        image_file = request.files.get('image')
        filename = None
        if image_file and image_file.filename != '':
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(image_path)

        blog = BlogModel(
            title=form.title.data,
            content=form.content.data,
            user_id=current_user.id,
            category_id=form.category.data,
            created_at=datetime.utcnow(),
            image=filename  # make sure your BlogModel has this column
        )
        db.session.add(blog)
        db.session.commit()
        flash("Blog created successfully.")
        return redirect(url_for('view_all_blogs'))

    return render_template('create_blog.html', form=form)

@app.route('/blogs', methods=['GET', 'POST'])
def view_all_blogs():
    form = FilterForm()
    form.category.choices = [(0, "All Categories")] + [(c.id, c.category_name) for c in CategoryMaster.query.all()]

    blogs = BlogModel.query
    if form.validate_on_submit():
        if form.category.data and form.category.data != 0:
            blogs = blogs.filter_by(category_id=form.category.data)
        if form.search.data:
            blogs = blogs.filter(BlogModel.title.ilike(f"%{form.search.data}%"))
    blogs = blogs.all()

    return render_template('blogs.html', blogs=blogs, form=form)

@app.route('/blog/<int:blog_id>', methods=['GET', 'POST'])
def view_blog(blog_id):
    blog = BlogModel.query.get_or_404(blog_id)
    comment_form = CommentForm()

    if comment_form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You must be logged in to comment.")
            return redirect(url_for('login'))

        comment = BlogComment(
            blog_id=blog_id,
            blog_comment=comment_form.blog_comment.data,
            blog_rating=comment_form.blog_rating.data,
            user_id=current_user.id,
            created_at=datetime.utcnow()
        )
        db.session.add(comment)
        db.session.commit()
        flash("Comment added successfully.")
        return redirect(url_for('view_blog', blog_id=blog_id))

    comments = BlogComment.query.filter_by(blog_id=blog_id).all()
    ratings = [c.blog_rating for c in comments]
    avg_rating = round(sum(ratings) / len(ratings), 2) if ratings else 0

    return render_template('view_blog.html', blog=blog, comments=comments, form=comment_form, avg_rating=avg_rating)

@app.route('/edit_blog/<int:blog_id>', methods=['GET', 'POST'])
@login_required
def edit_blog(blog_id):
    blog = BlogModel.query.get_or_404(blog_id)
    if blog.user_id != current_user.id:
        flash("Unauthorized access.")
        return redirect(url_for('view_all_blogs'))

    form = BlogForm(obj=blog)
    form.category.choices = [(c.id, c.category_name) for c in CategoryMaster.query.all()]

    if form.validate_on_submit():
        blog.title = form.title.data
        blog.content = form.content.data
        blog.category_id = form.category.data
        db.session.commit()
        flash("Blog updated successfully.")
        return redirect(url_for('view_all_blogs'))

    return render_template('edit_blog.html', form=form)

@app.route('/delete_blog/<int:blog_id>')
@login_required
def delete_blog(blog_id):
    blog = BlogModel.query.get_or_404(blog_id)
    if blog.user_id != current_user.id:
        flash("You are not authorized to delete this blog.")
        return redirect(url_for('view_all_blogs'))
    db.session.delete(blog)
    db.session.commit()
    flash("Blog deleted successfully.")
    return redirect(url_for('view_all_blogs'))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
