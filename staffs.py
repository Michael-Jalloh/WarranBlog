from flask import Blueprint, request, redirect, render_template, url_for, flash
from flask.views import MethodView
from flask_login import login_required
from wtfpeewee.orm import model_form
from models import Staff
from playhouse.flask_utils import get_object_or_404

staff = Blueprint('staff', __name__, template_folder='templates')

class SimList(MethodView):
	def get(self, page=1):
		max_page = Staff.max_staff_page_all()
		if Staff.select().count() != 0:
			staffs = Staff.select().paginate(page,10)
			return render_template('staffs/simlist.html', staffs=staffs,max_page=max_page, page=page)
		else:
			content = 'No staffs hav been added yet'
			return render_template('info.html', content=content,title='staff')

class Info(MethodView):
	def get(self, id):
		if Staff.select().count() != 0:
			query = Staff.select()
			staff = get_object_or_404(query, Staff.id == int(id))
			return render_template('staffs/staff.html', staff=staff,title=staff.name)
		else:
			content = 'There are current no staff'
			return render_template('infor.html', content=content)

class List(MethodView):
	decorators = [login_required]

	def get(self, page=1):
		max_page = Staff.max_staff_page_all()
		staffs = Staff.select().paginate(page,10)
		return render_template('staffs/list.html', staffs = staffs,max_page=max_page, page=page, title='Staff List')


class Detail(MethodView):
	decorators = [login_required]

	def get_context(self, id=None):
		form_cls = model_form(Staff)
		
		if id:
			query = Staff.select()
			staff = get_object_or_404(query, Staff.id == id)
			if request.method == 'POST':
				form = form_cls(request.form, intial=staff.bio)
			else:
				form = form_cls(obj=staff)
		else:
			staff = Staff()
			form = form_cls(request.form)

		context = {
			'staff':staff,
			'form':form,
			'create': id is None
			}
		return context

	def get(self,id):
		context = self.get_context(id)
		return render_template('staffs/detail.html', **context)

	def post(self, id):
		context = self.get_context(id)
		form = context.get('form')

		if form.validate():
			staff = context.get('staff')
			form.populate_obj(staff)
			staff.save()
			flash('Detail Have been saved')
			return redirect(url_for('staff.index'))
		return render_template('staffs/detail.html', **context)

class Delete(MethodView):
	decorators = [login_required]
	def get(self, id):
		query = Post.select()
		staff = get_object_or_404(query, Staff.id == int(id))
		staff.delete_instance()
		return redirect('/staffs/')

# Register the urls
staff.add_url_rule('/staffs/', view_func=List.as_view('index'))
staff.add_url_rule('/staff/create/', defaults={'id':None}, view_func=Detail.as_view('create'))
staff.add_url_rule('/staff/<id>/', view_func=Detail.as_view('edit'))
staff.add_url_rule('/staff/delete/<id>/', view_func=Delete.as_view('delete'))
staff.add_url_rule('/staff/info/<id>/', view_func=Info.as_view('info'))
staff.add_url_rule('/staffs/list/', view_func=SimList.as_view('list'))
