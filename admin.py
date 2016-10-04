from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView
from flask_login import login_required
from wtfpeewee.orm import model_form
from playhouse.flask_utils import get_object_or_404
from models import Post
from atom import login_manager

admin = Blueprint('admin', __name__, template_folder='templates')


class List(MethodView):
	decorators = [login_required]

	def get(self):
		posts = Post.select()
		return render_template('admin/list.html', posts=posts, title='Post listing')


class Detail(MethodView):
	decorators = [login_required]

	def get_context(self, slug=None):
		form_cls = model_form(Post, exclude=('timestamp','slug'))

		if slug:
			query = Post.select()
			post = get_object_or_404(query, Post.slug ==slug)
			if request.method == 'POST':
				form = form_cls(request.form, intial=post.content)
			else:
				form = form_cls(obj=post)
		else:
			post = Post()
			form = form_cls(request.form)

		context = {
			'post': post,
			'form': form,
			'create': slug is None
		}
	
		return context

	def get(self, slug):
		context = self.get_context(slug)
		return render_template('admin/detail.html', title='Details', **context)

	def post(self, slug):
		context = self.get_context(slug)
		form = context.get('form')

		if form.validate():
			post = context.get('post')
			form.populate_obj(post)
			post.save()

			return redirect(url_for('admin.index'))
		return render_template('admin/detail.html', **context)


class Delete(MethodView):
	def get(self,slug):
		query = Post.select()
		post = get_object_or_404(query,Post.slug==slug)
		post.delete_instance()
		return redirect('/admin/')
		


# Register the urls
admin.add_url_rule('/admin/', view_func=List.as_view('index'))
admin.add_url_rule('/admin/create/', defaults={'slug': None}, view_func=Detail.as_view('create'))
admin.add_url_rule('/admin/<slug>/', view_func=Detail.as_view('edit'))
admin.add_url_rule('/admin/delete/<slug>/', view_func=Delete.as_view('delete'))
