from flask import Blueprint, render_template, request, current_app
from jobweb.models import Job_detail, Company
from flask_login import login_required


job = Blueprint('job', __name__, url_prefix='/jobs')

@job.route('/<int:job_id>')
def detail(job_id):
	job = Job_detail.query.get_or_404(job_id)
	company = job.company
	return render_template('job/detail.html', job=job, company=company)

@job.route('/all')
def all():
	page = request.args.get('page', default=1, type=int)
	pagination = Job_detail.query.paginate(page = page, per_page = current_app.config['INDEX_PER_PAGE'], error_out = False)
	return render_template('job/all.html', pagination = pagination)