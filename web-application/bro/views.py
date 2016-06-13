from bro.forms import SignInForm, SignUpForm, DeleteForm
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
    if request.method == "POST" and form.validate_for_exist():
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


@bro.route("/profile/edit", methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = SignUpForm(request.form, obj=current_user)
    if request.method == "POST" and form.validate_for_exist(current_bro=current_user):
        form.populate_obj(current_user)
        db.session.commit()
        flash("You profile has been successfully updated.", "info")
    return render_template('bro/edit_profile.html', form=form)


@bro.route("/profile/delete", methods=['GET', 'POST'])
@login_required
def delete_profile():
    form = DeleteForm()
    if request.method == "POST":
        db.session.delete(current_user)
        db.session.commit()
        flash("You profile has been successfully deleted", "info")
        return redirect(url_for('frontend.index'))
    return render_template('bro/delete_profile.html', form=form)


@bro.route("/bros")
def list_bros():
    query = Bro.query
    if current_user:
        query = query.filter(Bro.id != current_user.id)
    bros = query.all()

    return render_template('bro/list_bros.html', bros=bros)
