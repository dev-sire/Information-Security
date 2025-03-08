from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from forms import LoginForm, RegistrationForm
from models import db, User, ActivityLog

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-sire'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return redirect(url_for('register'))

@app.route('/logs')
@login_required
def view_logs():
    logs = db.session.query(ActivityLog, User.username).join(User).all()
    return render_template('logs.html', logs=logs)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:  # Use hashed passwords in production
            login_user(user)
            log_activity(user.id, 'Logged In')
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)  # Use hashed passwords in production
        db.session.add(user)
        db.session.commit()
        log_activity(user.id, 'Account Created')
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.username)

@app.route('/logout')
@login_required
def logout():
    log_activity(current_user.id, 'Logged Out')
    logout_user()
    return redirect(url_for('login'))

def log_activity(user_id, action):
    activity = ActivityLog(user_id=user_id, action=action)
    db.session.add(activity)
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()