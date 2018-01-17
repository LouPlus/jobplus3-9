from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    
    
    
class Position(db.Model):
    __tablename__ = 'position'
    
    position_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    salary_range = db.Column(db.Integer)
    experience_req = db.Column(db.Integer)
    work_place = db.Column(db.String(32))
    info = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    company = db.relationship('Company', uselist=False)
    
 class Company(db.Model):
     __tablename__ = 'company'
     
     company_id = db.Column(db.Integer, primary_key=True)
     # logo图片url地址
     logo = db.Column(db.String(256))
     name = db.Column(db.String(128), unique=True, nullable=False)
     work_place = db.Column(db.String(128))
     website = db.Column(db.String(32))
     brief = db.Column(db.Text)
     number_hire = db.Column(db.Integer)
     positions = db.relationship('Position');
