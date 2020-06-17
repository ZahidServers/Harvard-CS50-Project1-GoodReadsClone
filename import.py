#This Python Code is Written By Mohammed Zahid Wadiwale
import os
import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
os.environ["DATABASE_URL"] = "postgres://nkweeotaiaocev:cd2afe545b2364432178fb4333d2f6aa12c74bd0bb1ba1804840a93cc218a23c@ec2-79-125-26-232.eu-west-1.compute.amazonaws.com:5432/daqdsbbqpv9hrd"
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")
engine= create_engine(os.getenv("DATABASE_URL"))
db =scoped_session(sessionmaker(bind=engine))
def main():
    print("Hello Creating DB")
    db.execute("CREATE TABLE bookuser (id SERIAL PRIMARY KEY, email TEXT NOT NULL, password TEXT NOT NULL)")
    db.execute("CREATE TABLE reviews (isbn TEXT NOT NULL,review TEXT NOT NULL, rating INTEGER NOT NULL,email TEXT NOT NULL)")
    db.execute("CREATE TABLE books (isbn TEXT PRIMARY KEY,title TEXT NOT NULL,author TEXT NOT NULL,year TEXT NOT NULL)")
    f=open("books.csv")
    reader=csv.reader(f)
    for isbn,title,author,year in reader:
        if year == "year":
            print('skipped first line')
        else:    
            db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:a,:b,:c,:d)",{"a":isbn,"b":title,"c":author,"d":year})
    print("done")            
    db.commit()
main()
