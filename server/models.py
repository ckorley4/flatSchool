from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)


class Student(db.Model, SerializerMixin):
    __tablename__ ='students'

    id = db.Column(db.Integer,primary_key=True)
    fname = db.Column(db.String,nullable=False)
    lname = db.Column(db.String,nullable=False)
    email = db.Column(db.String,unique=True,nullable=False)
    enrollment = db.Column(db.Integer,db.ForeignKey('enrollments.id'),nullable=False)
     
    #relationship
    enrollment = db.relationship('Enrollment',back_populates='sutdent', cascade='all,delete')

    #serialize rules
    serialize_rules = ('-enrollments.student')

    def __repr__(self):
        return "<Student {self.id} => {self.fname} - {self.lname}>"
    
class Enrollment(db.Model,SerializerMixin):
    __tablename__='enrollments'

    id = db.Column(db.Integer,primary_key=True)
    student_id = db.Column(db.Integer,db.ForeignKey("students.id"),nullable=False)
    course_id =  db.Column(db.Integer,db.ForeignKey("courses.id"),nullable= False)
    
    #relationships
    student = db.relationship("Student",back_populates='enrollment')
    course = db.relationship("Course",back_populates='enrollment')


    #serialize rules
    serialize_rules =('-stundents.enrollment',)

    def __repr__(self):
        return "<Enrollment {self.id}>"


class Course(db.Model,SerializerMixin):
    __tablename__='courses'

    id = db.Column(db.Integer,primary_key=True)
    description =  db.Column(db.String(50),nullable=False)
    venue_id = db.Column(db.Integer,db.ForeignKey("venues.id"),nullable=False)
    time = db.Column(db.Integer)
    instructor_id = db.Column(db.Integer,db.ForeignKey("instructors.id"),nullable=False)

    #relationship
    enrollment = db.relationship("Enrollment",back_populates='course',cascade='all,delete')
    instructor = db.relationship('Instructor',back_populates='course')
    venue = db.relationship('Venue',back_populates='course')

    #serialize rules
    serialize_rules =('-enrollments.course_id')
    serialize_rules = ('-instructors.id')
    serialize_rules = ('-venues.id')

    def __repr__(self):
        return "<Course {self.description}>"

class Instructor(db.Model,SerializerMixin):
    __tablename__='instructors'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    department =db.Column(db.String(50))
    specialty = db.Column(db.String(50))

    course =db.relationship('Course',back_populates='courses.instructor',cascade='all,delete')
    
    serialize_rules =('-courses.instructor_id',)

    def __repr__(self):
        return "<Instructor {self.name}>"

class Venue(db.Model,SerializerMixin):
    __tablename__='venues'

    id = db.Column(db.Integer,primary_key=True)
    location = db.Column(db.String)

    db.relationship('Course',back_populates='courses.venue',cascade='all,delete')

    serialize_rules =('-courses.venue_id',)


