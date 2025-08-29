from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    TextAreaField,
    SelectField,
    IntegerField
)
from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    EqualTo,
    NumberRange,
    Optional
)
from wtforms.fields import EmailField

# 🔒 Registration Form
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=50)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message="Passwords must match.")])
    submit = SubmitField('Register')

# 🔐 Login Form
class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# 📝 Blog Form
class BlogForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    content = TextAreaField('Content', validators=[DataRequired()])
    category = SelectField('Category', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Create Blog')

# 💬 Comment + Rating Form
class CommentForm(FlaskForm):
    blog_comment = TextAreaField('Comment', validators=[DataRequired(), Length(max=500)])
    blog_rating = IntegerField('Rating (1 to 5)', validators=[DataRequired(), NumberRange(min=1, max=5)])
    submit = SubmitField('Submit')

# 🔎 Filter + Search Form
class FilterForm(FlaskForm):
    category = SelectField("Category", choices=[], coerce=int, validators=[Optional()])
    search = StringField("Search by title", validators=[Optional()])
    submit = SubmitField("Filter")
