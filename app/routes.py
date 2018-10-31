from app import app, db
from app.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm, AddProspectForm, AddClientForm, ModifyProspectForm, ModifyClientForm, SearchClientForm
from app.models import User, Prospects, Clients
from app.email import send_password_reset_email
from app.queryfunc import create_prospect, create_client, edit_prospect, get_prospects, get_clients, upgrade_prospect_client, search_names
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from pandas_datareader import data
import datetime
from bokeh.plotting import figure, show, output_file
from bokeh.embed import components
from bokeh.resources import CDN


@app.route('/')
@app.route('/index')
@login_required
def index():
    def inc_dec(c, o):
        if c > o:
            value="Increase"
        elif c < o:
            value="Decrease"
        else:
            value="Equal"
        return value

    start=datetime.datetime(2018,1,1)
    end=datetime.datetime(2018,10,29)
    df = data.DataReader(name="JPM", data_source="yahoo", start=start, end=end)
    df["Status"]=[inc_dec(c,o) for c, o in zip(df.Close, df.Open)]
    df["Middle"]=(df.Open+df.Close)/2
    df["Height"]=abs(df.Close-df.Open)
    p=figure(title="Candelstick Chart", x_axis_type='datetime', width=1000, height=300)
    p.grid.grid_line_alpha=0.3
    hours_12=12*60*60*1000
    p.segment(df.index, df.High, df.index, df.Low, color="Black")
    p.rect(df.index[df.Status=="Increase"], df.Middle[df.Status=="Increase"],
                hours_12, df.Height[df.Status=="Increase"], fill_color="#CCFFFF", line_color="black")
    p.rect(df.index[df.Status=="Decrease"], df.Middle[df.Status=="Decrease"],
                hours_12, df.Height[df.Status=="Decrease"], fill_color="#FF3333", line_color="black")

    script1, div1 = components(p)
    cdn_js=CDN.js_files
    cdn_css=CDN.css_files
    return render_template("index.html", title='Index', script1=script1, div1=div1, cdn_js=cdn_js[0], cdn_css=cdn_css[0])

@app.route('/search_client', methods=['GET', 'POST'])
@login_required
def search_client():
    form = SearchClientForm()
    if form.validate_on_submit():
        search_entry = form.first_last.data
        return redirect('/search_result/{}'.format(search_entry))
    return render_template("search_client.html", title='Search for Prospect/Client', form=form)

@app.route('/search_result/<search_entry>', methods=['GET', 'POST'])
@login_required
def search_result(search_entry):
    #current_holding_shares = get_holding(current_user=current_user, ticker_symbol=ticker_symbol)
    #tran_history = get_specific_orders(current_user=current_user, ticker_symbol=ticker_symbol)
    #current_price = quote(ticker_symbol)
    #if current_holding_shares:
    #    current_value = current_price * current_holding_shares
    #else:
    #    current_value = 0
    searchresult=search_names(current_user, search_entry)
    return render_template("search_result.html", title="Search Result", search_entry=search_entry, searchresult=searchresult)

@app.route('/listings', methods=['GET'])
@login_required
def listings():
    all_clients = get_clients(current_user=current_user)
    return render_template('listings.html', title='Listings', all_clients=all_clients)

@app.route('/prospects', methods=['GET'])
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
    form = ModifyProspectForm(modified_first_name=select_prospect.first_name, modified_last_name=select_prospect.last_name, modified_phone_cell=select_prospect.phone_cell, modified_notes=select_prospect.notes)
    if form.validate_on_submit():
        select_prospect.first_name=form.modified_first_name.data
        select_prospect.last_name=form.modified_last_name.data
        select_prospect.phone_cell=form.modified_phone_cell.data
        select_prospect.notes=form.modified_notes.data
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
    form = ModifyClientForm(modified_first_name=select_client.first_name, modified_last_name=select_client.last_name, modified_phone_cell=select_client.phone_cell, modified_notes=select_client.notes)
    if form.validate_on_submit():
        select_client.first_name=form.modified_first_name.data
        select_client.last_name=form.modified_last_name.data
        select_client.phone_cell=form.modified_phone_cell.data
        select_client.notes=form.modified_notes.data
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
