from flask import Flask, render_template
from flask_login import LoginManager
from playhouse.flask_utils import FlaskDB
from flask_mail import Mail
from config import config
from threading import Thread
SITE_WIDTH = 800
application = Flask(__name__)
application.config.from_object(config['production'])
config['production'].init_app(application)

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view ='auth.login'

flask_db = FlaskDB(application)
database = flask_db.database
mail = Mail(application)


# Send a mail in the background
def send_async_email(app, msg):
	with app.app_context():
		mail.send(msg)
# This is the mailing function
def send_mail(to, subject, template, **kwargs):
	msg = Message(application['MAIL_SUBJCT_PREFIX'] + subject,
			sender=application.config['MAIL_SENDER'], recipents=[to])
	msg.body = render_template(template +'.txt', **kwargs)
	msg.html = render_tamplate(template + '.html', **kwargs)
	thr = Thread(target=send_async_email, args=[applicaton, msg])
	thr.start()
	return thr

def register_blueprints(app):
	# Prevents circular imports
	from views import posts
	from admin import admin
	from auth import auth
	from profile import profile
	from errors import errors
	from defaults import defaults
	from staffs import staff
	app.register_blueprint(posts)
	app.register_blueprint(admin)
	app.register_blueprint(auth)
	app.register_blueprint(profile)
	app.register_blueprint(errors)
	app.register_blueprint(defaults)
	app.register_blueprint(staff)

	@app.errorhandler(404)
	def page_nt_found(e):
                return render_template('404.html')
        @app.errorhandler(500)
        def internal_server_error(e):
                return render_template('500.html')
	login_manager.init_app(app)


register_blueprints(application)

if __name__ == '__main__':
	application.run()
