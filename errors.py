from flask import Blueprint, render_template
from flask.views import MethodView


errors = Blueprint('errors', __name__, template_folder='templates')

class e404(MethodView):
	
	def get(self):
		return render_template('404.html')



class e500(MethodView):
	def get(self):
		return render_template('500.html')


# Register th urls
errors.add_url_rule('/404/', view_func=e404.as_view('404'))
errors.add_url_rule('/500/', view_func=e500.as_view('500'))

