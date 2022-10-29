from multiprocessing import connection
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, String, DateTime, Integer, create_engine
from sqlalchemy.sql.sqltypes import Date
from datetime import datetime, timedelta
import pymysql


pymysql.install_as_MySQLdb()

# BASE_DIR = os.path.dirname(os.path.realpath(__file__))

# connection_string = "mysql+pymysql:///" + os.path.join(BASE_DIR, "Library.db")
password = input("Please enter root password: ")
connection_string = f'mysql+pymysql://root:{password}@localhost/Library'

Base = declarative_base()

engine = create_engine(connection_string, echo = True)
# engine = create_engine('mysql://root:password123@localhost')

Session = sessionmaker()

"""
class User
    id int
    username str
    email str
    date_created datetime

"""


""" class User(Base):
    __tablename__ = "Users"
    id = Column(Integer(), primary_key = True)
    username = Column(String(25), nullable = False, unique = True)
    email = Column(String(25), unique = True, nullable = False)
    date_created = Column(DateTime(), default = datetime.utcnow)

    def __repr__(self):
        return f"<User username = {self.username} email = {self.email}>" """

class Member(Base):
    __tablename__ = "Member"
    membershipid = Column(String(7), primary_key = True, nullable = False, unique = True)
    name = Column(String(25), nullable = False)
    email = Column(String(25), nullable = False)
    faculty = Column(String(25), nullable = False)
    phonenumber = Column(Integer(), nullable = False)
    # date_created = Column(DateTime(), default = datetime.utcnow)

    #def __repr__(self):
    #    return f"<User username = {self.username} email = {self.email}>"

class Book(Base):
    __tablename__ = "Book"
    accessionNo = Column(String(3), primary_key = True, nullable = False, unique = True)
    # publisherYear = Column(Integer(), nullable = False)
    # publisher = Column(String(100), nullable = False)
    # title = Column(String(100), nullable = False)
    isbn = Column(String(25), nullable = False)


class Borrow(Base):
    __tablename__ = "Borrow"
    accessionNo = Column(String(3), primary_key = True, nullable = False, unique = True)
    membershipid = Column(String(7), nullable = False, unique = True)
    returndate = Column(DateTime(), default = datetime.today() + timedelta(days=14))

class Reservation(Base):
    __tablename__ = "Reservation"
    accessionNo = Column(String(3), primary_key = True, nullable = False, unique = True)
    membershipid = Column(String(7), nullable = False, unique = True)
    reservedate = Column(DateTime(), default = datetime.today())

class Author(Base):
    __tablename__ = "Author"
    isbn = Column(String(25), nullable = False, primary_key = False)
    authorname = Column(String(100), primary_key = True, nullable = False)

class Isbn(Base):
    __tablename__ = "Isbn"
    isbn = Column(String(25), nullable = False, unique = True, primary_key=True)
    publisherYear = Column(Integer(), nullable = False)
    publisher = Column(String(100), nullable = False)
    title = Column(String(100), nullable = False)

class Fine(Base):
    __tablename__ = "Fine"
    membershipid = Column(String(7), primary_key = True, nullable = False)
    paymentDate = Column(DateTime(), nullable = True, default = None)
    paymentAmount = Column(Integer(), nullable = False)


