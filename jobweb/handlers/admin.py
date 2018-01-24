from flask import Blueprint, render_template, request, current_app
from jobweb.decorators import admin_required
from jobweb.models import User
from jobweb.forms import UserRegisterForm

admin = Blueprint('admin', __name__, url_prefix='/admin')

# admin的首页
@admin.route('/')
@admin_required
def admin_index():
  return render_template('admin/index.html')

# 实现用户管理
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

@admin.route('/users/adduser', methods=['GET', 'POST'])
@admin_required
def create_user():
  user = UserForm()
  if form.validate_on_submit():
    form.create_user()
    flash('create user success', 'success') #添加求职者成功
    return redirect(url_for('admin.users'))
  return render_template('admin/user/adduser.html', form=form)
