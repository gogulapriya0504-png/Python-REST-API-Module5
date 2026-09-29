# Module 5: Python Application Development - REST API
# Author: Gokulapriya M

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import os

app = Flask(__name__)

# SQLite Database Setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    course = db.Column(db.String(50), nullable=False)
    
    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'email': self.email, 'course': self.course}

# Create Tables
with app.app_context():
    db.create_all()

# API Authentication (Basic)
API_KEY = "gokula_api_key_2026"

def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        key = request.headers.get('X-API-KEY')
        if key != API_KEY:
            return jsonify({'error': 'Invalid or Missing API Key'}), 401
        return f(*args, **kwargs)
    return decorated

# --- API ENDPOINTS ---

@app.route('/')
def home():
    return jsonify({
        'message': 'Python REST API - Module 5',
        'endpoints': {
            'GET /api/students': 'Get all students',
            'GET /api/students/<id>': 'Get student by ID',
            'POST /api/students': 'Create new student',
            'PUT /api/students/<id>': 'Update student',
            'DELETE /api/students/<id>': 'Delete student'
        },
        'auth': 'Add header X-API-KEY: gokula_api_key_2026'
    })

# GET ALL - CRUD Read
@app.route('/api/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    return jsonify([s.to_dict() for s in students])

# GET ONE
@app.route('/api/students/<int:id>', methods=['GET'])
def get_student(id):
    student = Student.query.get(id)
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    return jsonify(student.to_dict())

# POST - CRUD Create (with Validation & Auth)
@app.route('/api/students', methods=['POST'])
@require_api_key
def create_student():
    data = request.get_json()
    
    # Schema Validation
    if not data or not all(k in data for k in ('name','email','course')):
        return jsonify({'error': 'Missing fields: name, email, course required'}), 400
    
    if '@' not in data['email']:
        return jsonify({'error': 'Invalid email format'}), 400
    
    try:
        new_student = Student(name=data['name'], email=data['email'], course=data['course'])
        db.session.add(new_student)
        db.session.commit()
        return jsonify(new_student.to_dict()), 201
    except:
        return jsonify({'error': 'Email already exists'}), 409

# PUT - CRUD Update
@app.route('/api/students/<int:id>', methods=['PUT'])
@require_api_key
def update_student(id):
    student = Student.query.get(id)
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    
    data = request.get_json()
    student.name = data.get('name', student.name)
    student.email = data.get('email', student.email)
    student.course = data.get('course', student.course)
    db.session.commit()
    return jsonify(student.to_dict())

# DELETE - CRUD Delete
@app.route('/api/students/<int:id>', methods=['DELETE'])
@require_api_key
def delete_student(id):
    student = Student.query.get(id)
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    db.session.delete(student)
    db.session.commit()
    return jsonify({'message': 'Student deleted successfully'})

if __name__ == '__main__':
    print("API Running at http://127.0.0.1:5000")
    print("API Key: gokula_api_key_2026")
    app.run(debug=True)
