from app import app, db
from app.models import User, People, ProfileNotes, ClosedDeals



def create_people(current_user, first_name, last_name, phone_cell, ptype, pstatus, notes, house_number, street_name, city_name, state_name, zip_code):
    currentuser = User.query.filter_by(username=current_user.username).first()
    user_account_pk = currentuser.id
    new_people = People(first_name=first_name, last_name=last_name, 
            phone_cell=phone_cell, ptype=ptype, pstatus=pstatus, notes=notes, 
            house_number=house_number, street_name=street_name, city_name=city_name, state_name=state_name, zip_code=zip_code,
            user_account_pk=user_account_pk)
    db.session.add(new_people)
    db.session.commit()
    return True

#def total_sales(current_user):
#    currentuser = User.query.filter_by(username=current_user.username).first()
#    user_account_pk = currentuser.id
#    all_closed = ClosedDeals.query.filter_by(user_account_pk=user_account_pk).all()
#    for price in all_closed:
#        print(price)

    #final_tally = 0
    #for sales in alldeals[9]:
        #final_tally = final_tally + sales
    #return final_tally


def add_profile_note(current_user, pnotes, people_account_pk):
    currentuser = User.query.filter_by(username=current_user.username).first()
    user_account_pk = currentuser.id
    new_profile_note = ProfileNotes(pnotes=pnotes, people_account_pk=people_account_pk, user_account_pk=user_account_pk)
    db.session.add(new_profile_note)
    db.session.commit()
    return True

def view_closed_deals(current_user):
    currentuser = User.query.filter_by(username=current_user.username).first()
    user_account_pk = currentuser.id
    all_closed = ClosedDeals.query.filter_by(user_account_pk=user_account_pk).all()
    return all_closed


def delete_client(user_account_pk, people_id):
    delete_c = People.query.filter_by(user_account_pk=user_account_pk, id=people_id).first()
    db.session.delete(delete_c)
    db.session.commit()
    return True

def convertclient(user_account_pk, people_id):
    convert_cl = People.query.filter_by(user_account_pk=user_account_pk, id=people_id).first()
    add_sale = ClosedDeals(first_name=convert_cl.first_name, last_name=convert_cl.last_name, 
        phone_cell=convert_cl.phone_cell, ptype=convert_cl.ptype, house_number=convert_cl.house_number, 
        street_name=convert_cl.street_name, city_name=convert_cl.city_name, state_name=convert_cl.state_name,
        zip_code=convert_cl.zip_code, price=convert_cl.price, 
        user_account_pk=convert_cl.user_account_pk)
    db.session.add(add_sale)
    db.session.commit()
    return True


def view_profile_notes(current_user, people_account_pk):
    currentuser = User.query.filter_by(username=current_user.username).first()
    account_pk = currentuser.id
    pnotes = ProfileNotes.query.filter_by(user_account_pk=account_pk, people_account_pk=people_account_pk).all()
    return pnotes

def view_buyers(current_user):
    currentuser = User.query.filter_by(username=current_user.username).first()
    account_pk = currentuser.id
    all_buyers=People.query.filter_by(user_account_pk=account_pk, ptype="buyer").all()
    return all_buyers

def view_buyer_prospects(current_user):
    currentuser = User.query.filter_by(username=current_user.username).first()
    account_pk = currentuser.id
    buyerprospects=People.query.filter_by(user_account_pk=account_pk, ptype="buyer", pstatus="prospect").all()
    return buyerprospects

#def select_person(current_user, first_name, last_name):
#    currentuser = User.query.filter_by(username=current_user.username).first()
#    account_pk = currentuser.id
#    person_selected=
#    return person_selected

def view_buyer_clients(current_user):
    currentuser = User.query.filter_by(username=current_user.username).first()
    account_pk = currentuser.id
    buyerclients=People.query.filter_by(user_account_pk=account_pk, ptype="buyer", pstatus="client").all()
    return buyerclients

def view_sellers(current_user):
    currentuser = User.query.filter_by(username=current_user.username).first()
    account_pk = currentuser.id
    all_sellers=People.query.filter_by(user_account_pk=account_pk, ptype="seller").all()
    return all_sellers

def view_seller_prospects(current_user):
    currentuser = User.query.filter_by(username=current_user.username).first()
    account_pk = currentuser.id
    sellerprospects=People.query.filter_by(user_account_pk=account_pk, ptype="seller", pstatus="prospect").all()
    return sellerprospects

def view_seller_clients(current_user):
    currentuser = User.query.filter_by(username=current_user.username).first()
    account_pk = currentuser.id
    sellerclients=People.query.filter_by(user_account_pk=account_pk, ptype="seller", pstatus="client").all()
    return sellerclients



#for loggin purposes, you will have to add some sort of tracking as to which user edits
#which information for which people
def edit_people(current_user, first_name, last_name, phone_cell):
    currentuser = User.query.filter_by(username=current_user.username).first()
    user_account_pk = currentuser.id
    #TODO FINISH THIS

def get_people(current_user):
    currentuser = User.query.filter_by(username=current_user.username).first()
    account_pk = currentuser.id
    all_people=People.query.filter_by(user_account_pk=account_pk).all()
    return all_people

#def add_people_notes(current_user, select_people, pnotes):
    #currentuser = User.query.filter_by(username=current_user.username).first()
    #IDENTIFY USER WITH USERACCOUNTPK
    #user_account_pk = currentuser.id
    #people_account_pk = select_people.id
    #new_people_note = 
    #pass


def search_names(current_user, search_entry):
    currentuser = User.query.filter_by(username=current_user.username).first()
    account_pk = currentuser.id
    people_first_names=People.query.filter_by(user_account_pk=account_pk).filter(People.first_name.contains(search_entry)).all()
    people_last_names=People.query.filter_by(user_account_pk=account_pk).filter(People.last_name.contains(search_entry)).all()
    results_list=people_first_names+people_last_names
    return results_list

#FOR NOW, THE MODIFY_PROSPECT IS WRITTEN INTO THE ROUTE
#def modify_prospect(current_user, first_name, last_name, modified_first_name, modified_last_name, modified_phone_cell):
#    currentuser = User.query.filter_by(username=current_user.username).first()
#    account_pk = currentuser.id
#    select_prospect = Prospects.query.filter_by(user_account_pk=account_pk, first_name=first_name, last_name=last_name).first()
#    select_prospect.first_name = modified_first_name
#    select_prospect.last_name = modified_last_name
#    select_prospect.phone_cell = modified_phone_cell
#    db.session.commit
#    return True

#FOR NOW, THE MODIFY_CLIENT IS WRITTEN INTO THE ROUTE
#def modify_client(current_user, first_name, last_name, modified_first_name, modified_last_name, modified_phone_cell):
#    currentuser = User.query.filter_by(username=current_user.username).first()
#    account_pk = currentuser.id
#    select_client = Clients.query.filter_by(user_account_pk=account_pk, first_name=first_name, last_name=last_name).first()
#    select_client.first_name = modified_first_name
#    select_client.last_name = modified_last_name
#    select_client.phone_cell = modified_phone_cell
#    db.session.commit
#    return True

 
#def select_prospect(current_user, first_name, last_name):
#    currentuser = User.query.filter_by(username=current_user.username).first()
#    account_pk = currentuser.id
#    prospect = Prospects.query.filter_by(user_account_pk=account_pk, first_name=first_name, last_name=last_name).first()
#    return prospect
#    #TODO FINISH THIS FUNCTION TO RETURN CURRENT PROSPECT!!
