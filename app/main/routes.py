from flask import render_template, redirect, url_for, flash, current_app
from app.main import bp
from app.main.forms import ContactForm
from app.models import Contact
from app import db
from app.email import send_email


@bp.route('/')
def index():
    return render_template('main/index.html')


@bp.route('/about')
def about():
    return render_template('main/about.html')


def send_contact_email(cont):
    create_date = cont.create_date.strftime('%d/%m/%y %H:%M')
    rec = current_app.config['MAIL_ADMINS']
    return send_email('You have a new message from Arisa via the contact form',
                      sender=current_app.config['MAIL_FROM'],
                      recipients=rec.split(' '),
                      text_body=render_template('main/email_contact.txt', contact=cont, create_date=create_date),
                      html_body=render_template('main/email_contact.html', contact=cont, create_date=create_date))


@bp.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        cont = Contact(name=form.name.data, email=form.email.data, message=form.message.data)
        db.session.add(cont)
        db.session.commit()
        if send_contact_email(cont):
            flash('Message has been sent!')
        else:
            flash('Sorry system error')
        return redirect(url_for('main.index'))
    return render_template('main/contact.html', form=form)
