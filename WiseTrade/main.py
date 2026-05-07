from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'Vishwas'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(20), unique=True)
    age = db.Column(db.Integer)
    phone = db.Column(db.String(20))
    password = db.Column(db.String(100))

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, unique=True, nullable=False)
    topicID = db.Column(db.String)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect('/home')
        else:
            return render_template('login.html', error="Invalid email or password. Please try again.")
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        phone = request.form['phone']
        password = request.form['password']
        email = request.form['email']
        new_user = User(name=name, email=email, age=age, phone=phone, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')
    return render_template('signup.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'user_id' in session:
        if request.method == "POST":
            topic = Topic(
                title=request.form["title"],
                description=request.form["description"],
            )
            db.session.add(topic)
            db.session.commit()
        topics = Topic.query.all()
        return render_template('index.html', topics=topics)
    else:
        return redirect('/login')
    
@app.route("/community", methods=["GET", "POST"])
def community():
    if request.method == "POST":
        # Add a new topic
        topic = Topic(
            title=request.form["title"],
            description=request.form["description"],
        )
        db.session.add(topic)
        db.session.commit()

    topics = db.session.execute(db.select(Topic)).scalars()
    # for topic in topics:
    #     print(topic.id, topic.title, topic.description)
    return render_template('index.html', topics = topics)

@app.route('/topic/<int:id>', methods=['GET', 'POST'])
def topic(id):
    if request.method == "POST":
        comment = Comment(
            text=request.form["comment"],
            topicID=id
        )
        db.session.add(comment)
        db.session.commit()
    topic = Topic.query.get_or_404(id)
    comments = Comment.query.filter_by(topicID=id).all()
    CommentsCount = len(comments)
    return render_template("topic.html", topic=topic, comments=comments, CommentsCount=CommentsCount)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
