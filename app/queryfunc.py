from app import app, db
from app.models import User, Prospects, Clients



def create_prospect(current_user, first_name, last_name, phone_cell):
    currentuser = User.query.filter_by(username=current_user.username).first()
    user_account_pk = currentuser.id
    new_prospect = Prospects(first_name=first_name, last_name=last_name, phone_cell=phone_cell, user_account_pk=user_account_pk)
    db.session.add(new_prospect)
    db.session.commit()
    return True



def create_client(current_user, first_name, last_name, phone_cell):
    currentuser = User.query.filter_by(username=current_user.username).first()
    user_account_pk = currentuser.id
    new_client = Clients(first_name=first_name, last_name=last_name, phone_cell=phone_cell, user_account_pk=user_account_pk)
    db.session.add(new_client)
    db.session.commit()
    return True
    

#for loggin purposes, you will have to add some sort of tracking as to which user edits
#which information for which prospects
def edit_prospect(current_user, first_name, last_name, phone_cell):
    currentuser = User.query.filter_by(username=current_user.username).first()
    user_account_pk = currentuser.id
    #TODO FINISH THIS

def get_prospects(current_user):
    currentuser = User.query.filter_by(username=current_user.username).first()
    account_pk = currentuser.id
    all_prospects=Prospects.query.filter_by(user_account_pk=account_pk).all()
    return all_prospects

def get_clients(current_user):
    currentuser = User.query.filter_by(username=current_user.username).first()
    account_pk = currentuser.id
    all_clients=Clients.query.filter_by(user_account_pk=account_pk).all()
    return all_clients

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

def upgrade_prospect_client(current_user, first_name, last_name, phone_cell):
    currentuser = User.query.filter_by(username=current_user.username).first()
    account_pk = currentuser.id
    select_prospect = Prospects.query.filter_by(user_account_pk=account_pk, first_name=first_name, last_name=last_name, phone_cell=phone_cell).first()
    #FINISH THIS

def search_names(current_user, search_entry):
    currentuser = User.query.filter_by(username=current_user.username).first()
    account_pk = currentuser.id
    client_first_names=Clients.query.filter_by(user_account_pk=account_pk).filter(Clients.first_name.contains(search_entry)).all()
    client_last_names=Clients.query.filter_by(user_account_pk=account_pk).filter(Clients.last_name.contains(search_entry)).all()
    prospect_first_names=Prospects.query.filter_by(user_account_pk=account_pk).filter(Prospects.first_name.contains(search_entry)).all()
    prospect_last_names=Prospects.query.filter_by(user_account_pk=account_pk).filter(Prospects.last_name.contains(search_entry)).all()
    results_list=client_first_names+client_last_names+prospect_first_names+prospect_last_names
    return results_list