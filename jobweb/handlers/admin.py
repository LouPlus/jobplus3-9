from flask import Blueprint, render_template, request, current_app,redirect
from flask import url_for, flash
from jobweb.decorators import admin_required
from jobweb.models import db,User
from jobweb.forms import UserRegisterForm, CompanyRegisterForm,UserEditForm, CompanyEditForm

admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/')
@admin_required
def admin_index():
  return render_template('admin/index.html')


@admin.route('/users')
@admin_required
def users():
  page = request.args.get('page', default=1, type=int)
  pagination = User.query.paginate(
    page=page,
    per_page=current_app.config['ADMIN_PER_PAGE'],
    error_out = False
  )
  return render_template('admin/users.html', pagination=pagination)

@admin.route('/users/create_user', methods=['GET', 'POST'])
@admin_required
def create_user():
  form = UserRegisterForm()
  if form.is_submitted():
    form.create_user()
    flash('create user success', 'success') #添加求职者成功
    return redirect(url_for('admin.users'))
  return render_template('admin/create_user.html', form=form)


@admin.route('/users/create_company', methods=["GET","POST"])
@admin_required
def create_company():
  form = CompanyRegisterForm()
  if form.is_submitted():
    form.create_companyProfile()
    flash('create company success','success') #添加企业成功
    return redirect(url_for('admin.users'))
  return render_template('admin/create_company.html', form=form)

@admin.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.is_company:
        form = CompanyEditForm(obj=user)
    else:
        form = UserEditForm(obj=user)
    if form.validate_on_submit():
        form.update(user)
        flash('edit success', 'success')
        return redirect(url_for('admin.users'))
    if user.is_company:
        form.website.data = user.companydetail.website
        form.desc.data = user.companydetail.desc
    return render_template('admin/edit_user.html', form=form, user=user)


@admin.route('/users/<int:user_id>/disable', methods=['GET','POST'])
@admin_required
def disable_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.is_disable:
        user.is_disable = False
        flash('enable user', 'success')
    else:
        user.is_disable = True
        flash('disable user', 'success')
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('admin.users'))
