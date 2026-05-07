from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# initialize the app with the extension
db.init_app(app)

"""
    The 'topic' class represents a topic in the database.
    It has an 'id' as the primary key, a 'title' that is unique and cannot be null,
    and a 'description' that can be null.
"""
class Topic(db.Model):
    # Set up the primary key and the title column
    id = db.Column(db.Integer, primary_key=True)
    title  = db.Column(db.String, unique = True, nullable = False)
    # Set up the description column
    description = db.Column(db.String)


class Comment(db.Model):
    # The 'id' column is an Integer type and is the primary key for this table
    id = db.Column(db.Integer, primary_key=True)
    # The 'text' column is a String type and is unique and not nullable
    text  = db.Column(db.String, unique=True, nullable=False)
    # The 'topicID' column is a String type and is used to link comments to a specific topic
    topicID = db.Column(db.String)  # Changed attribute name to match the database column name



with app.app_context():
    db.create_all()
    
@app.route("/community", methods=["GET", "POST"])
def home():
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

@app.route("/community/topic/<int:id>", methods=["GET", "POST"])
def topic(id):
    if request.method == "POST":
        # Add a new comment to the topic
        comment = Comment(
            text=request.form["comment"],
            topicID=id
        )
        db.session.add(comment)
        db.session.commit()
    topic = db.get_or_404(Topic, id)
    comments = Comment.query.filter_by(topicID = id)
    CommentsCount = len(list(comments))
    # for comment in comments:
    #     print(comment)
    return render_template("topic.html", topic = topic, comments = comments, CommentsCount = CommentsCount)

app.run(debug=True)






