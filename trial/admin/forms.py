from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FloatField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, EqualTo, Length, Email, ValidationError
from trial.models import User

#Create Registration Form
class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    #Check to see if username already exists
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists. Please choose a different one.')  


    #Check to see if email already exists
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already exists. Please choose a different one.')


#Create Blog Post Form
class BlogPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    blog_content = TextAreaField('Content', validators=[DataRequired()])
    picture = FileField('Upload Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'])]) 
    submit = SubmitField('Post')

class ContractDetailsForm(FlaskForm):
    name_of_contract = StringField('Name of Contract', validators=[DataRequired()])
    length = FloatField('Length (Km)', validators=[DataRequired()])
    lot = StringField('Lot', validators=[DataRequired()])
    contract_sum = StringField('Contract Sum', validators=[DataRequired()])
    contractor = StringField('Contractor', validators=[DataRequired()])
    date_commenced = StringField('Date of Commence', validators=[DataRequired()])
    date_completed = StringField('Date of Completion', validators=[DataRequired()])
    video_title = StringField('Video Title', validators=[DataRequired()])
    video_link = StringField('Video Link', validators=[DataRequired()], render_kw={'placeholder':"https://www.youtube.com/watch?v="})
    video_description = TextAreaField('Video Description')
    submit = SubmitField('Submit')