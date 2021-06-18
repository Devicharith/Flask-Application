from flask import Blueprint,render_template,request,flash,redirect,url_for
from flask_login import login_user, login_required, logout_user, current_user
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from flask_mail import Mail,Message
from .models import User,Note
from .auth import s
from . import db

mail = Blueprint('mail',__name__)

@mail.route('/mail_sent/<token>')
def confirm_mail(token):
    email = s.loads(token, salt='email-confirm', max_age=3600)
    user = User.query.filter_by(email=email).first()
    print(user)
    if user:
        user.confirm = True
        db.session.commit()
        login_user(user, remember=True)
        flash('Logged in successfully!', category='success')
        return redirect(url_for('view.home'))
    else:
        flash('Your Link Has Expired!! Login Again')
        return redirect(url_for('auth.login'))
