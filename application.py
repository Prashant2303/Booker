import os
import requests

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("welcome.html")

@app.route("/user", methods=["POST"])
def user():
    username= request.form.get("username")
    password= request.form.get("password")
    if db.execute("SELECT * FROM members WHERE username=:username",{"username":username}).rowcount==1:
        return render_template("error.html", message="Username taken")
    db.execute("INSERT INTO members (username, password) VALUES (:username, :password)",
               {"username":username, "password":password})
    db.commit()
    return render_template("user.html", username=username)

@app.route("/login", methods=["POST"])
def login():
    login.username= request.form.get("usernamel")
    password= request.form.get("passwordl")
    if db.execute("SELECT * FROM members WHERE  username=:username AND password=:password", {"username":login.username, "password":password}).rowcount == 0:
        return render_template("error.html", message="User not found")
    return render_template("user.html", username=login.username)

@app.route("/results", methods=["POST"])
def results():
    query=request.form.get("query")
    if db.execute("SELECT * FROM books WHERE  title LIKE :query OR isbn LIKE :query OR author LIKE :query", {"query": "%{}%".format(query)}).rowcount == 0:
        return render_template("error.html", message="No Book Found")
    books = db.execute("SELECT * FROM books WHERE title LIKE :query OR isbn LIKE :query OR author LIKE :query", {"query": "%{}%".format(query)})
    return render_template("results.html", books = books)

@app.route("/books/<book_num>")
def book(book_num):
    book=db.execute("SELECT * FROM books WHERE isbn=:isbn",{"isbn":book_num})
    res=requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "PGKpdo40NGG3UYKK15b1rQ", "isbns":book_num})
    data=res.json()
    rating = data["books"][0]["average_rating"]
    num = data["books"][0]["work_ratings_count"]
    reviews = db.execute("SELECT * FROM reviews WHERE isbn=:isbn",{"isbn":book_num})  
    return render_template("book.html",book=book, reviews=reviews, rating=rating, count=num)

def addreview():
    review = request.form.get("review")
    db.execute("INSERT INTO reviews (review, user, isbn) VALUES (:review, :user, :isbn)",{"review":review, "user":login.username, "isbn":book_num})

    
