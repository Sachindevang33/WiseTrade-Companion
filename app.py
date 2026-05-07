from flask import Flask, render_template, request, redirect, url_for, session, flash
import random
import string
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'Vishwas'
db = SQLAlchemy(app)





class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(20), unique=True)
    age = db.Column(db.Integer)
    phone = db.Column(db.String(20))
    password = db.Column(db.String(100))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if (user.password == password):
            # Login successful, set user id in session
            session['user_id'] = user.id
            return redirect('/home')  # Redirect to a page showing login success
        else:
            return render_template('login.html', error="Invalid email or password. Please try again.")

    return render_template('login.html')

@app.route('/login-success')
def login_success():
    if 'user_id' in session:
        return 'Login successful!'
    else:
        return redirect('/login')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        phone = request.form['phone']
        password = request.form['password']

        # Generate random username
        email = request.form['email']

        new_user = User(name=name, email=email, age=age, phone=phone, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect('/login')

    return render_template('signup.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'user_id' in session:
        return render_template('home.html')
    else:
        return redirect('/login')



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    port = int(5000)
    app.static_folder = 'static'
    app.run(host='0.0.0.0', port=port, debug=True)   


