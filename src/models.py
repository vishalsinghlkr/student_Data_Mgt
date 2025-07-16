import uuid
from . import db
from sqlalchemy.orm import relationship

from sqlalchemy.dialects.postgresql import UUID
import bcrypt



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'admin', 'teacher', 'student'

    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))



class PersonalInfo(db.Model):
    __tablename__ = 'personal_info'
    registration_no = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False, index=True) # Unique identifier for each student 

    name = db.Column(db.String(50))
    gender = db.Column(db.String(10))
    email = db.Column(db.String(100), unique=True)
    phone_number = db.Column(db.String(15))

    sports = relationship('Sports', backref='student', cascade='all, delete-orphan')
    classes = relationship('ClassInfo', backref='student', cascade='all, delete-orphan')


class Sports(db.Model):
    __tablename__ = 'sports'
    sport_id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False, index=True)

    registration_no = db.Column(db.Integer, db.ForeignKey('personal_info.registration_no', ondelete='CASCADE'), nullable=False)
    sport_name = db.Column(db.String(100), nullable=False)
    team_name = db.Column(db.String(100))
    coach_name = db.Column(db.String(100))
    ranking = db.Column(db.Integer)


class ClassInfo(db.Model):
    __tablename__ = 'class_info'
    roll_no = db.Column(db.String(20), primary_key=True)
    uuid = db.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False, index=True) 

    registration_no = db.Column(db.Integer, db.ForeignKey('personal_info.registration_no', ondelete='CASCADE'), nullable=False)
    class_name = db.Column(db.String(50), nullable=False)
    section = db.Column(db.String(10))
    academic_year = db.Column(db.String(20))
    batch = db.Column(db.String(50)) 