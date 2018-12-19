from app import app, db
from app.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm, AddPeopleForm, ModifyPeopleForm, SearchPeopleForm, AddProfileNotesForm
from app.models import User, People
from app.email import send_password_reset_email
from app.queryfunc import create_people, create_people, edit_people, get_people, search_names, view_buyer_prospects, view_buyer_clients, view_seller_prospects, view_seller_clients, add_profile_note, view_profile_notes
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from flask_weasyprint import HTML, render_pdf
import datetime

now=datetime.datetime.now()



@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template("index.html", title='Index')

@app.route('/search_people', methods=['GET', 'POST'])
@login_required
def search_people():
    if request.method == "POST":
        search_string = request.form.get('search_string', '')
        return redirect(url_for('search_result', search_entry=search_string))
    return render_template("search_people.html", title='Search for People')

@app.route('/search_result/<search_entry>', methods=['GET', 'POST'])
@login_required
def search_result(search_entry):
    searchresult=search_names(current_user, search_entry)
    return render_template("search_result.html", title="Search Result", search_entry=search_entry, searchresult=searchresult)

@app.route('/people', methods=['GET'])
@login_required
def people():
    all_people = get_people(current_user=current_user)
    return render_template('people.html', title='People', all_people=all_people)

@app.route('/buyer_prospects', methods=['GET'])
@login_required
def buyer_prospects():
    buyerprospects=view_buyer_prospects(current_user=current_user)
    return render_template('buyer_prospects.html', title='Buyer Prospects', buyerprospects=buyerprospects)

@app.route('/buyer_clients', methods=['GET'])
@login_required
def buyer_clients():
    buyerclients=view_buyer_clients(current_user=current_user)
    return render_template('buyer_clients.html', title='Buyer Clients', buyerclients=buyerclients)

@app.route('/seller_prospects', methods=['GET'])
@login_required
def seller_prospects():
    sellerprospects=view_seller_prospects(current_user=current_user)
    return render_template('seller_prospects.html', title='Seller Prospects', sellerprospects=sellerprospects)

@app.route('/seller_clients', methods=['GET'])
@login_required
def seller_clients():
    sellerclients=view_seller_clients(current_user=current_user)
    return render_template('seller_clients.html', title='Seller Clients', sellerclients=sellerclients)

@app.route('/view_people/<people_id>', methods=['GET', 'POST'])
@login_required
def view_people(people_id):
    currentuser = User.query.filter_by(username=current_user.username).first()
    account_pk = currentuser.id
    select_people = People.query.filter_by(user_account_pk=account_pk, id=people_id).first()
    user_account_pk = account_pk
    pnotes=view_profile_notes(current_user=current_user, people_account_pk=people_id)
    form = ModifyPeopleForm(modified_first_name=select_people.first_name, modified_last_name=select_people.last_name, 
                modified_phone_cell=select_people.phone_cell, modified_notes=select_people.notes,
                modified_ptype=select_people.ptype, modified_pstatus=select_people.pstatus)
    notes_form = AddProfileNotesForm()
    #viewpnotes=view_profile_notes(current_user=current_user, people_account_pk=people_id)
    if notes_form.validate_on_submit():
        profile_note=notes_form.pnotes.data
        profile_note_storage=add_profile_note(current_user=current_user, pnotes=profile_note, people_account_pk=people_id, people_id=people_id)
        if profile_note_storage == True:
            flash('Notes Added.')
            return redirect(url_for('view_people', people_id=people_id))
        else:
            flash('Something is wrong, note not added.')
    if form.validate_on_submit():
        select_people.first_name=form.modified_first_name.data
        select_people.last_name=form.modified_last_name.data
        select_people.phone_cell=form.modified_phone_cell.data
        select_people.notes=form.modified_notes.data
        select_people.ptype=form.modified_ptype.data
        select_people.pstatus=form.modified_pstatus.data
        db.session.commit()
        flash('Your Persons Information has been modified.')
        return redirect(url_for('view_people', people_id=people_id))
        #return redirect('/view_people/<people_id>')

        #flash('You CLICKED IT')
        #return redirect(url_for('/view_people/<people_id>'))
    return render_template('view_people.html', title = 'View Person', select_people=select_people, form=form, notes_form=notes_form, viewpnotes=pnotes)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        account=User.query.filter_by(username=form.username.data).first()
        if account is None or not account.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(account, remember=form.remember_me.data)
        next_page=request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/add_people', methods=['GET', 'POST'])
@login_required
def add_people():
    form = AddPeopleForm()
    if form.validate_on_submit():
        people_create = create_people(current_user=current_user, first_name=form.first_name.data, last_name=form.last_name.data, phone_cell=form.phone_cell.data, ptype=form.ptype.data, pstatus=form.pstatus.data, notes=form.notes.data)
        if people_create == True:
            flash('Congradulations, you added the Person to your CRM!')
            return redirect(url_for('people'))
        elif people_create == False:
            flash('Something is wrong. Try again!')
    return render_template('add_people.html', title='Add People', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congradulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html', title='Reset Password', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)

@app.route('/hello_<fname>_<lname>.pdf')
def hello_pdf(fname, lname):
    #currentuser = User.query.filter_by(username=current_user.username).first()
    #account_pk = currentuser.id
    #select_people = People.query.filter_by(user_account_pk=account_pk, id=people_id).first()
    html = render_template('peoplepdf.html', fname=fname, lname=lname, day=now.day, month=now.month, year=now.year, endyear=now.year+1)
    return render_pdf(HTML(string=html))