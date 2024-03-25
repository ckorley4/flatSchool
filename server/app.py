from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import ipdb
import os
from  models import db,Student

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

class Students(Resource):
    def get(self):
        students = Student.query.all()
        students_list = [student.to_dict() for student in students]
        return make_response(students_list,200)
    def post(self):
       # ipdb.set_trace()
        incoming = request.json
        new_student = Student(**incoming)
        db.session.add(new_student)
        db.session.commit()
        return make_response(new_student.to_dict(),201)

class StudentbyId(Resource):
    def get(self,id):
        student = Student.query.get(id)
        return make_response(student.to_dict(),200)
    def patch(self,id):
        pass
    def delete(self,id):
        student = Student.query.get(id)
        db.session.delete(student)
        db.session.commit()

    
api.add_resource(Students,'/students')
api.add_resource(StudentbyId,'/students/<int:id>')

if __name__ == "__main__":
    app.run(port=5555, debug=True)