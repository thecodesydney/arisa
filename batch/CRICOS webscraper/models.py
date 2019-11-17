from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import datetime

Base = declarative_base()


class Institute(Base):
    __tablename__ = 'institute'

    id = Column(Integer, primary_key=True)
    cricos_prov_code = Column(String(10), nullable=False)
    trading_name = Column(String(400))
    inst_name = Column(String(200))
    inst_type = Column(String(20))
    conditions = Column(String(1600))
    total_capacity = Column(Integer)
    website = Column(String(200))
    inst_post_address = Column(String(400))
    page = Column(Integer)
    update_date = Column(DateTime, default=datetime.datetime.utcnow)
    state = Column(String(30))

    # cascade all, delete so if you delete institute it will also delete amy orphans in linked tables
    # this seems only for python doesnt seem to work when running sql DELETE on mysql? See notes below for workaround.
    contact_principal = relationship("ContactPrincipal", cascade="all,delete-orphan", backref="institute")
    contact_int_student = relationship("ContactIntStudent", cascade="all,delete-orphan", backref="institute")
    course = relationship("Course", cascade="all,delete-orphan", backref="institute")


class ContactPrincipal(Base):
    __tablename__ = 'contact_principal'

    id = Column(Integer, primary_key=True)
    inst_id = Column(Integer, ForeignKey('institute.id'))
    name = Column(String(100))
    title = Column(String(200))
    phone = Column(String(100))
    fax = Column(String(100))
    page = Column(Integer)
    update_date = Column(DateTime, default=datetime.datetime.utcnow)


class ContactIntStudent(Base):
    __tablename__ = 'contact_int_student'

    id = Column(Integer, primary_key=True)
    inst_id = Column(Integer, ForeignKey('institute.id'))
    name = Column(String(100))
    title = Column(String(200))
    phone = Column(String(100))
    fax = Column(String(100))
    email = Column(String(100))
    page = Column(Integer)
    update_date = Column(DateTime, default=datetime.datetime.utcnow)


class Course(Base):
    __tablename__ = 'course'

    id = Column(Integer, primary_key=True)
    inst_id = Column(Integer, ForeignKey('institute.id'))
    course_name = Column(String(200))
    course_sector = Column(String(200))
    cricos_course_code = Column(String(50), nullable=False)
    vet_nat_code = Column(String(200))
    dual_qual = Column(String(200))
    broad_field = Column(String(200))
    narrow_field = Column(String(200))
    detailed_field = Column(String(200))
    course_level = Column(String(200))
    foundation_studies = Column(String(200))
    work_component = Column(String(200))
    course_language = Column(String(200))
    duration = Column(String(200))
    tution_fee = Column(String(100))
    non_tution_fee = Column(String(100))
    total_cost = Column(String(100))
    inst_id = Column(Integer, ForeignKey('institute.id'))
    page = Column(Integer)
    state = Column(String(30))
    update_date = Column(DateTime, default=datetime.datetime.utcnow)
    course_location = relationship("CourseLocation", cascade="all,delete-orphan", backref="course")


class CourseLocation(Base):
    __tablename__ = 'course_location'

    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('course.id'))
    location = Column(String(1000))
    page = Column(Integer)
    update_date = Column(DateTime, default=datetime.datetime.utcnow)


engine = create_engine('mysql+pymysql://kevin:Sydn3y30@localhost:3306/cricos')
# Create all tables in the engine. This is equivalent to Create Table in SQL
Base.metadata.create_all(engine)

'''
NOTES for mysql
1.
show create table contact_int_student;

2.
Alter table contact_principal drop foreign key contact_principal_ibfk_1;
Alter table contact_int_student drop foreign key contact_int_student_ibfk_1;

Alter table course_location drop foreign key course_location_ibfk_1;
Alter table course drop foreign key course_ibfk_1;

3.
Alter table contact_int_student add foreign key (`inst_id`) REFERENCES `institute` (`id`) on DELETE CASCADE;
Alter table contact_principal add foreign key (`inst_id`) REFERENCES `institute` (`id`) on DELETE CASCADE;

Alter table course_location add foreign key (`course_id`) REFERENCES `course` (`id`) on DELETE CASCADE;
Alter table course add foreign key (`inst_id`) REFERENCES `institute` (`id`) on DELETE CASCADE;

Alter table institute drop foreign key institute_ibfk_1;
Alter table institute add foreign key (`course_id`) REFERENCES `course` (`id`) on DELETE CASCADE;

4.
drop table course_location;
drop table course;
'''
