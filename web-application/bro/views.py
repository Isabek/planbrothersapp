from bro.forms import SignInForm, SignUpForm
from bro.models import Bro
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
from main.extensions import db

bro = Blueprint('bro', __name__)


@bro.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SignInForm()
    if request.method == "POST" and form.validate():
        registered_bro = Bro.query.filter_by(email=form.email.data).first()

        if registered_bro and registered_bro.is_correct_password(form.password.data):
            flash("Bro logged in successfully", 'info')
            login_user(registered_bro, remember=form.remember.data)
            return redirect(url_for('frontend.index'))

        flash("Email or Password is invalid.", "error")
        return redirect(url_for('bro.signin'))

    return render_template('bro/signin.html', form=form)


@bro.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if request.method == "POST" and form.validate():
        bro_model = Bro(username=form.username.data,
                        password=form.password.data,
                        email=form.email.data,
                        birthdate=form.birthdate.data)
        db.session.add(bro_model)
        db.session.commit()
        flash('Bro has been successfully registered.', 'info')
        return redirect(url_for('bro.signin'))

    return render_template('bro/signup.html', form=form)


@bro.route('/signout')
def signout():
    logout_user()
    flash("Bro logged out successfully", 'info')
    return redirect(url_for('frontend.index'))


@bro.route("/profile")
@login_required
def profile():
    return render_template('bro/profile.html')
