''''
Admin Route deals with Reset Password functionality. On selection of the user, website will automatically generate reset password.
New Reset Password logic is first name of the user + "123". E,g. : "john123"
Author - Chintan Patel
Date - 29/SEp/2019
'''


from flask import render_template, redirect, url_for, flash, current_app, request, session
from app.admin import bp
from app.models import User, Agent, Leads, Institute, ContactPrincipal, ContactIntStudent, Course, CourseLocation, db
from flask_login import login_required
from app.admin.resetPasswordform import ResetPasswordForm
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, and_
from _datetime import datetime

#This route displays the list of the registered users in the website. The website user can select individual user whose password needs to
# reset.
@bp.route('/manage_password', methods=['GET', 'POST'])
@login_required
def manage_password():

    # create session variables if doesn't exist, set to default
    if 'search_str_reset_pwd' not in session:
        session['search_str_reset_pwd'] = ''
    if request.method == 'POST':
        if request.form['whichform'] == 'searchform':
            session['search_str_reset_pwd'] = request.form['search-inp-reset-pwd']
            session.modified = True

    # convert string to list for sql
    search_terms = session['search_str_reset_pwd'].split()

    # Print statements are to print it to command prompt. It helps in debugging.
    #print(search_terms)

    if search_terms:

        user_avail = User.query.outerjoin(Agent).filter(and_(User.agent_id == Agent.id,
                                                             or_(User.email.in_(search_terms),
                                                                 Agent.first_name.in_(search_terms),
                                                                 Agent.last_name.in_(search_terms),
                                                                 Agent.agency_name.in_(search_terms),
                                                                 Agent.phone.in_(search_terms),
                                                                 )))
        #Print statements are to print it to command prompt. It helps in debugging.
        #print(user_avail)
    else:
        user_avail = User.query.all()
    #user_avail = User.query.filter(User.email.like('chintan%'))
    return render_template('admin/admin.html', user_avail=user_avail, search_str_reset_pwd=session['search_str_reset_pwd'])



#This route will generate new system generated password. The logic for new system generated password is "first name of the user" followed by
# 123

# Reset Password
@bp.route('/reset_pass/<id>', methods=['GET'])
def reset_pass(id):

    # Print statements are to print it to command prompt. It helps in debugging.
    form = ResetPasswordForm()
    user = User.query.filter_by(id = id).first()
    #print(user)
    newPassword = user.agent.first_name.lower() + "123"
    #print('hello',user.agent.first_name)
    #print(newPassword)
    return render_template('admin/reset_password.html', user=user, newPassword=newPassword, form = form)


#This route will store the system generated password to the database.
#It will also update the update_date db field in the Table.
@bp.route('/submit_password', methods=['POST'])
def submit_password():

    # Print statements are to print it to command prompt. It helps in debugging.
    agentID = request.form['agentID']
    newResetPassword = request.form['newResetPassword']
    #print(agentID, newResetPassword)
    user = User.query.filter_by(agent_id = agentID).first()
    user.update_date = datetime.utcnow()
    user.set_password(newResetPassword)
    #print(datetime.utcnow())
    db.session.commit()
    flash('New Password has been reset succesfully')
    return render_template('main/index.html')

