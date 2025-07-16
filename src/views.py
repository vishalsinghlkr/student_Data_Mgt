from flask import Blueprint, render_template, request, redirect, url_for,jsonify
from .models import db, PersonalInfo,ClassInfo,Sports


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
def add_presonalinfo():
    """
    Fill your details:-
    ---
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
    sports_id=data.get('sports_id')

    if not all([name, email, gender, phone_number]):
        return {"error": "Missing required fields"}, 400

    new_student = PersonalInfo(name=name, email=email, gender=gender, phone_number=phone_number)
    db.session.add(new_student)
    db.session.commit()
    
    return {"message": f"Student '{name}' added successfully"}, 200



#Delete Student From the Database:-
@views.route('/delete-student', methods=['DELETE'])
def delete_user():
    """
    Delete a user by ID :
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - registration_no
          properties:
            registration_no:
              type: integer
              example: 1
    responses:
      200:
        description: User deleted
        examples:
          application/json: {"message": "User deleted successfully"}
      404:
        description: User not found
        examples:
          application/json: {"message": "User not found"}
    """
    data = request.get_json()
    registration_no = data.get('registration_no')

    student = PersonalInfo.query.get(registration_no)
    if student:
        db.session.delete(student)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"}), 200
    else:
        return jsonify({"message": "User not found"}), 404

    
#Search Student From the Database By Id:
   
@views.route('/search-student',methods=['POST'])
def search():
    """
    Search A Student By Id
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - registration_no
          properties:
            registration_no:
              type: integer
              example: 1
    responses:
      200:
        description: Student Searched 
        examples:
          application/json: {"message": "Student Searched successfully"}
      404:
        description: Student not found
        examples:
          application/json: {"message": "Student not found"}
    """
    data = request.get_json()
    registration_no = data.get('registration_no')
    
    student = PersonalInfo.query.get(registration_no)
    

    if student:
        return jsonify({
            "id": student.registration_no,
            "name":student.name,
            "email": student.email,
            "gender":student.gender,
            "phone_number":student.phone_number
        }), 200
    else:
        return jsonify({"message": "User not found"}), 404
#retrive all the records

@views.route('/personal-info', methods=['GET'])
def get_all_personal_info():
    """
    Get all personal info records
    ---
    responses:
      200:
        description: List of personal info records
        schema:
          type: array
          items:
            type: object
            properties:
              registration_no:
                type: integer
              uuid:
                type: string
              name:
                type: string
              gender:
                type: string
              email:
                type: string
              phone_number:
                type: string
    """
    records = PersonalInfo.query.all()
    result = [{
        "registration_no": r.registration_no,
        "uuid": str(r.uuid),
        "name": r.name,
        "gender": r.gender,
        "email": r.email,
        "phone_number": r.phone_number
    } for r in records]
    return jsonify(result)

@views.route('/add-student', methods=['POST'])
def add_student():
    """
    Add a student with class info and sports
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [name, gender, email, phone_number, class_info]
          properties:
            name:
              type: string
            gender:
              type: string
            email:
              type: string
            phone_number:
              type: string
            class_info:
              type: object
              required: [roll_no, class_name]
              properties:
                roll_no:
                  type: string
                class_name:
                  type: string
                section:
                  type: string
                academic_year:
                  type: string
                batch:
                  type: string
            sports:
              type: array
              items:
                type: object
                required: [sport_name]
                properties:
                  sport_name:
                    type: string
                  team_name:
                    type: string
                  coach_name:
                    type: string
                  ranking:
                    type: integer
    responses:
      201:
        description: Student added successfully
    """
    data = request.get_json()

    # 1. Personal Info
    student = PersonalInfo(
        name=data['name'],
        gender=data['gender'],
        email=data['email'],
        phone_number=data['phone_number']
    )
    db.session.add(student)
    db.session.flush()  # Gets registration_no before committing

    # 2. Class Info (one-to-one)
    class_data = data.get('class_info')
    class_info = ClassInfo(
        roll_no=class_data['roll_no'],
        registration_no=student.registration_no,
        class_name=class_data['class_name'],
        section=class_data.get('section'),
        academic_year=class_data.get('academic_year'),
        batch=class_data.get('batch')
    )
    db.session.add(class_info)

    # 3. Sports Info (one-to-many)
    sports_data = data.get('sports', [])
    for sport in sports_data:
        sport_obj = Sports(
            registration_no=student.registration_no,
            sport_name=sport['sport_name'],
            team_name=sport.get('team_name'),
            coach_name=sport.get('coach_name'),
            ranking=sport.get('ranking')
        )
        db.session.add(sport_obj)

    db.session.commit()
    return jsonify({"message": "Student added successfully"}), 201

@views.route('/students', methods=['GET'])
def get_all_students():
    """
    Get all students with class and sports info
    ---
    responses:
      200:
        description: List of students with details
    """
    students = PersonalInfo.query.all()
    result = []

    for s in students:
        student_info = {
            "registration_no": s.registration_no,
            "uuid": str(s.uuid),
            "name": s.name,
            "gender": s.gender,
            "email": s.email,
            "phone_number": s.phone_number,
            "class_info": None,
            "sports": []
        }

        # ClassInfo (One-to-One)
        if s.classes:
            c = s.classes[0]  # One-to-one relationship
            student_info["class_info"] = {
                "roll_no": c.roll_no,
                "uuid": str(c.uuid),
                "class_name": c.class_name,
                "section": c.section,
                "academic_year": c.academic_year,
                "batch": c.batch
            }

        # Sports (One-to-Many)
        for sport in s.sports:
            student_info["sports"].append({
                "sport_id": sport.sport_id,
                "sport_name": sport.sport_name,
                "team_name": sport.team_name,
                "coach_name": sport.coach_name,
                "ranking": sport.ranking
            })

        result.append(student_info)

    return jsonify(result), 200


