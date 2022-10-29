from main import Session, engine, Member

local_session = Session(bind = engine)

def update_name(id, new):
    user_to_update = local_session.query(Member).filter(Member.membershipid == id).first()
    user_to_update.name = new
    local_session.commit()

# update other stuff
def update_faculty(id, new):
    user_to_update = local_session.query(Member).filter(Member.membershipid == id).first()
    user_to_update.faculty = new
    local_session.commit()

def update_phone(id, new):
    user_to_update = local_session.query(Member).filter(Member.membershipid == id).first()
    user_to_update.phonenumber = new
    local_session.commit()

def update_email(id, new):
    user_to_update = local_session.query(Member).filter(Member.membershipid == id).first()
    user_to_update.email = new
    local_session.commit()

#update_name("member", "new name")