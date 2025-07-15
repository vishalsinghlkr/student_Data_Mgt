from flask import Blueprint, render_template, request, redirect, url_for
from .models import db, PersonalInfo

views = Blueprint('views', __name__) #it is used to create a blueprint for the views module


# List all students
@views.route('/')
def home():
    """
    Welcome to the Student Management System
    ---
    responses:
      200:
        description: Returns a welcome message
    """
    return "Welcome to the Student Management System"


@views.route('/add', methods=['POST'])
def add_student():
    """
    Fill your details:-
    ---
    tags:
      - Adding Students Personal Detail
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - name
            - email
            - gender
            - phone_number
          properties:
            name:
              type: string
              example: John Doe
            email:
              type: string
              example: john@example.com
            gender:
              type: string
              example: Male
            phone_number:
              type: string
              example: 1234567890
    responses:
      200:
        description: Student added successfully
      400:
        description: Missing fields or invalid input
    """
    data = request.get_json()

    # Extract fields safely
    name = data.get('name')
    email = data.get('email')
    gender = data.get('gender')
    phone_number = data.get('phone_number')

    if not all([name, email, gender, phone_number]):
        return {"error": "Missing required fields"}, 400

    new_student = PersonalInfo(name=name, email=email, gender=gender, phone_number=phone_number)
    db.session.add(new_student)
    db.session.commit()
    
    return {"message": f"Student '{name}' added successfully"}, 200


