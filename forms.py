from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('admin', 'Admin'), ('user', 'User')], validators=[DataRequired()])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    role = SelectField('Role', choices=[('admin', 'Admin'), ('user', 'User')], validators=[DataRequired()])
    submit = SubmitField('Login')

class CreateSubjectForm(FlaskForm):
    name = StringField('Subject Name', validators=[DataRequired(), Length(min=3, max=50)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=200)])
    submit = SubmitField('Create Subject')

class CreateChapterForm(FlaskForm):
    name = StringField('Chapter Name', validators=[DataRequired(), Length(min=3, max=50)])
    subject = SelectField('Subject', choices=[], validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=200)])
    submit = SubmitField('Create Chapter')

class CreateQuizForm(FlaskForm):
    chapter = SelectField('Chapter', choices=[], validators=[DataRequired()])
    date = StringField('Date', validators=[DataRequired()])
    time_duration = StringField('Time Duration (hh:mm)', validators=[DataRequired()])
    remarks = TextAreaField('Remarks', validators=[Length(max=200)])
    submit = SubmitField('Create Quiz')

class CreateQuestionForm(FlaskForm):
    quiz = SelectField('Quiz', choices=[], validators=[DataRequired()])
    question_statement = TextAreaField('Question', validators=[DataRequired(), Length(max=500)])
    option1 = StringField('Option 1', validators=[DataRequired(), Length(max=100)])
    option2 = StringField('Option 2', validators=[DataRequired(), Length(max=100)])
    option3 = StringField('Option 3', validators=[DataRequired(), Length(max=100)])
    option4 = StringField('Option 4', validators=[DataRequired(), Length(max=100)])
    correct_answer = SelectField('Correct Answer', choices=[('option1', 'Option 1'), ('option2', 'Option 2'), ('option3', 'Option 3'), ('option4', 'Option 4')], validators=[DataRequired()])
    submit = SubmitField('Create Question')

class QuizAttemptForm(FlaskForm):
    quiz_id = IntegerField('Quiz ID', validators=[DataRequired()])
    answers = StringField('Answers', validators=[DataRequired()])
    submit = SubmitField('Submit Quiz')
