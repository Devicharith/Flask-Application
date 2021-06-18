from flask import Blueprint,render_template,request,flash,redirect,url_for
from .models import User,Note
from werkzeug.security import generate_password_hash, check_password_hash
from . import db,ma
from flask_login import login_user, login_required, logout_user, current_user
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from flask_mail import Mail,Message

s = URLSafeTimedSerializer("usbsusjjua")
auth = Blueprint('auth',__name__)

@auth.route('/login', methods = ['POST','GET'])
def login():
    if request.method =='POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                if user.confirm:
                    login_user(user, remember=True)
                    flash('Logged in successfully!', category='success')
                    return redirect(url_for('view.home'))
                else:
                    token = s.dumps(email, salt='email-confirm')
                    msg = Message('Confirm Email', sender='devicharith12@gmail.com', recipients=[email])
                    link = url_for('mail.confirm_mail', token=token, _external=True)
                    msg.body = 'Your link is {}'.format(link)
                    ma.send(msg)
                    return render_template('sendmail.html',mail = email,user = current_user)
            else:
                flash("Wrong Password")
        else:
            flash("NO mail-id found")
    return render_template('login.html',user = current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/Sign up', methods = ['POST','GET'])
def sign():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists!', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email = email, first_name = first_name, password = generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account Created')
            return redirect(url_for('view.home'))

    return render_template('signup.html',user = current_user)
