from bro.forms import SignInForm, SignUpForm, DeleteForm
from bro.models import Bro
from bro.sort_strategy import SortStrategy
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
from flask_paginate import Pagination
from main.extensions import db
from main.utils import current_user_exists, redirect_url

BROS_PER_PAGE = 12

bro = Blueprint('bro', __name__)


@bro.route('/signin', methods=['GET', 'POST'])
@current_user_exists
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
@current_user_exists
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
@login_required
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
    if request.method == "POST" and form.validate():
        db.session.delete(current_user)
        db.session.commit()
        flash("You profile has been successfully deleted", "info")
        return redirect(url_for('frontend.index'))
    return render_template('bro/delete_profile.html', form=form)


@bro.route("/bros")
def list_bros():
    page = abs(int(request.args.get('page', 1)))
    sort = str(request.args.get('sort', ''))

    sort_strategy = SortStrategy(strategy=sort)
    total, result = sort_strategy.get_result(page=page, per_page=BROS_PER_PAGE)

    pagination = Pagination(page=page, total=total,
                            search=False,
                            per_page=BROS_PER_PAGE,
                            css_framework='bootstrap3')

    return render_template('bro/list_bros.html', result=result, sort=sort, pagination=pagination)


@bro.route('/bros/<int:bro_id>')
def bro_profile(bro_id):
    bro_model = Bro.query.get(bro_id)
    if not bro_model:
        flash("Bro doesn't exist", 'error')
        return redirect(url_for('bro.list_bros'))
    return render_template('bro/bro_profile.html', bro=bro_model)


@bro.route('/bros/friend/<int:bro_id>')
@login_required
def friend_bro(bro_id):
    bro_model = Bro.query.get(bro_id)
    if not bro_model:
        flash("Bro doesn't exist", 'error')
        return redirect(redirect_url('bro.list_bros'))

    if current_user.id == bro_model.id:
        flash("Are you sure? :)", "error")
        return redirect(redirect_url('bro.list_bros'))

    current_user.befriend(bro_model)
    db.session.commit()
    flash("Bro has been successfully added as a friend", "info")
    return redirect(redirect_url('bro.list_bros'))


@bro.route("/bros/unfriend/<int:bro_id>")
@login_required
def unfriend_bro(bro_id):
    bro_model = Bro.query.get(bro_id)
    if not bro_model:
        flash("Bro doesn't exist", 'error')
        return redirect(redirect_url('bro.list_bros'))

    current_user.unfriend(bro_model)
    db.session.commit()
    flash("Bro has been successfully unfriended", "info")
    return redirect(redirect_url('bro.list_bros'))


@bro.route('/bros/best_friend/<int:bro_id>')
@login_required
def best_friend_bro(bro_id):
    bro_model = Bro.query.get(bro_id)

    if not bro_model:
        flash("Bro doesn't exist", 'error')
        return redirect(redirect_url('bro.list_bros'))

    if current_user.id == bro_model.id:
        flash("Are you sure? :)", "error")
        return redirect(redirect_url('bro.list_bros'))

    current_user.add_best_friend(bro_model)
    db.session.commit()
    flash("Bro has been successfully added as a best friend", "info")
    return redirect(redirect_url('bro.list_bros'))


@bro.route("/bros/remove_best_friend/<int:bro_id>")
@login_required
def remove_best_friend(bro_id):
    bro_model = Bro.query.get(bro_id)
    if not bro_model:
        flash("Bro doesn't exist", 'error')
        return redirect(redirect_url('bro.list_bros'))

    current_user.remove_best_friend(bro_model)
    db.session.commit()
    flash("Best Bro has been successfully unfriended", "info")
    return redirect(redirect_url('bro.list_bros'))
