from main import Member, Session, engine, Book, Borrow, Reservation, Isbn, Fine, Author
from datetime import datetime, date, timedelta


local_session = Session(bind = engine)

# to add single member
def membership_creation(member, name ,email,faculty,hp):
    new_member = Member(membershipid = member, name = name, email = email, faculty = faculty, phonenumber = hp)
    local_session.add(new_member)
    local_session.commit()

def book_acquisition(acc_no, isbn, authors, publication_year, publisher, title):
    authorslist = authors.split(",")
    new_book = Book(accessionNo = acc_no, isbn = isbn)
    new_isbn = Isbn(isbn = isbn, publisherYear = publication_year, publisher = publisher, title = title)
    if not local_session.query(Book).filter(Book.accessionNo == acc_no).first():
        local_session.add(new_book)
    if not local_session.query(Isbn).filter(Isbn.isbn == isbn).first():
        local_session.add(new_isbn)
        for author in authorslist:
            new_author = Author(isbn = isbn, authorname = author)
            local_session.add(new_author)
    local_session.commit()


def book_reservation(acc_no, member, reservedate):
    new_reservation = Reservation(accessionNo = acc_no, membershipid = member, reservedate = reservedate)
    if not local_session.query(Reservation).filter(Reservation.accessionNo == acc_no).first() and not local_session.query(Fine).filter(Fine.membershipid == member).first() and \
        local_session.query(Reservation).filter(Reservation.membershipid == member).count() <= 1:
        local_session.add(new_reservation)
        local_session.commit()

def borrow_book(acc_num, member):
    new_borrow = Borrow(accessionNo = acc_num, membershipid = member)
    if not local_session.query(Borrow).filter(Borrow.accessionNo == acc_num).first() and not local_session.query(Reservation).filter(Reservation.accessionNo == acc_num).first() \
    and not local_session.query(Fine).filter(Fine.membershipid == member).first() and local_session.query(Borrow).filter(Borrow.membershipid == member).count() <= 1:  
        local_session.add(new_borrow)
        local_session.commit()

def return_book(acc_num, memid, returnDate):
    old_book = local_session.query(Borrow).filter(Borrow.accessionNo == acc_num).first()
    returndate = datetime.strptime(returnDate, "%Y-%m-%d").date()
    if returndate > old_book.returndate:
        if local_session.query(Fine).filter(Fine.membershipid == memid).first():
            new_fine = returndate - old_book.returndate
            mem = local_session.query(Fine).filter(Fine.membershipid == memid).first()
            mem.paymentAmount += new_fine.days
        elif not local_session.query(Fine).filter(Fine.membershipid == memid).first():
            new_fine = Fine(membershipid = memid, paymentAmount = (returndate - old_book.returndate).days)
            local_session.add(new_fine)
    local_session.delete(old_book)
    local_session.commit() 

def reservation_cancellation(acc_num, memid, canceldate):
    if local_session.query(Reservation).filter(Reservation.membershipid == memid, Reservation.accessionNo == acc_num).first() \
        and local_session.query(Borrow).filter(Borrow.accessionNo == acc_num):
        to_delete = local_session.query(Reservation).filter(Reservation.membershipid == memid, Reservation.accessionNo == acc_num).first()
        local_session.delete(to_delete)
        local_session.commit()



def fine_payment(memid, paymentdate, amount):
    mem = local_session.query(Fine).filter(Fine.membershipid == memid).first()
    if mem and mem.paymentAmount == amount:
        mem.paymentDate = paymentdate
        local_session.commit()
            
            
        



#membership_creation("A100", "Ryu", "hrhr", "science", 81234567)
#borrow_book("A03", "A100")
#borrow_book("A01", "A100")
#return_book("A03", "A100", "2022-03-29")
#book_acquisition("122", 123, "asd,aasd,dksk", 123, "askd", "asddas")
#book_reservation("A04", "A10", date.today())
#reservation_cancellation("A04", "A10")
#fine_payment("A111", date.today(), 12)

# to add list of users
""" users = [
    {
        "username" : "jerry",
        "email" : "jerry@company.com"
    },
    {
        "username" : "jordan",
        "email" : "jordan@company.com"
    },{
        "username" : "james",
        "email" : "james@company.com"
    },{
        "username" : "jane",
        "email" : "jane@company.com"
    },{
        "username" : "john",
        "email" : "john@company.com"
    },
] """

""" for u in users:
    new_user = User(username = u["username"], email = u["email"])
    local_session.add(new_user)
    local_session.commit()
    print(f"Added {new_user}")     """

