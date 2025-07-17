from flask import Blueprint, render_template, request, redirect, url_for,jsonify,flash
from .models import db, PersonalInfo,ClassInfo,Sports
from .auth import login_required
from flask_login import current_user


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


@views.route('/add', methods=['GET','POST'])
# @login_required
def add_presonalinfo():
    if request.method=='POST':
        name = request.form.get('name')
        email = request.form.get('email')
        gender = request.form.get('gender')
        phone_number = request.form.get('phone_number')
        personalinfo=PersonalInfo.query.filter_by(email=email).first()


        if personalinfo:
            flash("Email already exists.", category='error')
        elif len(email) < 4:
            flash("Email must be greater than 4 characters.", category='error')
        elif len(name) < 2:  # Fixed typo
            flash("First name must be greater than 2 characters.", category='error')
        elif len(gender) < 7:
            flash("Password must be at least 7 characters long.", category='error')
        elif len(phone_number)<10 and len(phone_number)>10:
            flash('Please Enter valid Phone Number :',category='error')
        else:
            new_student = PersonalInfo(name=name, email=email, gender=gender, phone_number=phone_number)
            db.session.add(new_student)
            db.session.commit()
            flash("Account Created!",category='success')
    return render_template('Return to the student dashboard',personalinfo=current_user)
    

    
        
    
        
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

    # data = request.get_json()

    # Extract fields safely
    

    

    
    
    



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
    # data = request.get_json()
    registration_no = request.form.get('registration_no')
    name=request.form.get('name')

    student = PersonalInfo.query.get(registration_no,name)
    if student:
        db.session.delete(student)
        db.session.commit()
        flash('Student Deleted Successfully',category='success')
    else:
        flash('User not found',category='error'),404

    
#Search Student From the Database By Id:
   
@views.route('/search-student', methods=['POST'])
def search_student():
    registration_no = request.form.get('registration_no')
    name = request.form.get('name')

    # Start query
    query = PersonalInfo.query
    if registration_no:
        query = query.filter_by(registration_no=registration_no)
    if name:
        query = query.filter(PersonalInfo.name.ilike(f"%{name}%"))

    student = query.first()

    if student:
        return render_template('student_result.html', student=student)
    else:
        return render_template('student_result.html', message="Student not found")
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
    # 1. Personal Info
    student = PersonalInfo(
        name=request.form.get('name'),
        gender=request.form.get('gender'),
        email=request.form.get('email'),
        phone_number=request.form.get('phone_number')
    )
    db.session.add(student)
    db.session.flush()  # Needed to get registration_no

    # 2. Class Info
    class_info = ClassInfo(
        roll_no=request.form.get('roll_no'),
        registration_no=student.registration_no,
        class_name=request.form.get('class_name'),
        section=request.form.get('section'),
        academic_year=request.form.get('academic_year'),
        batch=request.form.get('batch')
    )
    db.session.add(class_info)

    # 3. Sports Info (can be multiple)
    sport_names = request.form.getlist('sport_name')
    team_names = request.form.getlist('team_name')
    coach_names = request.form.getlist('coach_name')
    rankings = request.form.getlist('ranking')

    for i in range(len(sport_names)):
        sport_obj = Sports(
            registration_no=student.registration_no,
            sport_name=sport_names[i],
            team_name=team_names[i] if i < len(team_names) else None,
            coach_name=coach_names[i] if i < len(coach_names) else None,
            ranking=int(rankings[i]) if i < len(rankings) and rankings[i].isdigit() else None
        )
        db.session.add(sport_obj)

    db.session.commit()
    flash('Student Added Successfully')
    return render_template("student_success.html", student=student)



@views.route('/students', methods=['GET'])
def get_all_students():
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
            c = s.classes[0]
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
    source = request.args.get('source', 'teacher')

    return render_template("students.html", students=result,source=source)



# ── Teacher home page ──────────────────────────────────────────────
@views.route('/teacher-home')
# @login_required  # ←‑‑ uncomment if you protect teacher pages
def teacher_home():
    """
    Teacher dashboard with quick links.
    """
    return render_template("teacher_home.html")

