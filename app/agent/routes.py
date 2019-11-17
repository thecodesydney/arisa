from flask import render_template, request, session
from flask_login import login_required
from app.agent import bp
from app.models import Leads, Institute, ContactPrincipal, ContactIntStudent, Course, CourseLocation, db
from sqlalchemy import or_


def get_sort_order(sort_order):
    if sort_order == 'coo':
        so = Leads.country_of_origin.asc()
    if sort_order == 'cou':
        so = Leads.course.asc()
    elif sort_order == 'edu':
        so = Leads.education.asc()
    elif sort_order == 'nat':
        so = Leads.nationality.asc()
    elif sort_order == 'sub':
        so = Leads.id.desc()
    elif sort_order == 'tar':
        so = Leads.target_city.asc()
    return so


# Agent main page
@bp.route('/agent_account', methods=['GET', 'POST'])
@login_required
def agent_account():
    # get page number from url. If no page number use page 1
    page = request.args.get('page', 1, type=int)

    # create session variables if doesn't exist, set to default
    if 'sort_order' not in session:
        session['sort_order'] = 'sub'
    if 'show_no_items' not in session:
        session['show_no_items'] = '10'
    if 'search_str' not in session:
        session['search_str'] = ''

    if request.method == 'POST':
        # Sort by
        if request.form['whichform'] == 'sortform':
            session['sort_order'] = request.form['sortform-value']
            session.modified = True
        # Show no of items
        elif request.form['whichform'] == 'showform':
            session['show_no_items'] = request.form['showform-value']
            session.modified = True
        # Search
        elif request.form['whichform'] == 'searchform':
            session['search_str'] = request.form['search-inp']
            session.modified = True

    # convert string to list for sql
    search_terms = session['search_str'].split()

    # if user performed a search
    if search_terms:
        # uses the SQL statement OR and IN equivalent
        # False means an empty list is returned if page no is empty
        stud_avail = Leads.query.filter(or_(Leads.nationality.in_(search_terms),
                                            Leads.target_city.in_(search_terms),
                                            Leads.course.in_(search_terms),
                                            Leads.education.in_(search_terms),
                                            Leads.country_of_origin.in_(search_terms))).\
            order_by(get_sort_order(session['sort_order'])).\
            paginate(page, int(session['show_no_items']), False)
    # user did not perform a search
    else:
        stud_avail = Leads.query.order_by(get_sort_order(session['sort_order'])).\
            paginate(page, int(session['show_no_items']), False)

    return render_template('agent/agent-account.html',
                           stud_avail=stud_avail,
                           sort_order=session['sort_order'],
                           show_no_items=session['show_no_items'],
                           search_str=session['search_str'])



