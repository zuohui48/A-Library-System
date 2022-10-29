from threading import local
from turtle import title
from main import Member, Session, engine, Book, Borrow, Reservation, Isbn, Fine, Author
from sqlalchemy import or_

local_session = Session(bind = engine)

#query all users
#users = local_session.query(User).all() #[:x] to keep it to first x rows


""" def book_search_by_title(title_input):
    return local_session.query(Book).filter(Book.title.contains(title_input)).all()

def book_search_by_isbn(isbn_input):
    return local_session.query(Isbn).filter(Isbn.isbn.contains(isbn_input)).all()

def book_search_by_publisher(publisher_input):
    return local_session.query(Isbn).filter(Isbn.publisher.contains(publisher_input)).all()

def book_search_by_publication_year(year_input):
    return local_session.query(Isbn).filter(Isbn.publisherYear.contains(year_input)).all() """

def book_search_author(word_input):
    if " " in word_input:
        return []
    search = "%{}%".format(word_input)
    result_list = local_session.query(Author).filter(Author.authorname.like(search)).all()
    result = []
    isbn_list = []
    for author in result_list:
        isbn_list.append(author.isbn)
        if author:
            book_isbn = local_session.query(Isbn).filter(Isbn.isbn == author.isbn).first()
            book_book = local_session.query(Book).filter(author.isbn == Book.isbn).first()
            if book_isbn and book_book:
                result.append([book_book.accessionNo, book_isbn.title, author.authorname, author.isbn, book_isbn.publisher, book_isbn.publisherYear])
    return result

def book_search_title(word_input):
    if " " in word_input:
        return []
    search = "{} %".format(word_input)
    search1 = "% {} %".format(word_input)
    search2 = "% {}".format(word_input)
    search3 = "{}".format(word_input)

    result_list = local_session.query(Isbn).filter(or_(Isbn.title.startswith(search),Isbn.title.contains(search1),Isbn.title.endswith(search2),Isbn.title.like(search3))).all()
    result = []
    for isbn in result_list:
        if isbn:
            book_book = local_session.query(Book).filter(isbn.isbn == Book.isbn).first()
            book_authors = local_session.query(Author).filter(Author.isbn == book_book.isbn).all()
            authorslist = []
            for author in book_authors:
                authorslist.append(author.authorname)
            result.append([book_book.accessionNo, isbn.title, authorslist, isbn.isbn, isbn.publisher, isbn.publisherYear])
    return result

def book_search_isbn(word_input):
    if " " in word_input:
        return []
    result_list = local_session.query(Isbn).filter(Isbn.isbn == word_input).all()
    result = []
    for book in result_list:
        if book:
            book_book = local_session.query(Book).filter(book.isbn == Book.isbn).first()
            book_authors = local_session.query(Author).filter(Author.isbn == book.isbn).all()
            for author in book_authors:
                result.append([book_book.accessionNo, book.title, author.authorname, book.isbn, book.publisher, book.publisherYear])
    return result   

def book_search_publisher(word_input):
    if " " in word_input:
        return []
    search = "%{}%".format(word_input)
    result_list = local_session.query(Isbn).filter(Isbn.publisher.like(search)).all()
    result = []
    for book in result_list:
        if book:
            book_book = local_session.query(Book).filter(book.isbn == Book.isbn).first()
            book_authors = local_session.query(Author).filter(Author.isbn == book.isbn).all()
            for author in book_authors:
                result.append([book_book.accessionNo, book.title, author.authorname, book.isbn, book.publisher, book.publisherYear])
    return result

def book_search_publisheryear(word_input):
    if " " in word_input:
        return []
    search = "%{}%".format(word_input)
    result_list = local_session.query(Isbn).filter(Isbn.publisherYear.like(search)).all()
    result = []
    for book in result_list:
        if book:
            book_book = local_session.query(Book).filter(book.isbn == Book.isbn).first()
            book_authors = local_session.query(Author).filter(Author.isbn == book.isbn).all()
            for author in book_authors:
                result.append([book_book.accessionNo, book.title, author.authorname, book.isbn, book.publisher, book.publisherYear])
    return result

def display_books_on_loan():
    borrow_list = []
    for x in local_session.query(Borrow).all():
        book = local_session.query(Book).filter(Book.accessionNo == x.accessionNo).first()
        borrow_list.append(book)
    result = []
    for borrow in borrow_list:
        if borrow:
            borrow_isbn = local_session.query(Isbn).filter(Isbn.isbn == borrow.isbn).first()
            borrow_authors = local_session.query(Author).filter(Author.isbn == borrow.isbn).all()
            for author in borrow_authors:
                result.append([borrow.accessionNo, borrow_isbn.title, author.authorname, borrow_isbn.isbn, borrow_isbn.publisher, borrow_isbn.publisherYear])
    return result

def display_books_on_reservation():
    reservation_list = local_session.query(Reservation).all()
    result = []
    for reserve in reservation_list:
        if reserve:
            reserve_book = local_session.query(Book).filter(Book.accessionNo == reserve.accessionNo).first()
            if reserve_book:
                reserve_isbn = local_session.query(Isbn).filter(Isbn.isbn == reserve_book.isbn).first()
                if reserve_isbn:
                    reserve_member = local_session.query(Member).filter(Member.membershipid == reserve.membershipid).first()
                    if reserve_member:
                        result.append([reserve.accessionNo, reserve_isbn.title, reserve_member.membershipid, reserve_member.name])
    return result

def display_fines():
    fine_list = local_session.query(Fine).all()
    result = []
    for member in fine_list:
        if member and member.paymentDate == None:
            member_entity = local_session.query(Member).filter(Member.membershipid == member.membershipid).first()
            if member_entity:
                result.append([member_entity.membershipid, member_entity.name, member_entity.faculty, member_entity.phonenumber, member_entity.email])
    return result


def display_member_loans(member_id):
    borrow_list = []
    for x in local_session.query(Borrow).filter(Borrow.membershipid == member_id).all():
        book = local_session.query(Book).filter(Book.accessionNo == x.accessionNo).first()
        borrow_list.append(book)
    result = []
    for borrow in borrow_list:
        if borrow:
            borrow_isbn = local_session.query(Isbn).filter(Isbn.isbn == borrow.isbn).first()
            borrow_authors = local_session.query(Author).filter(Author.isbn == borrow.isbn).all()
            for author in borrow_authors:
                result.append([borrow.accessionNo, borrow_isbn.title, author.authorname, borrow_isbn.isbn, borrow_isbn.publisher, borrow_isbn.publisherYear])
    return result
