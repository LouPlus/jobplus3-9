from flask import Blueprint, render_template, request, flash,current_app, abort, redirect, url_for
from jobweb.models import Job_detail, Company,User, applications, Delivery
from flask_login import login_required, current_user
from jobweb.forms import companyForm, baseUserForm, jobForm


company = Blueprint('company', __name__, url_prefix='/companies')

@company.route('/<int:company_id>')
def detail(company_id):
    company = Company.query.get_or_404(company_id)
    jobs = Job_detail.query.filter_by(company_id = company.id, isValid=True)
    return render_template('company/detail.html', jobs=jobs, company=company)

@company.route('/<int:company_id>/jobs')
def current_jobs(company_id):
    page = request.args.get('page', default=1, type=int)
    company = Company.query.get_or_404(company_id)
    jobs = Job_detail.query.filter_by(company_id = company.id, isValid=True)
    pagination = jobs.paginate(page=page, per_page=current_app.config['INDEX_PER_PAGE'],error_out=False)
    return render_template('company/current_jobs.html', pagination=pagination)



@company.route('/profile/<int:company_id>', methods = ['GET', 'POST'])
@login_required
def profile(company_id):
    company = Company.query.get_or_404(company_id)
    user = company.user
    if not current_user.is_company:
        flash("You are not company user", "warning")
        return redirect(url_for('front.index'))
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
    company = Company.query.filter_by(isValid=True)
    pagination = company.paginate(page = page, per_page = current_app.config['INDEX_PER_PAGE'], error_out = False)
    return render_template('company/all.html', pagination = pagination)

@company.route('/jobs', methods = ['GET','POST'])
@login_required
def jobs():
    if current_user.role == 20:
        company = current_user.companydetail
        page = request.args.get('page',default=1, type=int)
        pagination = Job_detail.query.filter_by(company_id = company.id).paginate(page=page, per_page=current_app.config['INDEX_PER_PAGE'], error_out=False)
        return render_template('company/jobs.html', pagination = pagination, company = company)
    else: 
        abort(404)

@company.route('/application', methods=['GET','POST'])
@login_required
def application():
    if current_user.role == 20:
        company = current_user.companydetail
        page = request.args.get('page',default=1, type=int)
        pagination = Delivery.query.filter_by(company_id=current_user.companydetail.id).paginate(page=page, per_page=current_app.config['INDEX_PER_PAGE'], error_out=False)
        return render_template('company/applications.html', pagination = pagination, company = company)

@company.route('/<int:delivery_id>/pass', methods=['GET','POST'])
@login_required
def accept(delivery_id):
    delivery = Delivery.query.get_or_404(delivery_id)
    if not current_user.companydetail.id == delivery.company_id:
        abort(404)
    delivery.status = 3
    delivery.save()
    flash('Sucessful', 'success')
    return redirect(url_for('company.application'))

@company.route('/<int:delivery_id>/reject', methods=['GET','POST'])
@login_required
def reject(delivery_id):
    delivery = Delivery.query.get_or_404(delivery_id)
    if not current_user.companydetail.id == delivery.company_id:
        abort(404)
    delivery.status = 2
    delivery.save()
    flash('Sucessful', 'success')
    return redirect(url_for('company.application'))

@company.route('/addJob', methods=['GET', 'POST'])
@login_required
def add():
    if current_user.is_company:
        form = jobForm()
        if form.validate_on_submit():
            form.add_job()
            flash('Add sucessful', 'success')
            return redirect(url_for('company.jobs'))
        return render_template('company/add_job.html', form=form, company = current_user.companydetail)



       



