import csv
import os


from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
def main():
    db.execute("CREATE TABLE users (id SERIAL PRIMARY KEY, username VARCHAR NOT NULL, password VARCHAR NOT NULL);")
    db.execute("CREATE TABLE reviews (id SERIAL PRIMARY KEY, context TEXT NOT NULL, score DECIMAL(2,1) NOT NULL, isbn VARCHAR REFERENCES books , writer_id INTEGER REFERENCES users );")
    db.commit()


if __name__ == "__main__":
    main()
