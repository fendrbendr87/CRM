from app import app, db
from app.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm, AddProspectForm, AddClientForm, ModifyProspectForm, ModifyClientForm
from app.models import User, Prospects, Clients
from app.email import send_password_reset_email
from app.queryfunc import create_prospect, create_client, edit_prospect, get_prospects, get_clients, upgrade_prospect_client
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template("index.html", title='Index')

@app.route('/listings', methods=['GET', 'POST'])
@login_required
def listings():
    all_clients = get_clients(current_user=current_user)
    return render_template('listings.html', title='Listings', all_clients=all_clients)

@app.route('/prospects', methods=['GET', 'POST'])
@login_required
def prospects():
    all_prospects = get_prospects(current_user=current_user)
    return render_template('prospects.html', title='Prospects', all_prospects=all_prospects)

@app.route('/view_prospect/<prospect_id>', methods=['GET', 'POST'])
@login_required
def view_prospect(prospect_id):
    currentuser = User.query.filter_by(username=current_user.username).first()
    account_pk = currentuser.id
    select_prospect = Prospects.query.filter_by(user_account_pk=account_pk, id=prospect_id).first()
    form = ModifyProspectForm(modified_first_name=select_prospect.first_name, modified_last_name=select_prospect.last_name, modified_phone_cell=select_prospect.phone_cell)
    if form.validate_on_submit():
        select_prospect.first_name=form.modified_first_name.data
        select_prospect.last_name=form.modified_last_name.data
        select_prospect.phone_cell=form.modified_phone_cell.data
        db.session.commit()
        flash('Your Prospect Information has been modified.')
        return redirect(url_for('prospects'))
    return render_template('view_prospect.html', title = 'View Prospect', select_prospect=select_prospect, form=form)

@app.route('/view_client/<client_id>', methods=['GET', 'POST'])
@login_required
def view_client(client_id):
    currentuser = User.query.filter_by(username=current_user.username).first()
    account_pk = currentuser.id
    select_client = Clients.query.filter_by(user_account_pk=account_pk, id=client_id).first()
    form = ModifyClientForm(modified_first_name=select_client.first_name, modified_last_name=select_client.last_name, modified_phone_cell=select_client.phone_cell)
    if form.validate_on_submit():
        select_client.first_name=form.modified_first_name.data
        select_client.last_name=form.modified_last_name.data
        select_client.phone_cell=form.modified_phone_cell.data
        db.session.commit()
        flash('Your Client Information has been modified.')
        return redirect(url_for('listings'))
    return render_template('view_client.html', title = 'View Client', select_client=select_client, form=form)

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

@app.route('/add_prospect', methods=['GET', 'POST'])
@login_required
def add_prospect():
    form = AddProspectForm()
    if form.validate_on_submit():
        prospect_create = create_prospect(current_user=current_user, first_name=form.first_name.data, last_name=form.last_name.data, phone_cell=form.phone_cell.data)
        if prospect_create == True:
            flash('Congradulations, you added the Prospect to your CRM!')
            return redirect(url_for('prospects'))
        elif prospect_create == False:
            flash('Something is wrong. Try again!')
    return render_template('add_prospect.html', title='Add Prospect', form=form)

@app.route('/add_client', methods=['GET', 'POST'])
@login_required
def add_client():
    form = AddClientForm()
    if form.validate_on_submit():
        client_create = create_client(current_user=current_user, first_name=form.first_name.data, last_name=form.last_name.data, phone_cell=form.phone_cell.data)
        if client_create == True:
            flash('Congradulations, you added the Client to your CRM!')
            return redirect(url_for('listings'))
        elif client_create == False:
            flash('Something is wrong. Try again!')
    return render_template('add_client.html', title='Add Client', form=form)

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
