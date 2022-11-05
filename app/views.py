from flask import render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from flask_mail import Message
from forms import LoginForm, SendEmailForm, RegistrationForm, UpdateAccountForm
from models import User, SendMail
from app import app, bcrypt, mail_app, db
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for('send_email'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password.encode('utf-8'), form.password.data):  #utf- unicode tranformation format - 8bit password-most effecient
                login_user(user)
                return redirect(url_for('send_email'))
    return render_template("login.html", title='Login', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('send_email'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username==form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password.encode('utf-8'), form.password.data):
                login_user(user)
                return redirect(url_for('send_email'))
    return render_template('login.html', title='Login', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('send_email'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password =hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/email', methods=['GET', 'POST'])
@login_required
def send_email():
    form = SendEmailForm()
    if form.validate_on_submit():
        send_mail =  SendMail(email = form.email.data, subject = form.subject.data, message = form.message.data, user_id = current_user.id)
        db.session.add(send_mail)
        db.session.commit()
        message = Message(
            subject=form.subject.data,
            recipients=[form.email.data])
        message.body = form.message.data
        mail_app.send(message)
        flash('Your mail has been Sent', 'success')
        return redirect(url_for('home'))
    return render_template('compose.html', form=form)


@app.route("/sent_mails")
@login_required
def sent_mail_data():
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    mails = SendMail.query.filter(SendMail.user_id == current_user.id)
    # mails = SendMail.query.all()
    return render_template('home.html', mails=mails)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('register'))


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        db.session.commit()
        flash('Your account has been updated')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
    return render_template('account.html', title='Account', form=form)

@app.route("/mails/<int:mail_id>/delete", methods=['POST'])
@login_required
def delete_mail(mail_id):
    mails = SendMail.query.filter(SendMail.id==(mail_id)).first()
    db.session.delete(mails)
    db.session.commit()
    flash('Your mail has been deleted!', 'success')
    return redirect(url_for('sent_mail_data'))

# @app.route("/mails/delete", methods=['GET'])
# @login_required
# def delete_mailsss():
#     try:
#         num_rows_deleted = db.session.query(SendMail).delete()
#         db.session.commit()
#     except:
#         db.session.rollback()