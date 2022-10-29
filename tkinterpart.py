from sre_constants import SUCCESS
from threading import local
from tkinter import *
from tkinter import ttk
import create_users, delete, update_file, query_display
from datetime import date, timedelta
from main import Member, Session, engine, Book, Borrow, Reservation, Isbn, Fine, Author
from query_display import display_books_on_loan, display_books_on_reservation, display_fines, display_member_loans
from datetime import datetime

local_session = Session(bind = engine)

def membershipbutton():
    membership = Tk()
    membership.title("Membership")
    membership.geometry('900x600')
    label = Label(membership, text = "Select one of the Options below:",
                  font=("Arial", 15), relief = RIDGE, padx = 50, pady = 30).pack()
    
    createmembershipbtn = Button(membership, text="Create New Membership", command = membershipcreationbutton)
    createmembershipbtn.pack(pady = 15)

    deletemembershipbtn = Button(membership, text="Delete Membership", command = memberdeletionbutton)
    deletemembershipbtn.pack(pady = 15)

    updatemembershipbtn = Button(membership, text="Update Membership", command = updatememberbutton)
    updatemembershipbtn.pack(pady = 15)

    backtomainbtn = Button(membership, text="Back to Main Menu", command = membership.destroy)
    backtomainbtn.pack(pady = 15)
    
    membership.mainloop()

def membershipcreationbutton():
    membercreation = Tk()
    membercreation.title("Create Membership")
    membercreation.geometry('900x600')
    label = Label(membercreation, text = "To create Member, Please Enter Required Information Below:",
                  font=("Arial", 15), relief = RIDGE, padx = 50, pady = 30).grid(row=0, column = 1, columnspan = 2)

    def membercreatebutton():
        #check if member alr exist or if there is missing fields (DONE)
        check_member = Session(bind=engine).query(Member).filter(Member.membershipid == memidentry.get()).first()
        if check_member or not memidentry.get() or not nameentry.get() or not facultyentry.get() or not phonenumentry.get() or not emailentry.get():
            error = Tk()
            error.geometry('500x300')
            error.configure(background='red')

            label = Label(error, text = "Error!", font=("Arial", 25), padx = 50, pady = 30,
                          bg = "red", fg = "yellow").pack()
            label2 = Label(error, text = "Member already exist; Missing or Incomplete fields",
                           font=("Arial", 12), padx = 50, pady = 30, bg = "red", fg = "yellow").pack()

            backbutton = Button(error, text="Back to Create Function", command = error.destroy, bg = "green").pack()
        
            error.mainloop()

        else:
            create_users.membership_creation(memidentry.get(), nameentry.get(), emailentry.get(), facultyentry.get(), phonenumentry.get())
            
            success = Tk()
            success.geometry('500x300')

            label = Label(success, text = "Success!", font=("Arial", 25), padx = 50, pady = 30).pack()
            label2 = Label(success, text = "ALS Membership created.", font=("Arial", 12), padx = 50, pady = 30).pack()

            backbutton = Button(success, text="Back to Create Function", command = success.destroy).pack()
        
            success.mainloop()
    
    global memid
    memid = StringVar()
    memidlbl = Label(membercreation, text='Membership ID')
    memidlbl.grid(row =1 , column = 1)
    memidentry = Entry(membercreation, textvariable=memid, width = 80)
    memidentry.grid(row = 1, column = 2)
    memidentry.focus()

    global name
    name = StringVar()
    namelbl = Label(membercreation, text='Name')
    namelbl.grid(row =2, column =1)
    nameentry = Entry(membercreation, textvariable=name, width = 80)
    nameentry.grid(row=2,column=2)
    nameentry.focus()

    global faculty
    faculty = StringVar()
    facultylbl = Label(membercreation, text = 'Faculty')
    facultylbl.grid(row=3, column=1)
    facultyentry = Entry(membercreation, textvariable = faculty, width = 80)
    facultyentry.grid(row=3,column=2)

    global phonenum
    phonenum = IntVar()
    phonenumlbl = Label(membercreation, text = 'Phone Number')
    phonenumlbl.grid(row=4, column=1)
    phonenumentry = Entry(membercreation, textvariable = phonenum, width = 80)
    phonenumentry.grid(row=4,column=2)

    global email
    email = StringVar()
    emaillbl = Label(membercreation, text = 'Email Address')
    emaillbl.grid(row=5, column=1)
    emailentry = Entry(membercreation, textvariable = email, width = 80)
    emailentry.grid(row=5,column=2)

    createbutton = Button(membercreation, text="Create Member", command = membercreatebutton)
    createbutton.grid(row=6,column=1)

    backtomainbtn = Button(membercreation, text="Back to Main Menu", command = membercreation.destroy)
    backtomainbtn.grid(row=6,column=2)
    
    membercreation.mainloop()



def memberdeletionbutton():
    memberdeletion = Tk()
    memberdeletion.title("Delete Membership")
    memberdeletion.geometry('900x600')
    label = Label(memberdeletion, text = "To Delete Member, Please Enter Membership ID:",
                  font=("Arial", 15), relief = RIDGE, padx = 50, pady = 30).grid(row=0, column = 0, columnspan = 2)

    def confirmdelete():
        delete.membership_deletion(memidentry.get())
        error = Tk()
        error.geometry('500x300')
        error.configure(background='green')

        label = Label(error, text = "Success!", font=("Arial", 25), padx = 50, pady = 30,
                        bg = "green", fg = "yellow").pack()
        label2 = Label(error, text = "Member deleted.",
                        font=("Arial", 12), padx = 50, pady = 30, bg = "green", fg = "yellow").pack()

        backbutton = Button(error, text="Back to Delete Function", command = error.destroy, bg = "yellow").pack()

        error.mainloop()
        return

    def memberdeletebutton():
        #check if member exists
        if not Session(bind=engine).query(Member).filter(memidentry.get() == Member.membershipid).first():
            error = Tk()
            error.geometry('500x300')
            error.configure(background='red')

            label = Label(error, text = "Error!", font=("Arial", 25), padx = 50, pady = 30,
                          bg = "red", fg = "yellow").pack()
            label2 = Label(error, text = "Member does not exist.",
                           font=("Arial", 12), padx = 50, pady = 30, bg = "red", fg = "yellow").pack()

            backbutton = Button(error, text="Back to Delete Function", command = error.destroy, bg = "green").pack()

            error.mainloop()

        #check if member has loans, reservations or outstanding fines
        elif display_member_loans(memidentry.get()) or memidentry.get() in [row[0] for row in display_fines()] or memidentry.get() in [row[2] for row in display_books_on_reservation()]:
            error = Tk()
            error.geometry('500x300')
            error.configure(background='red')

            label = Label(error, text = "Error!", font=("Arial", 25), padx = 50, pady = 30,
                          bg = "red", fg = "yellow").pack()
            label2 = Label(error, text = "Member has loans, reservations or outstanding fines.",
                           font=("Arial", 12), padx = 50, pady = 30, bg = "red", fg = "yellow").pack()

            backbutton = Button(error, text="Back to Delete Function", command = error.destroy, bg = "green").pack()
        
            error.mainloop()

        else:

            #SQL code
            member_to_delete = Session(bind=engine).query(Member).filter(Member.membershipid == memidentry.get()).first()

            ## details are all here, can put on confirmation page
            member_id = member_to_delete.membershipid
            member_name = member_to_delete.name
            member_fac = member_to_delete.faculty
            member_hp = member_to_delete.phonenumber
            memberemail = member_to_delete.email
            
            success = Tk()
            success.geometry('1000x700')

            label = Label(success, text = "PLease Confirm Details \n to Be Correct!",
                          font=("Arial", 25), padx = 50, pady = 30).grid(row=0, columnspan=2)
            memberid = Label(success, text = "Member ID: ", font=("Arial", 12), padx = 50, pady = 30).grid(row=1, column=0)
            memberid1 = Label(success, text = member_id, font=("Arial", 12), padx = 30, pady = 30).grid(row=1, column=1)
            membername = Label(success, text = "Name: ", font=("Arial", 12), padx = 50, pady = 30).grid(row=2, column=0)
            membername1 = Label(success, text = member_name, font=("Arial", 12), padx = 30, pady = 30).grid(row=2, column=1)
            memberfac = Label(success, text = "Faculty: ", font=("Arial", 12), padx = 50, pady = 30).grid(row=3, column=0)
            memberfac1 = Label(success, text = member_fac, font=("Arial", 12), padx = 30, pady = 30).grid(row=3, column=1)
            memberhp = Label(success, text = "Phone Number: ", font=("Arial", 12), padx = 50, pady = 30).grid(row=4, column=0)
            memberhp1 = Label(success, text = member_hp, font=("Arial", 12), padx = 30, pady = 30).grid(row=4, column=1)
            member_email = Label(success, text = "Email Address: ", font=("Arial", 12), padx = 50, pady = 30).grid(row=5, column=0)
            member_email1 = Label(success, text = memberemail, font=("Arial", 12), padx = 30, pady = 30).grid(row=5, column=1)

            confirmbutton = Button(success, text="Confirm Deletion",
                                   command = confirmdelete).grid(row=7, column=0)
            backbutton = Button(success, text="Back to Delete Function",
                                command = success.destroy).grid(row=7, column=1)

            success.mainloop()

    global memid
    memid = StringVar()
    memidlbl = Label(memberdeletion, text='Membership ID')
    memidlbl.grid(row =1 , column = 0)
    memidentry = Entry(memberdeletion, textvariable=memid)
    memidentry.grid(row = 1, column = 1)

    deletebutton = Button(memberdeletion, text="Delete Member", command = memberdeletebutton)
    deletebutton.grid(row=2,column=0)

    backtomainbtn = Button(memberdeletion, text="Back to Main Menu", command = memberdeletion.destroy)
    backtomainbtn.grid(row=2,column=1)
    
    memberdeletion.mainloop()


def updatememberbutton():
    memberupdate = Tk()
    memberupdate.title("Update Membership")
    memberupdate.geometry('900x600')
    label = Label(memberupdate, text = "To Update a Member, Please Enter Membership ID:",
                  font=("Arial", 15), relief = RIDGE, padx = 50, pady = 30)
    label.grid(row=0, column = 0, columnspan = 2)

    
            

    def memberupdatebutton():
        update = Tk()
        update.title("Update Membership")
        update.geometry('900x600')
        label = Label(update, text = "Please Enter Requested Information Below:",
                      font=("Arial", 15), relief = RIDGE, padx = 50, pady = 30)
        label.grid(row=0, column = 0, columnspan = 2)

        #def createbutton():
        #    return

        def confirmupdate():
            success = Tk()
            success.geometry('500x300')

            label = Label(success, text = "Success!",font=("Arial", 25), padx = 50, pady = 30)
            label.grid(row=0, columnspan=2)
            label2 = Label(success, text = "ALS Membership Updated.", font=("Arial", 12), padx = 50, pady = 30)
            label2.grid(row=1, columnspan=2)

            confirmbutton2 = Button(success, text="Create Another Member", command = membershipcreationbutton)
            confirmbutton2.grid(row=2, column=0)
            backbutton2 = Button(success, text="Back to Update Function", command = success.destroy)
            backbutton2.grid(row=2, column=1)
            
            update_file.update_email(memidentry.get(), email1.get())
            update_file.update_phone(memidentry.get(), phonenum1.get())
            update_file.update_faculty(memidentry.get(), faculty1.get())
            update_file.update_name(memidentry.get(), name1.get())

            success.mainloop()

        def updatec():
            #check if there are missing or incomplete fields
            if not name1.get() or not faculty1.get() or not phonenum1.get() or not email1.get(): #to be edited 
                error = Tk()
                error.geometry('500x300')
                error.configure(background='red')

                label = Label(error, text = "Error!", font=("Arial", 25), padx = 50, pady = 30,
                            bg = "red", fg = "yellow").pack()
                label2 = Label(error, text = "Missing or Incomplete fields.",
                            font=("Arial", 12), padx = 50, pady = 30, bg = "red", fg = "yellow").pack()

                backbutton = Button(error, text="Back to Update Function", command = error.destroy, bg = "green").pack()
            
                error.mainloop()
            
            elif Session(bind=engine).query(Member).filter(Member.membershipid == memidentry.get()).first():
                success = Tk()
                success.geometry('500x300')

                label = Label(success, text = "PLease Confirm Updated \n Details to Be Correct", font=("Arial", 25), padx = 50, pady = 30)
                label.grid(row=0, columnspan=2)
                memberid = Label(success, text = "Member ID: ").grid(row=1, column=0)
                memberid1 = Label(success, text = memidentry.get()).grid(row=1, column=1)
                membername = Label(success, text = "Name: ").grid(row=2, column=0)
                membername1 = Label(success, text = name1.get()).grid(row=2, column=1)
                memberfac = Label(success, text = "Faculty: ").grid(row=3, column=0)
                memberfac1 = Label(success, text = faculty1.get()).grid(row=3, column=1)
                memberhp = Label(success, text = "Phone Number: ").grid(row=4, column=0)
                memberhp1 = Label(success, text = phonenum1.get()).grid(row=4, column=1)
                member_email = Label(success, text = "Email Address: ").grid(row=5, column=0)
                member_email1 = Label(success, text = email1.get()).grid(row=5, column=1)


                confirmbutton1 = Button(success, text="Confirm Update", command = confirmupdate)
                confirmbutton1.grid(row=6, column=0)
                backbutton1 = Button(success, text="Back to Update Function", command = success.destroy)
                backbutton1.grid(row=6, column=1)
            
                success.mainloop()



            else:
                error = Tk()
                error.geometry('500x300')
                error.configure(background='red')

                label = Label(error, text = "Error!", font=("Arial", 25), padx = 50, pady = 30,
                            bg = "red", fg = "yellow").pack()
                label2 = Label(error, text = "Member does not exist.",
                            font=("Arial", 12), padx = 50, pady = 30, bg = "red", fg = "yellow").pack()

                backbutton = Button(error, text="Back to Update Function", command = error.destroy, bg = "green").pack()
            
                error.mainloop()

        memid = Label(update, text = "Membership ID", fg="white",bg = "blue", width = 20)
        memid.grid(row=1, column=0)
        name = Label(update, text = "Name", bg = "blue",fg="white", width = 20)
        name.grid(row=2, column=0)
        faculty = Label(update, text = "Faculty", fg="white",bg = "blue", width = 20)
        faculty.grid(row=3, column=0)
        phonenum = Label(update, text = "Phone Number",fg="white", bg = "blue", width = 20)
        phonenum.grid(row=4, column=0)
        email = Label(update, text = "Email Address", fg="white", bg = "blue", width = 20)
        email.grid(row=5, column=0)

        memid1 = Label(update, text=memidentry.get(), width = 50)
        memid1.grid(row=1, column=1)
        global name1
        name1 = Entry(update, width = 50)
        name1.grid(row=2, column=1)
        global faculty1
        faculty1 = Entry(update, width = 50)
        faculty1.grid(row=3, column=1)
        global phonenum1
        phonenum1 = Entry(update, width = 50)
        phonenum1.grid(row=4, column=1)
        global email1
        email1 = Entry(update, width = 50)
        email1.grid(row=5, column=1)

        updatebutton = Button(update, text="Update Member", command = updatec)
        updatebutton.grid(row=6,column=0)
        backtomembtn = Button(update, text="Back to Main Menu", command = update.destroy)
        backtomembtn.grid(row=6,column=1)
        
        update.mainloop()

    global memid
    memid = StringVar()
    memidlbl = Label(memberupdate, text='Membership ID')
    memidlbl.grid(row = 1 , column = 0)
    memidentry = Entry(memberupdate, textvariable=memid)
    memidentry.grid(row = 1, column = 1)

    deletebutton = Button(memberupdate, text="Update Member", command = memberupdatebutton)
    deletebutton.grid(row=2,column=0)

    backtomainbtn = Button(memberupdate, text="Back to Main Menu", command = memberupdate.destroy)
    backtomainbtn.grid(row=2,column=1)
    
    memberupdate.mainloop()

def booksbutton():
    books = Tk()
    books.title("Books")
    books.geometry('900x600')
    label = Label(books, text = "Select one of the Options below:",
                  font=("Arial", 15), relief = RIDGE, padx = 50, pady = 30).pack()
    
    bookacquisitionbtn = Button(books, text="Acquisition", command = bookacquisition).pack(pady = 15)

    bookwithdrawalbtn = Button(books, text="Withdrawal", command = bookwithdrawal).pack(pady = 15)

    backtomainbtn = Button(books, text="Back to Main Menu", command = books.destroy).pack(pady = 15)
    
    books.mainloop()

def bookacquisition():
    bookacqn = Tk()
    bookacqn.title("Books")
    bookacqn.geometry('900x600')
    

    label = Label(bookacqn, text = "For New Book Acquisition, Please Enter Requested Information Below:",
                  font=("Arial", 15), relief = RIDGE, padx = 50, pady = 30).grid(row=0, column = 0, columnspan = 3)

    def addnewbookbtn():
        #check if book is alr added/missing fields (DONE)
        if Session(bind = engine).query(Book).filter(Book.accessionNo == accessionnumentry.get()).all() or not accessionnumentry.get() or not titleentry.get() or not authorsentry.get() \
            or not isbnentry.get() or not publisherentry.get() or not yearentry.get():
            error = Tk()
            error.geometry('500x300')
            error.configure(background='red')

            label = Label(error, text = "Error!", font=("Arial", 25), padx = 50, pady = 30,
                          bg = "red", fg = "yellow").pack()
            label2 = Label(error, text = "Book already added; Duplicate, Missing or Incomplete fields.",
                           font=("Arial", 12), padx = 50, pady = 30, bg = "red", fg = "yellow").pack()

            backbutton = Button(error, text="Back to Acquisition Function", command = error.destroy, bg = "green").pack()
        
            error.mainloop()

        else:
            #SQL code to include book in library
            try:
                create_users.book_acquisition(accessionnumentry.get(), isbnentry.get(), authorsentry.get(), yearentry.get(), publisherentry.get(), titleentry.get())
            except:
                error = Tk()
                error.geometry('500x300')
                error.configure(background='red')

                label = Label(error, text = "Error!", font=("Arial", 25), padx = 50, pady = 30,
                    bg = "red", fg = "yellow").pack()
                label2 = Label(error, text = "Book already added; Duplicate, Missing or Incomplete fields.", 
                    font=("Arial", 12), padx = 50, pady = 30, bg = "red", fg = "yellow").pack()

                backbutton = Button(error, text="Back to Acquisition Function", command = error.destroy, bg = "green").pack()
        
                error.mainloop()
            else:
                success = Tk()
                success.geometry('500x300')

                label = Label(success, text = "Success!", font=("Arial", 25), padx = 50, pady = 30).grid(row=0)
                label2 = Label(success, text = "New Book added in Library", font=("Arial", 12), padx = 50, pady = 30).grid(row=1)

                backbutton1 = Button(success, text="Back to Acquisition Function", command = success.destroy).grid(row=2)
        
                success.mainloop()

    global accessionnum
    accessionnum = IntVar()
    accessionnumentry = Entry(bookacqn, textvariable = accessionnum, width = 50)
    accessionnumentry.grid(row=1, column=1)
    accessionnum1 = Label(bookacqn, text = "Accession Number", fg="white",bg = "blue", width = 40)
    accessionnum1.grid(row=1, column=0)

    global title
    title = StringVar()
    titleentry = Entry(bookacqn, textvariable = title, width = 50)
    titleentry.grid(row=2, column=1)
    title1 = Label(bookacqn, text = "Title", fg="white", bg = "blue", width = 40)
    title1.grid(row=2, column=0)
    
    global authors
    authors = StringVar()
    
    authorsentry = Entry(bookacqn, textvariable = authors, width = 50)
    authorsentry.grid(row=3, column=1)
    
    authors1 = Label(bookacqn, text = "Authors \n (For multiple Authors, please separate by ,)", fg="white",bg = "blue", width = 40)
    authors1.grid(row=3, column=0)
    
    global isbn
    isbn = StringVar()
    isbnentry = Entry(bookacqn, textvariable = isbn, width = 50)
    isbnentry.grid(row=4, column=1)
    isbn1 = Label(bookacqn, text = "ISBN", fg="white",bg = "blue", width = 40)
    isbn1.grid(row=4, column=0)

    global publisher
    publisher = StringVar()
    publisherentry = Entry(bookacqn, textvariable = publisher, width = 50)
    publisherentry.grid(row=5, column=1)
    publisher1 = Label(bookacqn, text = "Publisher", fg="white",bg = "blue", width = 40)
    publisher1.grid(row=5, column=0)
    
    global year
    year = IntVar()
    yearentry = Entry(bookacqn, textvariable = year, width = 50)
    yearentry.grid(row=6, column=1)
    year1 = Label(bookacqn, text = "Publication Year", fg="white" , bg = "blue", width = 40)
    year1.grid(row=6, column=0)

    addnewbtn = Button(bookacqn, text="Add New Book", command = addnewbookbtn)
    addnewbtn.grid(row=7,column=0)
    backtobookbtn = Button(bookacqn, text="Back to Books Menu", command = bookacqn.destroy)
    backtobookbtn.grid(row=7,column=1)
    
    bookacqn.mainloop()


def bookwithdrawal():
    bookwithd = Tk()
    bookwithd.title("Books")
    bookwithd.geometry('900x600')
    label = Label(bookwithd, text = "To Remove Outdated Books From System, Please Enter Requested Information Below:",
                  font=("Arial", 15), relief = RIDGE, padx = 50, pady = 30).grid(row=0, column = 0, columnspan = 2)

    def confirmwithdraw():
        #SQL code to remove book from system
        delete.withdraw_book(accessionnumentry.get())
        return

    def withdrawbookbtn():
        #check if book currently on loan
        if Session(bind = engine).query(Borrow).filter(Borrow.accessionNo == accessionnumentry.get()).all(): #to be edited
            error = Tk()
            error.geometry('500x300')
            error.configure(background='red')

            label = Label(error, text = "Error!", font=("Arial", 25), padx = 50, pady = 30,
                          bg = "red", fg = "yellow").pack()
            label2 = Label(error, text = "Book is currently on Loan.",
                           font=("Arial", 12), padx = 50, pady = 30, bg = "red", fg = "yellow").pack()

            backbutton = Button(error, text="Back to Withdrawal Function", command = error.destroy, bg = "green").pack()
        
            error.mainloop()

        #check if book currently reserved
        elif Session(bind = engine).query(Reservation).filter(Reservation.accessionNo == accessionnumentry.get()).all(): #to be edited
            error1 = Tk()
            error1.geometry('500x300')
            error1.configure(background='red')

            label = Label(error1, text = "Error!", font=("Arial", 25), padx = 50, pady = 30,
                          bg = "red", fg = "yellow").pack()
            label2 = Label(error1, text = "Book is currently Reserved.",
                           font=("Arial", 12), padx = 50, pady = 30, bg = "red", fg = "yellow").pack()

            backbutton = Button(error1, text="Back to Withdrawal Function", command = error1.destroy, bg = "green").pack()
        
            error1.mainloop()
            
        else:
            try:
                book = Session(bind = engine).query(Book).filter(Book.accessionNo == accessionnumentry.get()).first()
                book_isbn = Session(bind = engine).query(Isbn).filter(Isbn.isbn == book.isbn).first()
                book_author = Session(bind = engine).query(Author).filter(Author.isbn == book.isbn).first()
            except:
                error1 = Tk()
                error1.geometry('500x300')
                error1.configure(background='red')

                label = Label(error1, text = "Error!", font=("Arial", 25), padx = 50, pady = 30,
                            bg = "red", fg = "yellow").pack()
                label2 = Label(error1, text = "No such Book.",
                            font=("Arial", 12), padx = 50, pady = 30, bg = "red", fg = "yellow").pack()

                backbutton = Button(error1, text="Back to Withdrawal Function", command = error1.destroy, bg = "green").pack()
        
                error1.mainloop()
            else:
                success = Tk()
                success.geometry('900x600')

                label = Label(success, text = "PLease Confirm Updated \n Details to Be Correct", font=("Arial", 25), padx = 50, pady = 30).grid(row=0, columnspan=2)
                accnumlbl= Label(success,text = "Accession Number: {s} ".format(s= accessionnumentry.get() ))
                accnumlbl.grid(row=1 , column = 0)
                #get book function
                #replace (s="booktitle")
                booktitlelbl= Label(success,text = "Book Title : {s}".format(s=book_isbn.title))
                booktitlelbl.grid(row=2, column=0)
                authorlbl= Label(success, text = "Authors : {s}".format(s=book_author.authorname))
                authorlbl.grid(row = 3, column =0)
                isbnlbl= Label(success,text = "ISBN : {s}".format(s=book_isbn.isbn))
                isbnlbl.grid(row = 4 ,column = 0)
                publbl = Label(success,text="Publisher : {s}".format(s=book_isbn.publisher))
                publbl.grid(row=5,column = 0)
            
                pubyearlbl = Label(success,text="Publisher Year : {s}".format(s=book_isbn.publisherYear))
                pubyearlbl.grid(row=6,column = 0)

                confirmbutton1 = Button(success, text="Confirm Withdrawal", command = confirmwithdraw)
                confirmbutton1.grid(row=7, column=0)
                backbutton1 = Button(success, text="Back to Withdrawal Function", command = success.destroy)
                backbutton1.grid(row=7, column=1)
            
                success.mainloop()

    global accessionnum
    accessionnum = IntVar()
    accessionnumentry = Entry(bookwithd, textvariable = accessionnum, width = 50)
    accessionnumentry.grid(row=1, column=1)
    accessionnumlbl = Label(bookwithd, text = "Accession Number", bg = "blue", width = 20)
    accessionnumlbl.grid(row=1, column=0)

    withdrawbtn = Button(bookwithd, text="Withdraw Book", command = withdrawbookbtn).grid(row=2,column=0)
    backtobookbtn = Button(bookwithd, text="Back to Books Menu", command = bookwithd.destroy).grid(row=2,column=1)
    
    bookwithd.mainloop() 


#reserve book
def reservationsbutton():
    win = Tk()
    win.title("Reservations")
    win.geometry("900x600")
    label = Label(win, text = "Select one of the Options below:",
                  font=("Arial", 15), relief = RIDGE, padx = 50, pady = 30).grid(row =1, column = 3,pady = 30)
    reslbl = Label(win, text = "Reservation", font = ("Arial",25), relief = RIDGE , width = 15, height = 10)
    reslbl.grid( row =2 , rowspan=2 , padx = 50, column =1)
    bookreslbl = Label(win, text="Book Reservation")
    bookreslbl.grid (row =2 , column = 4)
    cancellbl = Label(win, text = "Reservation Cancellation")
    cancellbl.grid(row=3,column =4)
    reserveabookbtn = Button(win, text = "Reserve A Book" , width = 15, height = 5, command = reserveabook)
    reserveabookbtn.grid(row=2, column = 3 ,pady= 30)
    cancelreservationbtn = Button(win, text = " Cancel Reservation",width = 15, height= 5, command = cancelreservation)
    cancelreservationbtn.grid(row = 3, column=3,  pady = 30)
    backtomainbtn = Button(win, text="Back to Main Menu", command = win.destroy)
    backtomainbtn.grid(row = 4, column = 4,  pady =10)
    win.mainloop()

def reserveabook():
    win = Tk()
    win.title('Reserve A Book')
    win.geometry("900x600")
    label = Label(win, text = "To Reserve a Book, Please Enter Information Below:",
                  font=("Arial", 15), relief = RIDGE, padx = 50, pady = 30)
    label.grid(row=0, column = 2, columnspan = 2)
    
    def reservebook():
    
        win=Tk()
        win.title("Confirm Reservation")
        win.geometry("400x300")
        label = Label(win, text = "Confirm Reservation Details", font = ("Arial", 25), padx=20 , pady=20 )
        label.grid(row=0, column = 0, columnspan = 2)
        accnumlbl= Label(win,text = "Accession Number: {s} ".format(s= accnumentry.get() ))
        accnumlbl.grid(row=1 , column = 0)
        #get book function (DONE)
        book_temp = Session(bind = engine).query(Book).filter(Book.accessionNo == accnumentry.get()).first()
        #replace (s="booktitle") (DONE)
        if book_temp:
            isbn_temp = Session(bind = engine).query(Isbn).filter(Isbn.isbn == book_temp.isbn).first()
            booktitlelbl= Label(win,text = "Book Title : {s}".format(s=isbn_temp.title))
        else:
            booktitlelbl = Label(win,text = "Book Title : {s}".format(s="N/A"))
        booktitlelbl.grid(row=2, column=0)
        memidlbl = Label(win,text="Membership ID : {s}".format(s=memidentry.get()))
        memidlbl.grid(row=3,column = 0)
        #get name function (DONE)
        member = Session(bind = engine).query(Member).filter(Member.membershipid == memidentry.get()).first()
        #replace s=name (DONE)
        if member:
            memnamelbl=Label(win,text= "Member Name : {s}".format(s=member.name))
        else:
            memnamelbl=Label(win,text= "Member Name : {s}".format(s="N/A"))
        memnamelbl.grid(row=4,column=0)
        reservedatelbl= Label(win,text= "Reservation Date : {s}".format(s=resdateentry.get()))
        reservedatelbl.grid(row=5,column=0)

        cfmreservationbtn = Button(win,text = "Confirm Reservation" , command = reservationerror)
        cfmreservationbtn.grid(row=6,column=0)

        backtoreservebtn= Button(win,text= "Back to reserve function", command = win.destroy)
        backtoreservebtn.grid(row=6,column=1)

    def reservationerror():
        # if alr have 2 reservations (DONE)
        if len(Session(bind = engine).query(Reservation).filter(Reservation.accessionNo == accnumentry.get()).all()) > 2:
            win=Tk()
            win.title("Error")
            label = Label(win, text = "Error!", font = ("Arial", 25), padx=20 , pady=20 )
            label.pack()
            errormsg = Label(win, text = "Member currently  has 2 Books on Reservation.")
            errormsg.pack()
            backtoreservebtn= Button(win,text= "Back to reserve function", command = win.destroy)
            backtoreservebtn.pack()

        # elif outstanding fine (DONE)
        elif Session(bind = engine).query(Fine).filter(Fine.membershipid == memidentry.get()).first():
            win=Tk()
            win.title("Error")
            label = Label(win, text = "Error!", font = ("Arial", 25), padx=20 , pady=20 )
            label.pack()
            #get fine function (DONE)
            fines_to_pay = Session(bind = engine).query(Fine).filter(Fine.membershipid == memidentry.get()).all()
            total_fine = sum(x.paymentAmount for x in fines_to_pay)
            #replace s=$10 (DONE)
            errormsg = Label(win, text = "Member currently  has outstanding fine of {s}".format(s=total_fine))
            errormsg.pack()
            backtoreservebtn= Button(win,text= "Back to reserve function", command = win.destroy)
            backtoreservebtn.pack()

        elif not Session(bind = engine).query(Borrow).filter(Borrow.accessionNo == accnumentry.get()).first():
            win=Tk()
            win.title("Error")
            label = Label(win, text = "Error!", font = ("Arial", 25), padx=20 , pady=20 )
            label.pack()
            errormsg = Label(win, text = "Book available for loan, do not reserve")
            errormsg.pack()
            backtoreservebtn= Button(win,text= "Back to reserve function", command = win.destroy)
            backtoreservebtn.pack()
        
         #elif outstandingfine
        else:
            try:
                create_users.book_reservation(accnumentry.get(), memidentry.get(), resdateentry.get())
                win = Tk()
            

                win.title("Success")
                lbl=Label(win, text = "Success" , font=("Arial",25))
                lbl.pack()

                exitbtn = Button(win, test= "Exit" , command = win.destroy)
                exitbtn.pack()
            except:
                win=Tk()
                win.title("Error")
                label = Label(win, text = "Error!", font = ("Arial", 25), padx=20 , pady=20 )
                label.pack()
                #get fine function (DONE)
                fines_to_pay = Session(bind = engine).query(Fine).filter(Fine.membershipid == memidentry.get()).all()
                total_fine = sum(x.paymentAmount for x in fines_to_pay)
                #replace s=$10 (DONE)
                errormsg = Label(win, text = "Error")
                errormsg.pack()
                backtoreservebtn= Button(win,text= "Back to reserve function", command = win.destroy)
                backtoreservebtn.pack()

    
    

    
    
    
                        
    
    
    
       
    

    global accessionnumber
    accessionnumber = StringVar()
    
    accnumlbl= Label(win, text = "Accession Number", padx = 50, pady=30)
    accnumlbl.grid(row=1,column=1)
    accnumentry= Entry(win, textvariable=accessionnumber)
    accnumentry.grid(row=1,column=2, columnspan=2)

    global memid
    memid = StringVar()
    memidlbl= Label(win, text = "Membership ID", padx = 50, pady=30)
    memidlbl.grid(row=2,column=1)
    memidentry= Entry(win, textvariable=memid)
    memidentry.grid(row=2,column=2, columnspan=2)

    
    global resdate
    resdate= StringVar()
    resdatelbl= Label(win, text = "Reservation Date", padx = 50, pady=30)
    resdatelbl.grid(row=3,column=1)
    resdateentry= Entry(win, textvariable=resdate)
    resdateentry.grid(row=3,column=2, columnspan=2)

    backtoreservationbtn= Button(win,text="Back to Resevations Menu",command = win.destroy)
    backtoreservationbtn.grid(row=4, column = 4)

    reservebookbtn = Button(win,text = "Reserve Book" , command = reservebook)
    reservebookbtn.grid(row =4 , column = 1)
    
    
    #book_reservation(accnumentry.get(), memidentry.get())
    





    
    

    
    
    
       
    win.mainloop()
    #book_reservation(accnumentry.get(), memidentry.get())


    
#cancel reservation
def cancelreservation():
    win = Tk()
    win.title('Cancel A Reservation')
    win.geometry("900x600")
    label = Label(win, text = "To Cancel a Reservation, Please Enter Information Below:",
                  font=("Arial", 15), relief = RIDGE, padx = 50, pady = 30)
    label.grid(row=0, column = 2, columnspan = 2)

    
    
    
    def cancelres():
        win=Tk()
        win.title("Cancel Reservation")
        win.geometry("400x300")
        label = Label(win, text = "Confirm Cancellation Details", font = ("Arial", 25), padx=20 , pady=20 )
        label.grid(row=0, column = 0, columnspan = 2)
        accnumlbl= Label(win,text = "Accession Number: {s} ".format(s= accnumentry.get() ))
        accnumlbl.grid(row=1 , column = 0)
        #get book function
        book = Session(bind = engine).query(Book).filter(Book.accessionNo == accnumentry.get()).first()
        if book:
            book_isbn = Session(bind = engine).query(Isbn).filter(Isbn.isbn == Book.isbn).first()
            #replace (s="booktitle")
            booktitlelbl= Label(win,text = "Book Title : {s}".format(s=book_isbn.title))
        else:
            booktitlelbl= Label(win,text = "Book Title : {s}".format(s="N/A"))
        booktitlelbl.grid(row=2, column=0)
        memidlbl = Label(win,text="Membership ID : {s}".format(s=memidentry.get()))
        memidlbl.grid(row=3,column = 0)
        #get name function
        member = Session(bind = engine).query(Member).filter(memidentry.get() == Member.membershipid).first()
        #replace s=name
        if member:
            memnamelbl=Label(win,text= "Member Name : {s}".format(s=member.name))
        else:
            memnamelbl=Label(win,text= "Member Name : {s}".format(s="N/A"))
        memnamelbl.grid(row=4,column=0)
        reservedatelbl= Label(win,text= "Cancellation Date : {s}".format(s=cancelresdateentry.get()))
        reservedatelbl.grid(row=5,column=0)

        cfmcancelbtn = Button(win,text = "Confirm Cancellation" , command = cancelerror)
        cfmcancelbtn.grid(row=6,column=0)
    
        backtoreservebtn= Button(win,text= "Back to reserve function", command = win.destroy)
        backtoreservebtn.grid(row=6,column=1)






    def cancelerror():
        #if no reservation
        reservation = Session(bind = engine).query(Reservation).filter(Reservation.accessionNo == accnumentry.get() and memidentry.get() == Reservation.membershipid).first()
        if not reservation:
            win=Tk()
            win.title("Error")
            label = Label(win, text = "Error!", font = ("Arial", 25), padx=20 , pady=20 )
            label.pack()
            errormsg = Label(win, text = "Member has no such Reservation.")
            errormsg.pack()
            backtoreservebtn= Button(win,text= "Back to reserve function", command = win.destroy)
            backtoreservebtn.pack()
        elif not Session(bind = engine).query(Member).filter(Member.membershipid == memidentry.get()).first():
            win=Tk()
            win.title("Error")
            label = Label(win, text = "Error!", font = ("Arial", 25), padx=20 , pady=20 )
            label.pack()
            errormsg = Label(win, text = "No such Member.")
            errormsg.pack()
            backtoreservebtn= Button(win,text= "Back to reserve function", command = win.destroy)
            backtoreservebtn.pack()
        else:
            create_users.reservation_cancellation(accnumentry.get(), memidentry.get(), cancelresdateentry.get())
            win = Tk()
            

            win.title("Success")
            lbl=Label(win, text = "Success" , font=("Arial",25))
            lbl.pack()

            exitbtn = Button(win, text= "Exit" , command = win.destroy)
            exitbtn.pack()


    global accessionnumber
    accessionnumber = StringVar()
    
    accnumlbl= Label(win, text = "Accession Number", padx = 50, pady=30)
    accnumlbl.grid(row=1,column=1)
    accnumentry= Entry(win, textvariable=accessionnumber)
    accnumentry.grid(row=1,column=2, columnspan=2)

    global memid
    memid = StringVar()
    memidlbl= Label(win, text = "Membership ID", padx = 50, pady=30)
    memidlbl.grid(row=2,column=1)
    memidentry= Entry(win, textvariable=memid)
    memidentry.grid(row=2,column=2, columnspan=2)

    
    global cancelresdate
    cancelresdate= StringVar()
    cancelresdatelbl= Label(win, text = "Cancel Date", padx = 50, pady=30)
    cancelresdatelbl.grid(row=3,column=1)
    cancelresdateentry= Entry(win, textvariable=cancelresdate)
    cancelresdateentry.grid(row=3,column=2, columnspan=2)

    backtoreservationbtn= Button(win,text="Back to Resevations Menu",command = win.destroy , padx=5)
    backtoreservationbtn.grid(row=4, column = 4)

    cancelresbtn = Button(win,text = "Cancel Reservation" , command = cancelres)
    cancelresbtn.grid(row =4 , column = 1)

    win.mainloop()
    
    





def loansbutton():
    win = Tk()
    win.title("Loans")
    win.geometry("900x600")
    label = Label(win, text = "Select one of the Options below:",
                  font=("Arial", 15), relief = RIDGE, padx = 50, pady = 30).grid(row =1, column = 3,pady = 30)
    loanlbl = Label(win, text = "Loans", font = ("Arial",25), relief = RIDGE , width = 15, height = 10)
    loanlbl.grid( row =2 , rowspan=2 , padx = 50, column =1)
    borrowlbl = Label(win, text="Book Borrowing")
    borrowlbl.grid (row =2 , column = 4)
    returnlbl = Label(win, text = "Book Returning")
    returnlbl.grid(row=3,column =4)
    borrowabookbtn = Button(win, text = "Borrow" , width = 15, height = 5, command = borrowabook)
    borrowabookbtn.grid(row=2, column = 3 ,pady= 30)
    returnabookbtn = Button(win, text = " Return",width = 15, height= 5, command = returnabook)
    returnabookbtn.grid(row = 3, column=3,  pady = 30)
    backtomainbtn = Button(win, text="Back to Main Menu", command = win.destroy)
    backtomainbtn.grid(row = 4, column = 4,  pady =10)
    win.mainloop()

def borrowabook():
    win1 = Tk()
    win1.title('Borrow a Book')
    win1.geometry("900x600")
    label = Label(win1, text = "To Borrow a Book, Please Enter Information Below:",
                  font=("Arial", 15), relief = RIDGE, padx = 50, pady = 30)
    label.grid(row=0, column = 2, columnspan = 2)

    def borrowbook():
    
        win=Tk()
        win.title("Confirm Loan")
        win.geometry("400x300")
        label = Label(win, text = "Confirm Loan Details", font = ("Arial", 25), padx=20 , pady=20 )
        label.grid(row=0, column = 0, columnspan = 2)
        accnumlbl= Label(win,text = "Accession Number: {s} ".format(s= accnumentry.get() ))
        accnumlbl.grid(row=1 , column = 0)
        #get book function
        book = Session(bind = engine).query(Book).filter(Book.accessionNo == accnumentry.get()).first()
        if book:
            bookisbn = Session(bind = engine).query(Isbn).filter(Isbn.isbn == book.isbn).first()
            if bookisbn:
                member = Session(bind = engine).query(Member).filter(Member.membershipid == memidentry.get()).first()
            else:
                member = None
        else:
            bookisbn = None
            member = None
        #replace (s="booktitle")
        if bookisbn:
            booktitlelbl= Label(win,text = "Book Title : {s}".format(s=bookisbn.title))
        else:
            booktitlelbl= Label(win,text = "Book Title : ")
        booktitlelbl.grid(row=2, column=0)
        #get borrow date function
        borrow_date = date.today()
        #replace (s="borrow date")
        borrowdatelbl= Label(win,text = "Borrow Date : {s}".format(s=borrow_date))
        borrowdatelbl.grid(row = 3 ,column = 0)
        
        if member:
            memidlbl = Label(win,text="Membership ID : {s}".format(s=memidentry.get()))
            memnamelbl=Label(win,text= "Member Name : {s}".format(s=member.name))
        else:
            memidlbl = Label(win,text="Membership ID : ")
            memnamelbl=Label(win,text= "Member Name : ")

        memidlbl.grid(row=4,column = 0)
        #get name function
        #replace s=name
        memnamelbl.grid(row=5,column=0)
        #get due date function (dont need)
        #replace s="duedate"
        duedatelbl= Label(win,text= "Return Date : {s}".format(s=borrow_date + timedelta(days=14)))
        duedatelbl.grid(row=6,column=0)

        cfmloanbtn = Button(win,text = "Confirm Loan" , command = loanerror)
        cfmloanbtn.grid(row=7,column=0)

        backtoreturnbtn= Button(win,text= "Back to Return function", command = win.destroy)
        backtoreturnbtn.grid(row=7,column=1)

    def loanerror():
        if Session(bind = engine).query(Borrow).filter(Borrow.accessionNo == accnumentry.get()).first():
            win=Tk()
            win.title("Error")
            label = Label(win, text = "Error!", font = ("Arial", 25), padx=20 , pady=20 )
            label.pack()
            #get return date for book
            # replace s=dd/mm/yy
    
            errormsg = Label(win, text = "Book currently on Loan until: {s}.".format(s = Session(bind = engine).query(Borrow).filter(Borrow.accessionNo == accnumentry.get()).first().returndate))
            errormsg.pack()
            backtoborrowbtn= Button(win,text= "Back to Borrow function", command = win.destroy)
            backtoborrowbtn.pack()

        #else if outstanding fine
        elif Session(bind = engine).query(Fine).filter(Fine.membershipid == memidentry.get()).first():
            win=Tk()
            win.title("Error")
            label = Label(win, text = "Error!", font = ("Arial", 25), padx=20 , pady=20 )
            label.pack()
        
            errormsg = Label(win, text = "Member currently  has outstanding fine.")
            errormsg.pack()
            backtoborrowbtn= Button(win,text= "Back to Borrow function", command = win.destroy)
            backtoborrowbtn.pack()
    
        #elif loan quote exceed
        elif not Session(bind = engine).query(Borrow).filter(Borrow.membershipid == memidentry.get()).count() <= 2:
    
            win=Tk()
            win.title("Error")
            label = Label(win, text = "Error!", font = ("Arial", 25), padx=20 , pady=20 )
            label.pack()
        
            errormsg = Label(win, text = "Member loan quota exceeded.")
            errormsg.pack()
        
            backtoborrowbtn= Button(win,text= "Back to Borrow function", command = win.destroy)
            backtoborrowbtn.pack()
        #else success
        elif not Session(bind = engine).query(Member).filter(Member.membershipid == memidentry.get()) or not Session(bind = engine).query(Book).filter(Book.accessionNo == accnumentry.get()):
            win=Tk()
            win.title("Error")
            label = Label(win, text = "Error!", font = ("Arial", 25), padx=20 , pady=20 )
            label.pack()
        
            errormsg = Label(win, text = "Member or Book does not exist.")
            errormsg.pack()
        
            backtoborrowbtn= Button(win,text= "Back to Borrow function", command = win.destroy)
            backtoborrowbtn.pack()
        else:
            create_users.borrow_book(accnumentry.get(), memidentry.get())
            win = Tk()
            win.title("Success")
            lbl=Label(win, text = "Success" , font=("Arial",25))
            lbl.pack()
            exitbtn = Button(win, text= "Exit" , command = win1.destroy)
            exitbtn.pack()

    
    
    

    
    
    
                        
    
    
    

    global accessionnumber
    accessionnumber = StringVar()
    
    accnumlbl= Label(win1, text = "Accession Number", padx = 50, pady=30)
    accnumlbl.grid(row=1,column=1)
    accnumentry= Entry(win1, textvariable=accessionnumber)
    accnumentry.grid(row=1,column=2, columnspan=2)

    global memid
    memid = StringVar()
    memidlbl= Label(win1, text = "Membership ID", padx = 50, pady=30)
    memidlbl.grid(row=2,column=1)
    memidentry= Entry(win1, textvariable=memid)
    memidentry.grid(row=2,column=2, columnspan=2)

    
   

    backtoloansbtn= Button(win1,text="Back to Loan Menu",command = win1.destroy)
    backtoloansbtn.grid(row=4, column = 4)

    borrowbookbtn = Button(win1,text = "Borrow Book" , command = borrowbook)
    borrowbookbtn.grid(row =4 , column = 1)
    


    win1.mainloop()

def returnabook():
    win = Tk()
    win.title('Return a Book')
    win.geometry("900x600")
    label = Label(win, text = "To Return a Book, Please Enter Information Below:",
                  font=("Arial", 15), relief = RIDGE, padx = 50, pady = 30)
    label.grid(row=0, column = 2, columnspan = 2)

    def returnbook():
        try:
            book = Session(bind = engine).query(Book).filter(Book.accessionNo == accnumentry.get()).first()
            book_isbn = Session(bind = engine).query(Isbn).filter(Isbn.isbn == book.isbn).first()
            borrow = Session(bind = engine).query(Borrow).filter(Borrow.accessionNo == book.accessionNo).first()
            member = Session(bind = engine).query(Member).filter(Member.membershipid == borrow.membershipid).first()
        except:
            book = None
        else:
            win=Tk()
            win.title("Confirm Return")
            win.geometry("400x300")
            label = Label(win, text = "Confirm Return Details", font = ("Arial", 25), padx=20 , pady=20 )
            label.grid(row=0, column = 0, columnspan = 2)
            accnumlbl= Label(win,text = "Accession Number: {s} ".format(s= accnumentry.get() ))
            accnumlbl.grid(row=1 , column = 0)
            #get book function
            #replace (s="booktitle")
            booktitlelbl= Label(win,text = "Book Title : {s}".format(s=book_isbn.title))
            booktitlelbl.grid(row=2, column=0)
        
            #getmemid function
            #replace (s=memid)
            memidlbl = Label(win,text="Membership ID : {s}".format(s=borrow.membershipid))
            memidlbl.grid(row=3,column = 0)
            #get name function
            #replace s=name
            memnamelbl=Label(win,text= "Member Name : {s}".format(s=member.name))
            memnamelbl.grid(row=4,column=0)
        
            returndatelbl= Label(win,text= "Return Date : {s}".format(s=returndateentry.get()))
            returndatelbl.grid(row=5,column=0)
            
            #getfine function
            old_book = local_session.query(Borrow).filter(Borrow.accessionNo == accnumentry.get()).first()
            returndate = datetime.strptime(returndateentry.get(), "%Y-%m-%d").date()
            if returndate > old_book.returndate:
            #replace s=getfine
                finelbl= Label(win , text="Fine: ${s}".format(s=(returndate - old_book.returndate).days))
            else:
                finelbl= Label(win , text="Fine: ${s}".format(s=0))
            finelbl.grid(row =6, column = 0)

            cfmreturnbtn = Button(win,text = "Confirm Return" , command = returnerror)
            cfmreturnbtn.grid(row=7,column=0)

            backtoborrowbtn= Button(win,text= "Back to Borrow function", command = win.destroy)
            backtoborrowbtn.grid(row=7,column=1)
            return
    
        win=Tk()
        win.title("Invalid Accession Number")
        win.geometry("400x300")
        label = Label(win, text = "Invalid Accession Number", font = ("Arial", 25), padx=20 , pady=20 )
        label.grid(row=0, column = 0, columnspan = 2)

        backtoborrowbtn= Button(win,text= "Back to Borrow function", command = win.destroy)
        backtoborrowbtn.grid(row=7,column=0)
    
    
    def returnerror():
        borrow = Session(bind = engine).query(Borrow).filter(Borrow.accessionNo == accnumentry.get()).first()
        if borrow:
            fine = Session(bind = engine).query(Fine).filter(Fine.membershipid == borrow.membershipid).first()
            if fine:
                win=Tk()
                win.title("Error")
                label = Label(win, text = "Error!", font = ("Arial", 25), padx=20 , pady=20 )
                label.pack()
                #get return date for book
                # replace s=dd/mm/yy
            
                errormsg = Label(win, text = "Book returned successfully but has fines.")
                errormsg.pack()
                backtoreturnbtn= Button(win,text= "Back to Return function", command = win.destroy)
                backtoreturnbtn.pack()

            create_users.return_book(borrow.accessionNo, borrow.membershipid, returndateentry.get())
            win = Tk()
            win.title("Success")
            lbl=Label(win, text = "Success" , font=("Arial",25))
            lbl.pack()
            exitbtn = Button(win, text= "Exit" , command = win.destroy)
            exitbtn.pack()
    
    
    
    
                        
    
    
    
    

    

    global accessionnumber
    accessionnumber = StringVar()
    
    accnumlbl= Label(win, text = "Accession Number", padx = 50, pady=30)
    accnumlbl.grid(row=1,column=1)
    accnumentry= Entry(win, textvariable=accessionnumber)
    accnumentry.grid(row=1,column=2, columnspan=2)

    global returndate
    returndate = StringVar()
    returndatelbl= Label(win, text = "Return Date", padx = 50, pady=30)
    returndatelbl.grid(row=2,column=1)
    returndateentry= Entry(win, textvariable=returndate)
    returndateentry.grid(row=2,column=2, columnspan=2)

    
   

    backtoloansbtn= Button(win,text="Back to Loans Menu",command = win.destroy)
    backtoloansbtn.grid(row=4, column = 4)

    returnbookbtn = Button(win,text = "Return Book" , command = returnbook)
    returnbookbtn.grid(row =4 , column = 1)
    


    win.mainloop()
    

    










def finesbutton():
    win = Tk()
    win.title("Fines")
    win.geometry("900x600")
    label = Label(win, text = "Select one of the Options below:",
                  font=("Arial", 15), relief = RIDGE, padx = 50, pady = 30).grid(row =1, column = 3,pady = 30)
    finelbl = Label(win, text = "Fines", font = ("Arial",25), relief = RIDGE , width = 15, height = 10)
    finelbl.grid( row =2 , rowspan=2 , padx = 50, column =1)
    paymentlbl = Label(win, text="Fine Payment")
    paymentlbl.grid (row =2 , rowspan =2, column = 4)
    
    paymentbtn = Button(win, text = "Payment" , width = 15, height = 5, command = payment)
    paymentbtn.grid(row=2, rowspan=2, column = 3 ,pady= 30)
    
    backtomainbtn = Button(win, text="Back to Main Menu", command = win.destroy)
    backtomainbtn.grid(row = 4, column = 4,  pady =10)

    

    
def payment():
    win = Tk()
    win.title('Payment')
    win.geometry("900x600")
    label = Label(win, text = "To Pay A Fine, Please Enter Information Below:",
                  font=("Arial", 15), relief = RIDGE, padx = 50, pady = 30)
    label.grid(row=0, column = 2, columnspan = 2)
   


    def payfine():
    
        win=Tk()
        win.title("Confirm Payment")
        win.geometry("400x300")
        label = Label(win, text = "Confirm Payment Details", font = ("Arial", 25), padx=20 , pady=20 )
        label.grid(row=0, column = 0, columnspan = 2)
    
    
        memidlbl = Label(win,text="Membership ID : {s}".format(s=memidentry.get()))
        memidlbl.grid(row=1,column = 0)
    
        #get amount due function
        mem = Session(bind = engine).query(Fine).filter(Fine.membershipid == memidentry.get()).first()
        #replace s= fine
        if not mem:
            paymentduelbl = Label(win,text = "Payment Due : ${s} (Exact Fee Only)".format(s=0))
        else:
            paymentduelbl = Label(win,text = "Payment Due : ${s} (Exact Fee Only)".format(s=mem.paymentAmount))
        paymentduelbl.grid(row=2,column=0)
    
    
    
        paymentdatelbl= Label(win,text= "Payment Date : {s}".format(s=paymentdateentry.get()))
        paymentdatelbl.grid(row=3,column=0)
    
        cfmpaymentbtn = Button(win,text = "Confirm Payment" , command = paymenterror)
        cfmpaymentbtn.grid(row=4,column=0)

        backtopaymentbtn= Button(win,text= "Back to Payment function", command = win.destroy)
        backtopaymentbtn.grid(row=4,column=1)
        
    

    



    def paymenterror():
        mem = Session(bind = engine).query(Fine).filter(Fine.membershipid == memidentry.get()).first()
        if not Session(bind = engine).query(Fine).filter(Fine.membershipid == memidentry.get()).first():
            win=Tk()
            win.title("Error")
            label = Label(win, text = "Error!", font = ("Arial", 25), padx=20 , pady=20 )
            label.pack()
        
            errormsg = Label(win, text = "Member has no Fines")
            errormsg.pack()
            backtoreturnbtn= Button(win,text= "Back to Payment function", command = win.destroy)
            backtoreturnbtn.pack()

        elif mem.paymentAmount != int(amountentry.get()):
            win=Tk()
            win.title("Error")
            label = Label(win, text = "Error!", font = ("Arial", 25), padx=20 , pady=20 )
            label.pack()
        
            errormsg = Label(win, text = "Incorrect Fine Payment Amount")
            errormsg.pack()
            backtoreturnbtn= Button(win,text= "Back to Payment function", command = win.destroy)
            backtoreturnbtn.pack()
    

        else:
            create_users.fine_payment(memidentry.get(), paymentdateentry.get(), int(amountentry.get()))
            win = Tk()
            

            win.title("Success")
            lbl=Label(win, text = "Success" , font=("Arial",25))
            lbl.pack()

            exitbtn = Button(win, text= "Exit" , command = win.destroy)
            exitbtn.pack()
    

    global memid
    memid = StringVar()
    
    memidlbl= Label(win, text = "Membership ID", padx = 50, pady=30)
    memidlbl.grid(row=1,column=1)
    memidentry= Entry(win, textvariable=memid)
    memidentry.grid(row=1,column=2, columnspan=2)
    
    
    
    
    

    
    global paymentdate
    paymentdate = StringVar()
    paymentdatelbl= Label(win, text = "Payment Date", padx = 50, pady=30)
    paymentdatelbl.grid(row=2,column=1)
    paymentdateentry= Entry(win, textvariable=paymentdate)
    paymentdateentry.grid(row=2,column=2, columnspan=2)

    
    global amount
    amount = StringVar()
    amountlbl= Label(win, text = "Payment Amount", padx = 50, pady=30)
    amountlbl.grid(row=3,column=1)
    amountentry= Entry(win, textvariable=amount)
    amountentry.grid(row=3,column=2, columnspan=2)

    

    
   

    backtofinesbtn= Button(win,text="Back to Fines Menu",command = win.destroy)
    backtofinesbtn.grid(row=4, column = 4)

    payfinebtn = Button(win,text = "Pay Fine" , command = payfine)
    payfinebtn.grid(row =4 , column = 1)
    win.mainloop()
    



def reportsbutton():
    win = Tk()
    win.title("Reports")
    win.geometry("900x600")
    label = Label(win, text = "Select one of the Options below:",
                  font=("Arial", 15), relief = RIDGE, padx = 50, pady = 10).grid(row =1, column = 3,pady = 10)

    def booksearch():
        win = Tk()
        win.title('Search A Book')
        win.geometry("900x600")
        label = Label(win, text = "Search based on one of the categories Below:",
                      font=("Arial", 15), relief = RIDGE, padx = 50, pady = 30)
        label.grid(row=0, column = 2, columnspan = 2)

        def searchbook():

            win=Tk()

            win.title('Search Results')
            win.geometry('500x500')
            label = Label(win, text = "Book Search Result",
                        font=("Arial", 15), relief = RIDGE, padx = 50, pady = 30)
            label.pack(pady = 20)

            book_frame = Frame(win)
            book_frame.pack()

            #scrollbar
            book_scroll = Scrollbar(book_frame)
            book_scroll.pack(side=RIGHT, fill=Y)

            book_scroll = Scrollbar(book_frame,orient='horizontal')
            book_scroll.pack(side= BOTTOM,fill=X)

            set = ttk.Treeview(book_frame,yscrollcommand=book_scroll.set, xscrollcommand =book_scroll.set)



            set.pack()
            book_scroll.config(command=set.yview)
            book_scroll.config(command=set.xview)




            set['columns']= ('Accession Number', 'Title','Authors','ISBN','Publisher','Year')
            set.column("#0", width=0,  stretch=NO)
            set.column("Accession Number",anchor=CENTER, width=80)
            set.column("Title",anchor=CENTER, width=80)
            set.column("Authors",anchor=CENTER, width=80)
            set.column("ISBN",anchor=CENTER, width=80)
            set.column("Publisher",anchor=CENTER, width=80)
            set.column("Year",anchor=CENTER, width=80)

            set.heading("#0",text="",anchor=CENTER)
            set.heading("Accession Number",text="Accession Number",anchor=CENTER)
            set.heading("Title",text="Title",anchor=CENTER)
            set.heading("Authors",text="Authors",anchor=CENTER)
            set.heading("ISBN",text="ISBN",anchor=CENTER)
            set.heading("Publisher",text="Publisher",anchor=CENTER)
            set.heading("Year",text="Year",anchor=CENTER)

            #data
            #getdata function based on input
            #output to be ['Accession Number', 'Title','Authors','ISBN','Publisher','Year']
            #data = getdata
            if titleentry.get():
                data = query_display.book_search_title(titleentry.get())
            elif authorentry.get():
                data = query_display.book_search_author(authorentry.get())
            elif isbnentry.get():
                data = query_display.book_search_isbn(isbnentry.get())
            elif publisherentry.get():
                data = query_display.book_search_publisher(publisherentry.get())
            elif pubyearentry.get():
                data = query_display.book_search_publisheryear(pubyearentry.get())


            global count
            count=0
            
            for record in data:
            
                set.insert(parent='',index='end',iid = count,text='',values=(record[0],record[1],record[2],record[3],record[4],record[5]))
            
                count += 1

            backtosearchbtn= Button(win,text= "Back to Search Function", command = win.destroy)
            backtosearchbtn.pack()

            win.mainloop()

        global title
        title = StringVar()
        
        titlelbl= Label(win, text = "Title", padx = 50, pady=30)
        titlelbl.grid(row=1,column=1)
        titleentry= Entry(win, textvariable=title)
        titleentry.grid(row=1,column=2, columnspan=2)

        global author
        author = StringVar()
        authorlbl= Label(win, text = "Authors", padx = 50, pady=30)
        authorlbl.grid(row=2,column=1)
        authorentry= Entry(win, textvariable=author)
        authorentry.grid(row=2,column=2, columnspan=2)

        
        
        global isbn
        isbn= StringVar()
        isbnlbl= Label(win, text = "ISBN", padx = 50, pady=30)
        isbnlbl.grid(row=3,column=1)
        isbnentry= Entry(win, textvariable=isbn)
        isbnentry.grid(row=3,column=2, columnspan=2)

        global publisher
        publisher= StringVar()
        publisherlbl= Label(win, text = "Publisher", padx = 50, pady=30)
        publisherlbl.grid(row=4,column=1)
        publisherentry= Entry(win, textvariable=publisher)
        publisherentry.grid(row=4,column=2, columnspan=2)

        global pubyear
        pubyear= StringVar()
        pubyearlbl= Label(win, text = "Year", padx = 50, pady=30)
        pubyearlbl.grid(row=5,column=1)
        pubyearentry= Entry(win, textvariable=pubyear)
        pubyearentry.grid(row=5,column=2, columnspan=2)

        
        

        backtoreservationbtn= Button(win,text="Back to Reports Menu",command = win.destroy)
        backtoreservationbtn.grid(row=6, column = 4)

        searchbookbtn = Button(win,text = "Search Book" , command = searchbook)
        searchbookbtn.grid(row =6 , column = 1)
        
        

        win.mainloop()

    
        

    def loanreport():

        win=Tk()

        win.title('Loan Rport')
        win.geometry('500x500')
        label = Label(win, text = "Books On Loan Report",
                      font=("Arial", 15), relief = RIDGE, padx = 50, pady = 30)
        label.pack(pady = 20)

        book_frame = Frame(win)
        book_frame.pack()

        #scrollbar
        book_scrolly = Scrollbar(book_frame)
        book_scrolly.pack(side=RIGHT, fill=Y)

        book_scrollx = Scrollbar(book_frame,orient='horizontal')
        book_scrollx.pack(side= BOTTOM,fill=X)

        set = ttk.Treeview(book_frame,yscrollcommand=book_scrolly.set, xscrollcommand =book_scrollx.set)



        set.pack()
        book_scrolly.config(command=set.yview)
        book_scrollx.config(command=set.xview)


     


        set['columns']= ('Accession Number', 'Title','Authors','ISBN','Publisher','Year')
        set.column("#0", width=0,  stretch=NO)
        set.column("Accession Number",anchor=CENTER, width=80)
        set.column("Title",anchor=CENTER, width=80)
        set.column("Authors",anchor=CENTER, width=80)
        set.column("ISBN",anchor=CENTER, width=80)
        set.column("Publisher",anchor=CENTER, width=80)
        set.column("Year",anchor=CENTER, width=80)

        set.heading("#0",text="",anchor=CENTER)
        set.heading("Accession Number",text="Accession Number",anchor=CENTER)
        set.heading("Title",text="Title",anchor=CENTER)
        set.heading("Authors",text="Authors",anchor=CENTER)
        set.heading("ISBN",text="ISBN",anchor=CENTER)
        set.heading("Publisher",text="Publisher",anchor=CENTER)
        set.heading("Year",text="Year",anchor=CENTER)

        #data
        #getdata function based on input
        #output to be ['Accession Number', 'Title','Authors','ISBN','Publisher','Year']
        #data = getdata
        data  = display_books_on_loan()


        global count
        count=0
        
        for record in data:
          
            set.insert(parent='',index='end',iid = count,text='',values=(record[0],record[1],record[2],record[3],record[4],record[5]))
           
            count += 1

        backtosearchbtn= Button(win,text= "Back to Search Function", command = win.destroy)
        backtosearchbtn.pack()

        win.mainloop()
        
    def resreport():

        win=Tk()

        win.title('Reservation Report')
        win.geometry('500x500')
        label = Label(win, text = "Books On Reservation Report",
                      font=("Arial", 15), relief = RIDGE, padx = 50, pady = 30)
        label.pack(pady = 20)

        book_frame = Frame(win)
        book_frame.pack()

        #scrollbar
        book_scrolly = Scrollbar(book_frame)
        book_scrolly.pack(side=RIGHT, fill=Y)

        book_scrollx = Scrollbar(book_frame,orient='horizontal')
        book_scrollx.pack(side= BOTTOM,fill=X)

        set = ttk.Treeview(book_frame,yscrollcommand=book_scrolly.set, xscrollcommand =book_scrollx.set)



        set.pack()
        book_scrolly.config(command=set.yview)
        book_scrollx.config(command=set.xview)




        set['columns']= ('Accession Number', 'Title','Membership ID','Name')
        set.column("#0", width=0,  stretch=NO)
        set.column("Accession Number",anchor=CENTER, width=80)
        set.column("Title",anchor=CENTER, width=80)
        set.column("Membership ID",anchor=CENTER, width=80)
        set.column("Name",anchor=CENTER, width=80)
        

        set.heading("#0",text="",anchor=CENTER)
        set.heading("Accession Number",text="Accession Number",anchor=CENTER)
        set.heading("Title",text="Title",anchor=CENTER)
        set.heading("Membership ID",text="Membership ID",anchor=CENTER)
        set.heading("Name",text="Name",anchor=CENTER)
       

        #data
        #getdata function based on input
        #output to be ['Accession Number', 'Title','memid', 'name']
        #data = getdata
        data  = display_books_on_reservation()


        global count
        count=0
        
        for record in data:
          
            set.insert(parent='',index='end',iid = count,text='',values=(record[0],record[1],record[2],record[3]))
           
            count += 1

        backtosearchbtn= Button(win,text= "Back to Search Function", command = win.destroy)
        backtosearchbtn.pack()

        win.mainloop()
        
    def finereport():

        win=Tk()

        win.title('Fine Report')
        win.geometry('500x500')
        label = Label(win, text = "Members with Outstanding Fines Report",
                      font=("Arial", 15), relief = RIDGE, padx = 50, pady = 30)
        label.pack(pady = 20)

        book_frame = Frame(win)
        book_frame.pack()

        #scrollbar
        book_scrolly = Scrollbar(book_frame)
        book_scrolly.pack(side=RIGHT, fill=Y)

        book_scrollx = Scrollbar(book_frame,orient='horizontal')
        book_scrollx.pack(side= BOTTOM,fill=X)

        set = ttk.Treeview(book_frame,yscrollcommand=book_scrolly.set, xscrollcommand =book_scrollx.set)



        set.pack()
        book_scrolly.config(command=set.yview)
        book_scrollx.config(command=set.xview)




        set['columns']= ('Membership ID','Name','Faculty','Phone Number' , 'Email Address')
        set.column("#0", width=0,  stretch=NO)
        
        set.column("Membership ID",anchor=CENTER, width=80)
        set.column("Name",anchor=CENTER, width=80)
        set.column("Faculty",anchor=CENTER, width=80)
        set.column("Phone Number",anchor=CENTER, width=80)
        set.column("Email Address",anchor=CENTER, width=80)
        
        

        set.heading("#0",text="",anchor=CENTER)
        
        set.heading("Membership ID",text="Membership ID",anchor=CENTER)
        set.heading("Name",text="Name",anchor=CENTER)
        set.heading("Faculty",text="Faculty",anchor=CENTER)
        set.heading("Phone Number",text="Phone Number",anchor=CENTER)
        set.heading("Email Address",text="Email Address",anchor=CENTER)
       

        #data
        #getdata function based on input
        #output to be ['memid','name','faculty','phone number','email']
        #data = getdata
        data  = display_fines()


        global count
        count=0
        
        for record in data:
          
            set.insert(parent='',index='end',iid = count,text='',values=(record[0],record[1],record[2],record[3],record[4]))
           
            count += 1

        backtosearchbtn= Button(win,text= "Back to Search Function", command = win.destroy)
        backtosearchbtn.pack()

        win.mainloop()
        
    def memsearch():
        win = Tk()
        win.title('Member Search')
        win.geometry("900x600")
        label = Label(win, text = "Book On Loan To Member",
                      font=("Arial", 15), relief = RIDGE, padx = 50, pady = 30)
        label.grid(row=0, column = 2, columnspan = 2)

        def searchmember():

            win=Tk()

            win.title('Member Report')
            win.geometry('500x500')
            label = Label(win, text = "Books on Loan to Member",
                        font=("Arial", 15), relief = RIDGE, padx = 50, pady = 30)
            label.pack(pady = 20)

            book_frame = Frame(win)
            book_frame.pack()

            #scrollbar
            book_scrolly = Scrollbar(book_frame)
            book_scrolly.pack(side=RIGHT, fill=Y)

            book_scrollx = Scrollbar(book_frame,orient='horizontal')
            book_scrollx.pack(side= BOTTOM,fill=X)

            set = ttk.Treeview(book_frame,yscrollcommand=book_scrolly.set, xscrollcommand =book_scrollx.set)



            set.pack()
            book_scrolly.config(command=set.yview)
            book_scrollx.config(command=set.xview)




            set['columns']= ('Accession Number', 'Title','Authors','ISBN','Publisher','Year')
            set.column("#0", width=0,  stretch=NO)
            set.column("Accession Number",anchor=CENTER, width=80)
            set.column("Title",anchor=CENTER, width=80)
            set.column("Authors",anchor=CENTER, width=80)
            set.column("ISBN",anchor=CENTER, width=80)
            set.column("Publisher",anchor=CENTER, width=80)
            set.column("Year",anchor=CENTER, width=80)

            set.heading("#0",text="",anchor=CENTER)
            set.heading("Accession Number",text="Accession Number",anchor=CENTER)
            set.heading("Title",text="Title",anchor=CENTER)
            set.heading("Authors",text="Authors",anchor=CENTER)
            set.heading("ISBN",text="ISBN",anchor=CENTER)
            set.heading("Publisher",text="Publisher",anchor=CENTER)
            set.heading("Year",text="Year",anchor=CENTER)

            #data
            #getdata function based on input
            #output to be ['Accession Number', 'Title','Authors','ISBN','Publisher','Year']
            #data = getdata
            data  = display_member_loans(memidentry.get())


            global count
            count=0
            
            for record in data:
            
                set.insert(parent='',index='end',iid = count,text='',values=(record[0],record[1],record[2],record[3],record[4],record[5]))
            
                count += 1

            backtosearchbtn= Button(win,text= "Back to Search Function", command = win.destroy)
            backtosearchbtn.pack()

            win.mainloop()

            

        global memid
        memid = StringVar()
        memidlbl= Label(win, text = "Membership ID", padx = 50, pady=30)
        memidlbl.grid(row=1,column=1)
        memidentry= Entry(win, textvariable=memid)
        memidentry.grid(row=1,column=2, columnspan=2)

        
        

        

        
       

        backtoreportbtn= Button(win,text="Back to Reports Menu",command = win.destroy)
        backtoreportbtn.grid(row=2, column = 4)

        searchmemberbtn = Button(win,text = "Search Member" , command = searchmember)
        searchmemberbtn.grid(row =2, column = 1)
        
        

        win.mainloop()

        

    
    reportlbl = Label(win, text = "Report", font = ("Arial",25), relief = RIDGE , width = 15, height = 10)
    reportlbl.grid( row =2 , rowspan=5 , padx = 10, column =1)
    booksearchlbl = Label(win, text="A member can perform a search on the collection of books.",wraplength=300, justify='left')
    booksearchlbl.grid (row =2 , column = 4)
    
    booksearchbtn = Button(win, text = "Search A Book" , width = 15, height = 3, command = booksearch)
    booksearchbtn.grid(row=2, column = 3 ,pady= 10)

    loanreportlbl = Label(win, text="This function displays all the books currently on loan to members.",wraplength=300, justify='left')
    loanreportlbl.grid (row =3 , column = 4)
    
    loanreportbtn = Button(win, text = "Books on loan" , width = 15, height = 3, command = loanreport)
    loanreportbtn.grid(row =3 , column =3 , pady=10)
    
   

    resreportlbl = Label(win, text="This function displays all the books that members have reserved.",wraplength=300, justify='left')
    resreportlbl.grid (row =5 , column = 4)
    
    resreportbtn = Button(win, text = "Books on Reservation" , width = 15, height = 3, command = resreport)
    resreportbtn.grid(row=5, column = 3 ,pady= 10)

    finereportlbl = Label(win, text="This function displays all the members with outstanding fines.",wraplength=300, justify='left')
    finereportlbl.grid (row =6 , column = 4)
    
    finereportbtn = Button(win, text = "Outstanding Fines" , width = 15, height = 3, command = finereport)
    finereportbtn.grid(row=6, column = 3 ,pady= 10)

    memloanlbl = Label(win, text="This function displays all the books a member identified by the membership id has borrowed.",wraplength=300, justify='left') 
    memloanlbl.grid (row =7 , column = 4)
    
    memloanbtn = Button(win, text = "Books on Loan to Member" , width = 15, height = 3, command = memsearch)
    memloanbtn.grid(row=7, column = 3 ,pady= 10)
    

    

    



    
    backtomainbtn = Button(win, text="Back to Main Menu", command = win.destroy)
    backtomainbtn.grid(row = 8, column = 4,  pady =10)
    win.mainloop()

root = Tk()
root.geometry('900x600')
root.title("A Library System")

label = Label(root, text = "(ALS)", font=("Arial", 40))


membershipButton = Button(root, text="Membership", command = membershipbutton,
                          width = 15, height = 5, font=("Arial", 15))
booksButton = Button(root, text="Books", command = booksbutton,
                     width = 15, height = 5, font=("Arial", 15))
loanButton = Button(root, text="Loans", command = loansbutton,
                    width = 15, height = 5, font=("Arial", 15))
reservationsButton = Button(root, text="Reservations", command = reservationsbutton,
                            width = 15, height = 5, font=("Arial", 15))
finesButton = Button(root, text="Fines", command = finesbutton,
                     width = 15, height = 5, font=("Arial", 15))
reportsButton = Button(root, text="Reports", command = reportsbutton,
                       width = 15, height = 5, font=("Arial", 15))



label.grid(row = 0, column = 0, columnspan = 3, padx = 50, pady = 50)
membershipButton.grid(row = 1, column = 0, padx = 50, pady = 10)
booksButton.grid(row = 1, column = 1, padx = 50, pady = 10)
loanButton.grid(row = 1, column = 2, padx = 50, pady = 10)
reservationsButton.grid(row = 2, column = 0, padx = 50, pady = 10)
finesButton.grid(row = 2, column = 1, padx = 50, pady = 10)
reportsButton.grid(row = 2, column = 2, padx = 50, pady = 10)


root.mainloop()




