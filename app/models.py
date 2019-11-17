from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app import db, login


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    # email is also the username
    email = db.Column(db.String(45), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    agent_id = db.Column(db.Integer, db.ForeignKey('agent.id'), nullable=True)
    last_login = db.Column(db.DateTime, nullable=True)
    update_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    create_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # generate hash of given password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # return hash of given password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # allows you to check what role user is, returns true or false
    def is_role(self, role_name):
        return self.role.name == role_name

    def get_role(self):
        return self.role.name

    # get all users by role, returns all users of given role
    @staticmethod
    def get_all_users(role_name):
        return User.query.join(Role).filter(Role.name == role_name).all()

    # update last login date to now
    def stamplogin(self):
        self.last_login = datetime.utcnow()
        db.session.commit()

    # creates token of user object
    # decode('utf-8') converts token to string
    def get_reset_password_token(self, expires_in=current_app.config['FORGOT_PASSWORD_TOKEN_EXPIRE']):
        return jwt.encode(
            {'reset_password': self.id, 'exp': datetime.utcnow() + timedelta(seconds=expires_in)},
            current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    # decodes token and returns user object
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def __repr__(self):
        return '<User {}>'.format(self.email)


class Agent(db.Model):
    __tablename__ = 'agent'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45), nullable=False)
    last_name = db.Column(db.String(45), nullable=False)
    phone = db.Column(db.String(45), nullable=False)
    agency_name = db.Column(db.String(45), nullable=False)
    create_date = db.Column(db.DateTime(), default=datetime.utcnow, nullable=False)
    update_date = db.Column(db.DateTime(), default=datetime.utcnow, nullable=False)
    user = db.relationship('User', backref='agent', uselist=False)

    def __repr__(self):
        return '<Agent {}>'.format(self.email)


# This allows application to freely call User methods even if you're not logged in
class AnonymousUser(AnonymousUserMixin):
    def set_password(self, password):
        return False

    def check_password(self, password):
        return False

    def is_role(self, role_name):
        return False

    def stamplogin(self):
        return False


# This tells flask login which class to use if user is not logged in
login.anonymous_user = AnonymousUser


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    # get the role object given role name
    @staticmethod
    def get_role(role_name):
        return Role.query.filter_by(name=role_name).first()

    def __repr__(self):
        return '<Role {}>'.format(self.name)


class Student(db.Model):
    __tablename__='student'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(45), index=True, nullable=False)
    country_origin = db.Column(db.String(45), nullable=False)
    nationality = db.Column(db.String(45), nullable=False)
    dob = db.Column(db.DateTime(), nullable=False)
    education_level = db.Column(db.String(45), nullable=False)
    intended_city = db.Column(db.String(45), nullable=False)
    intended_course = db.Column(db.String(45), nullable=False)
    arrival_date = db.Column(db.DateTime(), nullable=False)
    stay_permanently = db.Column(db.Boolean, nullable=False)
    create_date = db.Column(db.DateTime(), default=datetime.utcnow, nullable=False)
    update_date = db.Column(db.DateTime(), default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return '<Student {}>'.format(self.email)


class Leads(db.Model):
    __tablename__ = 'leads'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(45), nullable=False)
    country_of_origin = db.Column(db.String(45))
    nationality = db.Column(db.String(45), nullable=False)
    date_of_birth = db.Column(db.DateTime())
    education = db.Column(db.String(45))
    target_city = db.Column(db.String(45), nullable=False)
    course = db.Column(db.String(45))
    arrival_date = db.Column(db.DateTime())
    stay_permanently_flag = db.Column(db.String(45), nullable=False)
    report_sent_flag = db.Column(db.String(45), nullable=False)
    school = db.Column(db.String(45), nullable=False)
    session_id = db.Column(db.String(100), nullable=False)
    download_count = db.Column(db.Integer())
    report_name = db.Column(db.String(100))

    def __repr__(self):
        return '<Leads {}>'.format(self.email)


class Contact(db.Model):
    __tablename__ = 'contact'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(3000), nullable=False)
    create_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

# Required by flask-login
# This callback is used to reload the user object from the user ID stored in the session
@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# CRICOS tables below
class Institute(db.Model):
    __tablename__ = 'institute'

    id = db.Column(db.Integer, primary_key=True)
    cricos_prov_code = db.Column(db.String(10), nullable=False)
    trading_name = db.Column(db.String(400))
    inst_name = db.Column(db.String(200))
    inst_type = db.Column(db.String(20))
    conditions = db.Column(db.String(1600))
    total_capacity = db.Column(db.Integer)
    website = db.Column(db.String(200))
    inst_post_address = db.Column(db.String(400))
    page = db.Column(db.Integer)
    update_date = db.Column(db.DateTime, default=datetime.utcnow)
    state = db.Column(db.String(30))

    # cascade all, delete so if you delete institute it will also delete amy orphans in linked tables
    # this seems only for python doesnt seem to work when running sql DELETE on mysql? See notes below for workaround.
    contact_principal = db.relationship('ContactPrincipal', backref='institute', lazy='dynamic')
    contact_int_student = db.relationship('ContactIntStudent', backref='institute', lazy='dynamic')
    course = db.relationship('Course', backref='institute', lazy='dynamic')


class ContactPrincipal(db.Model):
    __tablename__ = 'contact_principal'

    id = db.Column(db.Integer, primary_key=True)
    inst_id = db.Column(db.Integer, db.ForeignKey('institute.id'), nullable=False)
    name = db.Column(db.String(100))
    title = db.Column(db.String(200))
    phone = db.Column(db.String(100))
    fax = db.Column(db.String(100))
    page = db.Column(db.Integer)
    update_date = db.Column(db.DateTime, default=datetime.utcnow)


class ContactIntStudent(db.Model):
    __tablename__ = 'contact_int_student'

    id = db.Column(db.Integer, primary_key=True)
    inst_id = db.Column(db.Integer, db.ForeignKey('institute.id'), nullable=False)
    name = db.Column(db.String(100))
    title = db.Column(db.String(200))
    phone = db.Column(db.String(100))
    fax = db.Column(db.String(100))
    email = db.Column(db.String(100))
    page = db.Column(db.Integer)
    update_date = db.Column(db.DateTime, default=datetime.utcnow)


class Course(db.Model):
    __tablename__ = 'course'

    id = db.Column(db.Integer, primary_key=True)
    inst_id = db.Column(db.Integer, db.ForeignKey('institute.id'), nullable=False)
    course_name = db.Column(db.String(200))
    course_sector = db.Column(db.String(200))
    cricos_course_code = db.Column(db.String(50), nullable=False)
    vet_nat_code = db.Column(db.String(200))
    dual_qual = db.Column(db.String(200))
    broad_field = db.Column(db.String(200))
    narrow_field = db.Column(db.String(200))
    detailed_field = db.Column(db.String(200))
    course_level = db.Column(db.String(200))
    foundation_studies = db.Column(db.String(200))
    work_component = db.Column(db.String(200))
    course_language = db.Column(db.String(200))
    duration = db.Column(db.String(200))
    tution_fee = db.Column(db.String(100))
    non_tution_fee = db.Column(db.String(100))
    total_cost = db.Column(db.String(100))
    page = db.Column(db.Integer)
    state = db.Column(db.String(30))
    update_date = db.Column(db.DateTime, default=datetime.utcnow)
    course_location = db.relationship('CourseLocation', backref='course', lazy='dynamic')


class CourseLocation(db.Model):
    __tablename__ = 'course_location'

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    location = db.Column(db.String(1000))
    page = db.Column(db.Integer)
    update_date = db.Column(db.DateTime, default=datetime.utcnow)





