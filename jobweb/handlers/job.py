from flask import Blueprint, render_template, request, current_app, flash, redirect, url_for
from jobweb.models import Job_detail, Company, Delivery
from flask_login import login_required, current_user
from jobweb.forms import jobForm


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

@job.route('/<int:job_id>/edit', methods=['GET', 'POST'])
def edit(job_id):
    job = Job_detail.query.get_or_404(job_id)
    company = current_user.companydetail
    form = jobForm(obj=job)
    if form.validate_on_submit():
    	form.update_job(job)
    	flash('Update sucessful', 'success')
    	return redirect(url_for('company.jobs'))
    return render_template('company/edit_job.html', form=form, job=job, company=company)

@job.route('/<int:job_id>/offline')
def offline(job_id):
	job = Job_detail.query.get_or_404(job_id)
	job.isValid = False
	job.save()
	flash('update Sucessful', 'success')
	return redirect(url_for('company.jobs'))

@job.route('/<int:job_id>/online')
def online(job_id):
	job = Job_detail.query.get_or_404(job_id)
	job.isValid = True
	job.save()
	flash('update Sucessful', 'success')
	return redirect(url_for('company.jobs'))


@job.route('/<int:job_id>/apply', methods=['GET'])
@login_required
def apply(job_id):
	job = Job_detail.query.get_or_404(job_id)
	delivery = Delivery()
	delivery.job_id = job_id
	delivery.company_id = job.company_id
	delivery.user_id = current_user.id
	delivery.resume_up = current_user.seekerDetail.resume_up
	delivery.save()
	current_user.applied_jobs.append(job)
	job.applied_user.append(current_user)
	current_user.save()
	job.save()
	flash('Apply successful', 'success')
	return redirect(url_for('job.detail', job_id = job_id))