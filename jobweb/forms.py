from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,SelectField
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import Length, Email, EqualTo, Required
from jobweb.models import db, User, Company,Jobseeker
from wtforms import ValidationError
import os
from flask import url_for

db = SQLAlchemy()

"""class User(db.Model):
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
     positions = db.relationship('Position');"""

PEOPLE_CHOICES = [('1','1-50'),('2','51-100'),('3','101-500'),('4','>500')]
class Base(FlaskForm):
    __abstract__ = True
    username = StringField('Username', validators=[Required(), Length(3, 24)])
    email = StringField('Email', validators=[Required(), Email()])
    password = PasswordField('Password', validators=[Required(), Length(6, 24)])
    repeat_password = PasswordField('Password again', validators=[Required(), EqualTo('password')])


# cannot extends from Base
# Because we don't need repeated_password here
class UserEditForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Email()])
    password = PasswordField('password')
    username = StringField('name')
    phone = StringField('phone number')
    submit = SubmitField('submit')

    def update(self, user):
        self.populate_obj(user)
        if self.password.data:
            user.password = self.password.data
        db.session.add(user)
        db.session.commit()


class CompanyEditForm(FlaskForm):
    username = StringField('company name')
    email = StringField('email', validators=[Required(), Email()])
    password = PasswordField('password')
    cellphone = StringField('phone number')
    website = StringField('company site', validators=[Length(0, 64)])
    desc = StringField('description', validators=[Length(0, 100)])
    submit = SubmitField('submit')

    def update(self, company):
        company.username = self.username.data
        company.email = self.email.data
        if self.password.data:
            company.password = self.password.data
        if company.detail:
            detail = company.detail
        else:
            detail = CompanyDetail()
            detail.user_id = company.id
        detail.website = self.website.data
        deatil.desc = self.desc.data
        db.session.add(company)
        db.session.add(detail)
        db.session.commit()
            



class CompanyRegisterForm(Base):

    companyName = StringField('Company Name', validators=[Required(), Length(1,100)])
    location = StringField('Location', validators=[Required()])
    number_of_people = SelectField('Number of People', choices = PEOPLE_CHOICES)
    submit = SubmitField('Submit')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("User already exists")
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')
    def validate_companyName(self, field):
        if Company.query.filter_by(companyname = field.data).first():
            raise ValidationError('Company Name already registered')

    def create_companyProfile(self):
        user = User()
        company = Company()
        company.address = self.location.data
        company.num = dict(PEOPLE_CHOICES).get(self.number_of_people.data)
        company.companyname = self.companyName.data
        company.user = user
        user.companydetail = company
        user.username = self.username.data
        user.email = self.email.data
        user.password = self.password.data
        user.role = 20
        user.save()
        company.save()
        

class UserRegisterForm(Base):
    seekername = StringField('Real Name', validators=[Required()])
    submit = SubmitField('Submit')

    def create_user(self):
        user = User()
        jobseeker = Jobseeker()
        user.seekerDetail = jobseeker
        user.username = self.username.data
        user.email = self.email.data
        user.password = self.password.data
        jobseeker.seekername = self.seekername.data
        user.save()
        jobseeker.save()

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("User already exists")
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Email()])
    password = PasswordField('Password', validators=[Required(), Length(6, 24)])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Submit')

    def validae_email(self, field):
        if field.data and not User.query.filter_by(email=field.data).first():
            raise ValidationError('email not register')
    def validate_password(self, field):
        user = User.query.filter_by(email=self.email.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError('Password incorrect')

    
    
class baseUserForm(FlaskForm): 
    email = StringField('Email', validators=[Required(), Email()])
    password = PasswordField('Password', validators=[Required(), Length(6, 24)])
    cellphone = StringField('Phone Number', validators=[Length(10,15)])
    desc_edu = StringField('Education')
    desc_experience = StringField('Experience')
    seekername = StringField('RealName')
    resume_up = FileField('Resume', validators=[FileRequired()])
    
    submit = SubmitField('submit')

    def upload_resume(self):
        f = self.resume_up.data
        filename = self.seekername.data + '.pdf'
        f.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),'static','resumes',filename))
        return filename
    
    def saveUser(self, user):
          user.email = self.email.data
          user.password = self.password.data
          user.cellphone = self.cellphone.data
         #self.populate_obj(user)
          user.save()
          user.seekerDetail.seekername = self.seekername.data
          user.seekerDetail.desc_experience = self.desc_experience.data
          user.seekerDetail.desc_edu = self.desc_edu.data
          filename = self.upload_resume()
          user.seekerDetail.resume_up = url_for('static',filename=os.path.join('resumes',filename))
         #self.populate_obj(user.seekerDetail)
          user.seekerDetail.save()
          
class companyForm(FlaskForm):
    companyname = StringField('companyName')
    address = StringField('Address')
    website = StringField('Website')
    logo = StringField('Logo')
    desc = StringField('Description')
    email = StringField('Email', validators=[Required(), Email()])
    password = PasswordField('Password', validators=[Required(), Length(6,24)])
    submit = SubmitField('Submit')

    def saveCompany(self, company):
        self.populate_obj(company)
        company.save()
        self.populate_obj(company.user)
        company.user.save()

class jobForm(FlaskForm):
    jobname = StringField('Job Name')
    salary = StringField('Salary')
    workaddress = StringField('Address')
    education = StringField('Education')
    experience = StringField('Experience')
    desc = StringField('Description')
    submit = SubmitField('Submit')

    def update_job(self, job):
        self.populate_obj(job)
        job.save()
        return job

