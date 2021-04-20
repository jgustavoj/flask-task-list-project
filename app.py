from flask import Flask, flash, redirect, render_template, url_for, request
from models import db, Todo, User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import datetime as dt

# Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = '\x14B~^\x07\xe1\x197\xda\x18\xa6[[\x05\x03QVg\xce%\xb2<\x80\xa4\x00'
app.config['DEBUG'] = True

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
db.init_app(app)

#Authorization 
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


"""
Authorization Flask Login

"""
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Index Login to all users
@app.route('/')
def index():
    return render_template('login.html', user=current_user)


# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email') 
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Log in successful!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('all_todos'))
            else:
                flash('Incorrect password, please try again!', category='error')
        else:
            flash('Email does not exists.', category='error') 


    return render_template('login.html', user=current_user)


# Signup route
@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email') 
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        password1 = request.form.get('password1') 
        password2 = request.form.get('password2') 
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exist.', category='error')    
        elif password1 != password2:
            flash('Passwords do not match, please try again', category='error')
            return redirect(url_for('signup'))
        else:
            new_user = User(first_name=first_name, last_name=last_name, email=email, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()           
            flash('Success! Account created. Please login.', category='success')
            return redirect(url_for('login'))

    return render_template('signup.html', user=current_user)


# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

"""
Task Routes with user relationship 

"""


# All task with user route
@app.route('/todos')
@login_required
def all_todos():
    if current_user.is_authenticated:
        complete_task = Todo.query.filter_by(complete=True).all()
        tasks = Todo.query.all()
        return render_template('index.html', tasks=tasks, complete_task = complete_task, user=current_user)

        
# Add task with user route
@app.route('/add', methods=['POST'])
@login_required
def add_task():
        user_id = current_user.id
        task = request.form.get('content')
        due_date_iso = request.form.get('dueDate')
        if due_date_iso == '':
            due_date_iso = dt.datetime.now().isoformat(' ')
        due_date = dt.datetime.fromisoformat(due_date_iso)

        new_task = Todo(task=task, due_date=due_date, user_id=user_id)
        if task == "":
            flash('Please enter a task', category='error')
            redirect('/')
        else:
            db.session.add(new_task)
            db.session.commit()
        return redirect(url_for('all_todos'))


# Update task with user route 
@app.route('/update/<int:id>', methods=['POST', 'GET'])
@login_required
def update_task(id):
    update_id = Todo.query.get_or_404(id)
    if request.method == 'POST':
        update_id.task = request.form['content']
        if update_id.user_id == current_user.id:
            db.session.commit()
            return redirect(url_for('all_todos'))
          
    else:
        return render_template('update.html', update_id=update_id, user=current_user)


# Delete task route
@app.route('/delete/<int:id>')
@login_required
def delete_task(id):
    task_delete = Todo.query.get_or_404(id)
    if task_delete:
        db.session.delete(task_delete)
        db.session.commit()
        return redirect(url_for('all_todos'))


# Completed task route
@app.route('/complete/<int:id>', methods=['GET'])
@login_required
def completed_task(id):
    todo = Todo.query.get_or_404(id)
    todo.complete = True
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for('all_todos'))


if __name__ == "__main__":
    app.run(port=3000)

