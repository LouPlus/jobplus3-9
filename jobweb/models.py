from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()

class Base(db.Model):
    __abstract__ = True

    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    upodate_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class User(Base):
    __tablename__ = 'user'

    JOBSEEKER = 10
    COMPANY = 20
    ADMIN = 30

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    cellphone = db.Column(db.String(32))
    email = db.Column(db.String(64), unique=True, nullable=False)
    _password = db.Column('password', db.String(256), nullable=False)
    role = db.Column(db.SmallInteger, default = JOBSEEKER)
    seekerDetail = db.relationship('Jobseeker', uselist=False)
    companydetail = db.relationship('Company', uselist=False)

    def __repr__(self):
        return '<User:{}>'.format(self.name)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, pw):
        self._password = gennerate_password_hash(pw)

    def check_password(self, password):
        return check_password_hash(self._password, password)

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_company(self):
        return self.role == self.COMPANY
    

class Company(Base):
    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True)
    companyname = db.Column(db.String(64), unique=True, index=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    website = db.Column(db.String(64))
    # 公司人数
    num = db.Column(db.String(32))
    logo = db.Column(db.String(64))
    address = db.Column(db.String(64))
    # 公司介绍
    desc = db.Column(db.String(256))
    release_job = db.relationship('Job_detail')

    def __repr__(self):
        return '<Company {}>'.format(self.id)

class Job_detail(Base):
    __tablename__ = 'job_detail'

    id = db.Column(db.Integer, primary_key=True)
    jobname = db.Column(db.String(64))
    salary = db.Column(db.String(32), nullable=False)
    workaddress = db.Column(db.String(64))
    education = db.Column(db.String(32))
    company = db.relationship('Company', uselist=False)
    release_time = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '<Job_detail {}>'.format(self.jobname)

class  Jobseeker(Base):
    __tablename__ = 'jobseeker'

    id = db.Column(db.Integer, primary_key=True)
    seekername = db.Column(db.String(32), nullable=False)
    sex = db.Column(db.String(16))
    age = db.Column(db.Integer)
    address =db.Column(db.String(64))
    # 上传的简历
    resume_up = db.Column(db.String(32))
    experience = db.relationship('Experience', uselist=False)

class Experience(Base):
    __tablename__ = 'experience'

    id = db.Column(db.Integer, primary_key=True)
    ep_id = db.Column(db.Integer, db.ForeignKey('jobseeker.id'))
    desc_edu = db.Column(db.String(256))
    desc_job = db.Column(db.String(256))


