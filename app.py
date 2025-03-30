from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from forms import (
    RegistrationForm, LoginForm, CreateSubjectForm, 
    CreateChapterForm, CreateQuizForm, CreateQuestionForm, QuizAttemptForm
)
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = '9b26c53c7f8fb3b5ef4f5c3ecad4c44c'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image}')"

# Subject Model
class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    quizzes = db.relationship('Quiz', backref='subject', lazy=True)

    def __repr__(self):
        return f"Subject('{self.name}')"

# Quiz Model
class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    questions = db.relationship('Question', backref='quiz', lazy=True)

    def __repr__(self):
        return f"Quiz('{self.title}', Subject ID: {self.subject_id})"

# Question Model
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    option_a = db.Column(db.String(200), nullable=False)
    option_b = db.Column(db.String(200), nullable=False)
    option_c = db.Column(db.String(200), nullable=False)
    option_d = db.Column(db.String(200), nullable=False)
    correct_answer = db.Column(db.String(1), nullable=False)

    def __repr__(self):
        return f"Question('{self.text}', Quiz ID: {self.quiz_id})"

# Score Model
class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Score(User ID: {self.user_id}, Quiz ID: {self.quiz_id}, Score: {self.score})"

# Routes
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, is_admin=form.is_admin.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            session['user_id'] = user.id
            session['is_admin'] = user.is_admin
            flash('You have been logged in!', 'success')
            return redirect(url_for('admin_dashboard' if user.is_admin else 'user_dashboard', id=user.id))
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/admin/<int:id>")
def admin_dashboard(id):
    user = User.query.get_or_404(id)
    if not user.is_admin:
        flash("Access Denied!", "danger")
        return redirect(url_for('home'))
    return render_template('admin_dashboard.html', user=user)

@app.route("/user/<int:id>")
def user_dashboard(id):
    user = User.query.get_or_404(id)
    return render_template('user_dashboard.html', user=user)

@app.route("/create_subject", methods=['GET', 'POST'])
def create_subject():
    form = CreateSubjectForm()
    if form.validate_on_submit():
        subject = Subject(name=form.name.data, description=form.description.data)
        db.session.add(subject)
        db.session.commit()
        flash(f'Subject "{form.name.data}" created successfully!', 'success')
        return redirect(url_for('admin_dashboard', id=session.get('user_id')))
    return render_template('create_subject.html', title="Create Subject", form=form)

@app.route("/manage_subjects")
def manage_subjects():
    subjects = Subject.query.all()
    return render_template('manage_subjects.html', subjects=subjects)

@app.route("/create_quiz", methods=['GET', 'POST'])
def create_quiz():
    form = CreateQuizForm()
    if form.validate_on_submit():
        quiz = Quiz(title=form.title.data, subject_id=form.subject.data.id)
        db.session.add(quiz)
        db.session.commit()
        flash('Quiz created successfully!', 'success')
        return redirect(url_for('admin_dashboard', id=session.get('user_id')))
    return render_template('create_quiz.html', title="Create Quiz", form=form)

@app.route("/attempt_quiz", methods=['GET', 'POST'])
def attempt_quiz():
    form = QuizAttemptForm()
    if form.validate_on_submit():
        flash('Quiz submitted successfully!', 'success')
        return redirect(url_for('user_dashboard', id=session.get('user_id')))
    return render_template('attempt_quiz.html', title="Attempt Quiz", form=form)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
