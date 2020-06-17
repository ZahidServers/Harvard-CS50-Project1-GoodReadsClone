#This Python Application is Written By Mohammed Zahid Wadiwale
import os
from flask import Flask, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import Flask, render_template, flash, redirect, request, abort, url_for, jsonify
import json
import requests

app = Flask(__name__)
app.config['DATABASE_URL'] = "postgres://nkweeotaiaocev:cd2afe545b2364432178fb4333d2f6aa12c74bd0bb1ba1804840a93cc218a23c@ec2-79-125-26-232.eu-west-1.compute.amazonaws.com:5432/daqdsbbqpv9hrd"
os.environ["DATABASE_URL"] = "postgres://nkweeotaiaocev:cd2afe545b2364432178fb4333d2f6aa12c74bd0bb1ba1804840a93cc218a23c@ec2-79-125-26-232.eu-west-1.compute.amazonaws.com:5432/daqdsbbqpv9hrd"
app.secret_key = os.urandom(24) 
# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"), pool_size=10, max_overflow=10)
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
	if not session.get('logged_in'):
		return home()
	else:
		return render_template("index.html")
@app.route("/home")
def home():
	if not session.get('logged_in'):
		return render_template("index2.html")
	else:
		return index()
@app.route("/logout")
def logout():
	if session.get('logged_in'):
		session.clear()
		return index()
@app.route("/login", methods=['POST','GET'])
def login():
	if session.get('logged_in'):
		return index()
	error = None
	if request.method == 'POST':
		email=request.form['email']
		password=request.form['password']
		logon=db.execute("SELECT * FROM bookuser WHERE email=:it AND password=:itf",{"it":email,"itf":password}).fetchone()
		if logon is None:
			error = 'Invalid Credentials. Please try again.'
		else:
			session['logged_in'] = request.form['email']
			return redirect(url_for('index'))
	return render_template('login.html', error=error)
@app.route("/registar", methods=['POST','GET'])
def registar():
	if session.get('logged_in'):
		return index()
	error = None
	if request.method == 'POST':
		email=request.form['email']
		name=request.form['name']
		password=request.form['password']
		logon2=db.execute("SELECT * FROM bookuser WHERE email=:it",{"it":email}).fetchone()
		if logon2 is not None:
			error = 'This Email Already Exist'
		else:
			db.execute("INSERT INTO bookuser (name,email,password) VALUES (:name,:email,:password)",{'name':name,'email':email,'password':password})
			db.commit()
			return render_template('login.html', message="Account Sucessfully Created Now Login")
	return render_template('registar.html', error=error)
@app.route("/search", methods=['POST','GET'])
def search():

	if request.method=='POST':
		error=None
		searchit=request.form['k']
		search=db.execute("SELECT * FROM books WHERE author LIKE '%"+searchit+"%' OR title LIKE '%"+searchit+"%' OR isbn LIKE '%"+searchit+"%'")
		if search is None:
			error="No Results Found!"
		if session.get('logged_in'):
			return render_template('search.html', error=error,search=search,string=searchit)
		else:
			return render_template('search2.html', error=error,search=search,string=searchit)
@app.route("/isbn/<string:isbn>",methods=["GET","POST"])
def book(isbn):
	chechit=db.execute("SELECT * FROM books WHERE isbn = :isbn",{"isbn":isbn}).fetchone()
	if chechit==None:
		return render_template('404.html')
	if not session.get('logged_in'):
		return login()
	error=""
	email=session.get('logged_in')
	secondreview=db.execute("SELECT * FROM reviews WHERE isbn = :isbn AND email= :email",{"email":email,"isbn":isbn}).fetchone()
	data=db.execute("SELECT * FROM books WHERE isbn = :isbn",{"isbn":isbn}).fetchone()
	res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "YdT8QcJWE6ZvnDjMKIZgA", "isbns": isbn})
	average_rating=res.json()['books'][0]['average_rating']
	work_ratings_count=res.json()['books'][0]['work_ratings_count']
	if request.method=="POST" and secondreview!=None:
		error="Sorry. You cannot add second review."
		reviews=db.execute("SELECT * FROM reviews WHERE isbn = :isbn AND email=:email",{"isbn":isbn,"email":email}).fetchall()
	elif request.method=="GET" and secondreview!=None:
		reviews=db.execute("SELECT * FROM reviews WHERE isbn = :isbn AND email=:email",{"isbn":isbn,"email":email}).fetchall()
		return render_template('book.html',data=data,email=email,error=error,reviews=reviews,average_rating=average_rating,rcounts=work_ratings_count)
	else:
		reviews=None
	if request.method=="POST" and secondreview==None:
		review=request.form.get('textarea')
		rating=request.form.get('stars')
		db.execute("INSERT INTO reviews (isbn, review, rating, email) VALUES (:a,:b,:c,:d)",{"a":isbn,"b":review,"c":rating,"d":email})
		db.commit()
		return book(isbn)
	return render_template('book.html',data=data,email=email,error=error,reviews=reviews,average_rating=average_rating,rcounts=work_ratings_count)
@app.route("/api/<string:isbn>")
def api(isbn):
	if not session.get('logged_in'):
		return login()
	data=db.execute("SELECT * FROM books WHERE isbn = :isbn",{"isbn":isbn}).fetchone()
	if data!=None:
		res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "YdT8QcJWE6ZvnDjMKIZgA", "isbns": isbn})
		average_rating=res.json()['books'][0]['average_rating']
		work_ratings_count=res.json()['books'][0]['work_ratings_count']
		x = {
		"title": data.title,
		"author": data.author,
		"year": data.year,
		"isbn": isbn,
		"review_count": work_ratings_count,
		"average_score": average_rating
		}
		api=json.dumps(x)
	else:
		return jsonify({"error":"Invalid ISBN"}),422
	return render_template("api.json",api=api)
