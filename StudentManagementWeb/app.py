import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root2:Nik1701@localhost/students'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.urandom(24)

db = SQLAlchemy(app)

def is_logged_in():
    return 'username' in session

@app.route('/')
def index():
    if is_logged_in():
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    if username == admin_credentials['username'] and check_password_hash(admin_credentials['password_hash'], password):
        session['username'] = username
        flash('You are now logged in', 'success')
        return redirect(url_for('dashboard'))
    else:
        flash('Invalid login', 'error')
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if not is_logged_in():
        return redirect(url_for('index'))

    with app.app_context():
        students = Student.query.all()

    return render_template('dashboard.html', students=students, is_user_logged_in=is_logged_in())


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(15))
    email = db.Column(db.String(50), unique=True, nullable=False)
    address = db.Column(db.String(100))

admin_credentials = {'username': 'admin', 'password_hash': generate_password_hash('admin')}

def is_logged_in():
    return 'username' in session

@app.route('/add_student_form')
def add_student_form():
    if not is_logged_in():
        return redirect(url_for('index'))
    return render_template('add_student_form.html')

@app.route('/add_student', methods=['POST'])
def add_student():
    if not is_logged_in():
        return redirect(url_for('index'))

    with app.app_context():
        new_student = Student(
            name=request.form['name'],
            phone=request.form['phone'],
            email=request.form['email'],
            address=request.form['address']
        )

        db.session.add(new_student)
        db.session.commit()

        flash('Student added successfully', 'success')
        return redirect(url_for('dashboard'))

@app.route('/update_student_form/<int:student_id>')
def update_student_form(student_id):
    if not is_logged_in():
        return redirect(url_for('index'))

    with app.app_context():
        student = Student.query.get(student_id)

    if student:
        return render_template('update_student_form.html', student=student)
    else:
        flash('Student not found', 'error')
        return redirect(url_for('dashboard'))

@app.route('/update_student/<int:student_id>', methods=['POST'])
def update_student(student_id):
    if not is_logged_in():
        return redirect(url_for('index'))

    with app.app_context():
        student = Student.query.get(student_id)

        if student:
            student.name = request.form['name']
            student.phone = request.form['phone']
            student.email = request.form['email']
            student.address = request.form['address']
            db.session.commit()
            flash('Student updated successfully', 'success')
        else:
            flash('Student not found', 'error')

        return redirect(url_for('dashboard'))

@app.route('/remove_student/<int:student_id>')
def remove_student(student_id):
    if not is_logged_in():
        return redirect(url_for('index'))

    with app.app_context():
        student = Student.query.get(student_id)

        if student:
            db.session.delete(student)
            db.session.commit()
            flash('Student removed successfully', 'success')
        else:
            flash('Student not found', 'error')

        return redirect(url_for('dashboard'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)