from flask import Blueprint, render_template
from flask.views import MethodView
from playhouse.flask_utils import get_object_or_404
from models import Post

defaults = Blueprint('defaults',__name__, template_folder='templates')

class WelcomeView(MethodView):
	def get(self):
		query = Post.select()
		post = get_object_or_404(query, Post.title=='Welcome')
		return render_template('posts/detail.html', post=post, title=post.title)

class VisionView(MethodView):
	def get(self):
		query = Post.select()
		post = get_object_or_404(query, Post.title=='Vision')
		return render_template('posts/detail.html',post=post, title=post.title)


class AboutView(MethodView):
	def get(self):
		query = Post.select()
		post = get_object_or_404(query, Post.title=='About')
		return render_template('posts/detail.html',post=post, title=post.title)

class ContactView(MethodView):
	def get(self):
		query = Post.select()
		post = get_object_or_404(query, Post.title=='Contact')
		return render_template('posts/detail.html',post=post, title=post.title)

defaults.add_url_rule('/welcome/',view_func=WelcomeView.as_view('welcome'))
defaults.add_url_rule('/Vision/',view_func=VisionView.as_view('vision'))
defaults.add_url_rule('/about/',view_func=AboutView.as_view('about'))
defaults.add_url_rule('/contact/', view_func=ContactView.as_view('contact'))
