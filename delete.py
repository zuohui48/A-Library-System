from threading import local
from main import Author, Fine, Isbn, Session, engine, Member, Book, Borrow, Reservation

local_session = Session(bind = engine)

def withdraw_book(acc_num):
    book_to_delete = local_session.query(Book).filter(Book.accessionNo == acc_num).first()
    isbn = book_to_delete.isbn
    if not local_session.query(Borrow).filter(Borrow.accessionNo == acc_num).first() and not local_session.query(Reservation).filter(Reservation.accessionNo == acc_num).first():
        if local_session.query(Book).filter(Book.isbn == isbn).count() > 1:
            local_session.delete(book_to_delete)
        else:
            local_session.delete(book_to_delete)
            local_session.query(Isbn).filter(Isbn.isbn == isbn).delete(synchronize_session="fetch")
            local_session.query(Author).filter(Author.isbn == isbn).delete(synchronize_session="fetch")
    
    local_session.commit()

def membership_deletion(memid):
    mem_to_delete = local_session.query(Member).filter(Member.membershipid == memid).first()
    if not local_session.query(Borrow).filter(Borrow.membershipid == memid).first() and not local_session.query(Fine).filter(Fine.membershipid == memid).first() and not \
        local_session.query(Reservation).filter(Reservation.membershipid == memid).first():
        local_session.delete(mem_to_delete)
        local_session.commit()

#withdraw_book("asd")

