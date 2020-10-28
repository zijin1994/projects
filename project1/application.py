import os
#import requests to use api
import requests
#import
from flask import Flask, session, render_template, jsonify, request
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
    return render_template("index.html")

#try to register and return error when there is a existing same user name and success if register completed.
@app.route("/register", methods=["POST"])
def register():
    n = request.form.get("username")
    pswd = request.form.get("password")
    #check if the username has been used.
    if db.execute("SELECT * FROM users WHERE username = :username", {"username": n}).rowcount != 0:
        return render_template("error.html", message="That username has already been used!")
    db.execute("INSERT INTO users (username, password) VALUES (:username, :password)",
            {"username": n, "password": pswd})
    db.commit()
    return render_template("success.html", message="You have been registered!")

#if user has an account, jump to this following login page.
@app.route("/loginpage")
def loginpage():
    return render_template("loginpage.html")

#after user submit a login request, process all the info.
@app.route("/loginpage/login", methods=["POST"])
def login():
    nr = request.form.get("usn")
    pswdr = request.form.get("psw")
    #check if the user entered the right username or password.
    user = db.execute("SELECT * FROM users WHERE (username = :username) AND (password = :password)", {"username": nr , "password": pswdr}).fetchone()
    if user == None:
        return render_template("error.html", message="You have entered wrong username or password!")
    session["user_id"] = user.id
    return render_template("login.html", user = user, login_session=session["user_id"])

#after user's input, process and search.
@app.route("/loginpage/login/searching", methods=["POST", "GET"])
def searching():#test
    if session["user_id"] == None:
        return render_template("error.html", message="You need to login to search!")
    s = request.form.get("search_input")
    results = db.execute("SELECT * FROM books WHERE isbn LIKE :isbn OR title LIKE :title OR author LIKE :author", {"isbn": f"%{s}%", "title": f"%{s}%", "author": f"%{s}%"}).fetchall()
    if len(results) == 0:
        return render_template("error.html", message="Sorry, there is no such book!")
    return render_template("results.html", results = results, login_session=session["user_id"])

#after click on book, goes to that specific book page and get the book info and all the reivews about that book.
@app.route("/loginpage/login/searching/<string:book_id>")
def book_page(book_id):
    if session["user_id"] == None:
        return render_template("error.html", message="You need to login to see the details of this book!")

    #request api data.
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "oShQOn2nt52TEQEVSbpZA", "isbns": book_id})
    resp = res.json()
    rating_count = resp["books"][0]["work_ratings_count"]
    average = resp["books"][0]["average_rating"]

    #get the book and its relating reviews.
    book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": book_id}).fetchone()
    book_reviews = db.execute("SELECT context, score FROM reviews WHERE isbn = :isbn", {"isbn": book_id}).fetchall()
    return render_template("bookpage.html", book = book, book_reviews = book_reviews, rating_count = rating_count, average = average, login_session=session["user_id"])

#after submit review, pass in book isbn, and the login_session which is unique user_id and process the request.
@app.route("/loginpage/login/searching/<string:book_id>/review_submit", methods=["POST"])
def review_submit(book_id):
    if session["user_id"] ==None:
        return render_template("error.html", message="You need to login to submit a review!")
    ctx = request.form.get("context")
    r = request.form.get("score")
    if db.execute("SELECT * FROM reviews WHERE isbn = :isbn AND writer_id = :writer_id", {"isbn": book_id, "writer_id": session["user_id"]}).rowcount != 0:
        return render_template("error.html", message="Sorry, you have already written a review for this book in the past!")
    db.execute("INSERT INTO reviews (context, score, isbn, writer_id) VALUES (:context, :score, :isbn, :writer_id)",
            {"context": ctx, "score": r, "isbn": book_id, "writer_id": session["user_id"]})
    db.commit()
    return render_template("success.html", message="You have successfully uploaded a review!")

#sign out.
@app.route("/logout")
def logout():
    #if user not login, then there is an error and website does not perform logout.
    if session["user_id"] == None:
        return render_template("error.html", message="You cannot logout when you are not even logged in!")
    session["user_id"] = None
    return render_template("success.html", message="You have successfully logged out!")

#own api.
@app.route("/api/<string:isbn>", methods=["GET"])
def own_api(isbn):
    book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    if book == None:
        return jsonify({"error": "Invalid isbn number"}), 404

    rc = db.execute("SELECT COUNT(*) FROM reviews WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    av = db.execute("SELECT AVG(score) FROM reviews WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    #since decimal is not serializable, convert to float.
    av = float(av[0])

    return jsonify({

    "title": book.title,
    "author": book.author,
    "year": book.year,
    "isbn": book.isbn,
    "review_count": rc[0],
    "average_score": av
})
