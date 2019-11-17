from flask import render_template, redirect, url_for, flash, current_app, session
from flask_login import current_user, login_user, logout_user
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, AgentRegisterForm, ForgotPasswordForm, ResetPasswordForm
from app.models import User, Agent, Role
from app.email import send_email


def clear_session_var():
    # clear session variablea
    session.pop('sort_order', None)
    session.pop('show_no_items', None)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    clear_session_var()
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # dont allow login if username is incorrect, password is wrong
        if user is None or not user.check_password(form.password.data):
            flash('Login unsuccessful. Incorrect username / password.')
        else:
            # remember me keeps you logged in even after you close and open browser
            login_user(user, remember=form.remember_me.data)
            # update last login date
            if current_user.is_authenticated:
                current_user.stamplogin()
            flash(f'Hi {current_user.agent.first_name} {current_user.agent.last_name}, welcome back!')
            return redirect(url_for('agent.agent_account'))
    return render_template('auth/login.html', form=form)


@bp.route('/logout')
def logout():
    clear_session_var()
    if current_user.is_authenticated:
        logout_user()
        flash('You have successfully logged out')
    else:
        return redirect(url_for('main.index'))
    return redirect(url_for('main.index'))


@bp.route('/agent_registration', methods=['GET', 'POST'])
def agent_registration():
    form = AgentRegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        if User.query.filter(User.email == email).first() is not None:
            flash('Email has already been registered')
            return redirect(url_for('auth.agent_registration'))
        # create agent object first
        agent = Agent(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            phone=form.phone.data,
            agency_name=form.agency_name.data)
        db.session.add(agent)

        # create user object next
        role = Role.get_role('agent')
        # note the agent and role backrefs which creates the table relationships
        user = User(
            email=form.email.data,
            agent=agent,
            role=role)
        user.set_password(form.password.data)
        db.session.add(user)

        # commit both user and agent to database
        db.session.commit()

        # automatically log in user
        login_user(user)
        flash('You have successfully registered!')
        return redirect(url_for('agent.agent_account'))
    return render_template('auth/agent-registration.html', form=form)


# User to enter email address to send forgot password link to
@bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        # check that the email entered belongs to an existing user
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if send_password_reset_email(user):
                flash('Check your email for instructions to reset your password')
            else:
                flash('Sorry system error')
        else:
            flash('Email does not exist in our database')
            return redirect(url_for('auth.forgot_password'))
    return render_template('auth/forgot_password.html', form=form)


# Allow users to create new password
@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    # verify that the token is correct and still valid
    user = User.verify_reset_password_token(token)
    if not user:
        flash('Token has expired or is no longer valid')
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


##############################################################################
# Password reset
##############################################################################
def send_password_reset_email(user):
    token = user.get_reset_password_token()
    return send_email('Reset your password from arisa.com',
                      sender=current_app.config['MAIL_FROM'],
                      recipients=[user.email],
                      text_body=render_template('auth/email_reset_password.txt', user=user, token=token),
                      html_body=render_template('auth/email_reset_password.html', user=user, token=token))
