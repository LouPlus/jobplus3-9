from flask import Blueprint, render_template, request, flash,current_app, abort
from jobweb.models import Job_detail, Company,User, applications
from flask_login import login_required, current_user
from jobweb.forms import companyForm, baseUserForm


company = Blueprint('company', __name__, url_prefix='/companies')

@company.route('/<int:company_id>')
def detail(company_id):
    company = Company.query.get_or_404(company_id)
    jobs = Job_detail.query.filter_by(company_id = company.id)
    return render_template('company/detail.html', jobs=jobs, company=company)

@company.route('/profile/<int:company_id>', methods = ['GET', 'POST'])
@login_required
def profile(company_id):
    company = Company.query.get_or_404(company_id)
    user = company.user
    if current_user != user:
        abort(404)
    if request.method == 'GET':
        form = companyForm(obj = company)
        form.email.data = user.email
        form.password.data = user.password
    else:
        form = companyForm()

    if form.validate_on_submit():
        form.saveCompany(company)
        flash("Success!", 'success')
    return render_template('company/profile.html', company = company, form = form)

@company.route('/all')
def all():
    page = request.args.get('page', default=1, type=int)
    pagination = Company.query.paginate(page = page, per_page = current_app.config['INDEX_PER_PAGE'], error_out = False)
    return render_template('company/all.html', pagination = pagination)

@company.route('/jobs', methods = ['GET','POST'])
@login_required
def jobs():
    if current_user.role == 20:
        company = current_user.companydetail
        page = request.args.get('page',default=1, type=int)
        pagination = Job_detail.query.filter_by(company_id = company.id).paginate(page=page, per_page=current_app.config['INDEX_PER_PAGE'], error_out=False)
        return render_template('company/jobs.html', pagination = pagination)
    else: 
        abort(404)

"""@company.route('/application', method=['GET','POST'])
def application():
    if current_user.role == 20:

        jobs = Job_detail.query.filter_by(company_id = current_user.companydetail.id).all()

        job_ids = tuple(job.id for job in jobs)
        applications = applications.query.filter(applications.job_id.in_(job_ids))
        page = request.args.get('page',default=1, type=int)
        pagination = applications.paginate(page)

        return render_template('company/allication.html', )"""



