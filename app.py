from flask import Flask, render_template, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo

# User model simulation
users_db = {}

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password  # Remember to hash passwords in a real application

    @classmethod
    def get(cls, username):
        return users_db.get(username)

    @classmethod
    def create(cls, username, password):
        users_db[username] = cls(username, password)

# Flask-WTF Forms
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = '123123'  # Replace with a real secret key

@app.route('/')
def index():
    # If user is logged in, redirect to dashboard
    if 'username' in session:
        return redirect(url_for('dashboard'))
    # Otherwise, show the landing page
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Redirect to dashboard if user is already logged in
    if 'username' in session:
        return redirect(url_for('dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        User.create(form.username.data, form.password.data)
        # Redirect to login page after registration
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Redirect to dashboard if user is already logged in
    if 'username' in session:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get(form.username.data)
        if user and user.password == form.password.data:
            session['username'] = user.username
            # Redirect to dashboard after login
            return redirect(url_for('dashboard'))
        else:
            # In a real application, flash a message to the user
            return redirect(url_for('login'))
    return render_template('login.html', form=form)

@app.route('/dashboard')
def dashboard():
    # Ensure that the user is logged in before showing the dashboard
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    else:
        # Redirect to login page if the user is not logged in
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    # Remove 'username' from session and redirect to login
    session.pop('username', None)
    return redirect(url_for('index'))

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
