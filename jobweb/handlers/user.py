from flask import Blueprint, render_template,flash, request, abort, current_app
from flask_login import login_required, current_user

from jobweb.forms import baseUserForm
from jobweb.models import Job_detail, Jobseeker,User, Delivery

user = Blueprint('user', __name__, url_prefix='/user')


@user.route('/<int:user_id>/profile', methods = ['GET','POST'])
@login_required
def profile(user_id):
    user = User.query.get_or_404(user_id)
    if current_user != user:
        abort(404)
    jobseeker = user.seekerDetail

    if request.method == 'GET':
        form = baseUserForm(obj=user)
        # form.email.data = user.email
        # form.password.data = user._password
        # form.cellphone.data = user.cellphone
        form.seekername.data = jobseeker.seekername
        form.desc_edu.data = jobseeker.desc_edu
        form.desc_experience.data = jobseeker.desc_experience
        form.resume_up.data = jobseeker.resume_up
    else:
        form = baseUserForm()

    if form.validate_on_submit():
         form.saveUser(user)
         flash("Success!", 'success')
    return render_template('user/detail.html', user=user, form = form)

@user.route('/<int:user_id>/resume', methods=['GET','POST'])
@login_required
def resume(user_id):
    user = User.query.get_or_404(user_id)
    jobseeker = user.seekerDetail
    return render_template('/user/resume.html', jobseeker=jobseeker, user = user)

@user.route('/<int:user_id>/application', methods=['GET'])
@login_required
def application(user_id):
    user = User.query.get_or_404(user_id)
    page = request.args.get('page',default=1, type=int)
    pagination = Delivery.query.filter_by(user_id=current_user.id).paginate(page=page, per_page=current_app.config['INDEX_PER_PAGE'], error_out=False)
    return render_template('user/applications.html', pagination = pagination, user = user)



