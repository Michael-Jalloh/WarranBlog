from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView
from playhouse.flask_utils import get_object_or_404
from models import Post
from wtfpeewee.orm import model_form
from flask_login import login_required


POST_PER_PAGE = 5



posts = Blueprint('posts',__name__, template_folder='templates')


class ListView(MethodView):
        

	def get(self,page=1):
		max_page = Post.max_post_page_all()
		posts = Post.select().order_by(Post.timestamp.desc()).paginate(page,POST_PER_PAGE).where(Post.published == True)
		return render_template('posts/list.html', posts=posts, page=page, max_page= max_page)


class DetailView(MethodView):
	def get(self, slug):
                query = Post.select()
		post = get_object_or_404(query, Post.slug==slug)
		return render_template('posts/detail.html', post=post, title=post.title)


# Register the urls
posts.add_url_rule('/', view_func=ListView.as_view('list'))
posts.add_url_rule('/index/', view_func=ListView.as_view('index'))
posts.add_url_rule('/<int:page>/', view_func=ListView.as_view('page'))
posts.add_url_rule('/<slug>/', view_func=DetailView.as_view('detail'))
