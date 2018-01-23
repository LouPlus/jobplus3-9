from flask import Blueprint, render_template, request, flash,current_app
from jobweb.models import Job_detail, Company,User
from flask_login import login_required
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

