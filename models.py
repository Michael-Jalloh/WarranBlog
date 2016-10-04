from peewee import *
import re
import datetime
from hashlib import md5
from flask import Markup
from markdown import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.extra import ExtraExtension
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from playhouse.sqlite_ext import *
from atom import flask_db, database, login_manager


ppp  = 5



class User(UserMixin, flask_db.Model):
	email = CharField(unique=True, default='')
	username = CharField()
	password_hash = CharField()
	admin = BooleanField(default=False)
	about_me = TextField(default='')

	def avatar(self, size):
				return 'https://secure.gravatar.com/avatar/%s?d=identicon&s=%d' %( md5(self.email.encode('utf-8')).hexdigest(), size)

	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')



	@property
	def html_content(self):
                
	# This function will be use to turn our post content into html
		hilite = CodeHiliteExtension(linenums=False, css_class='highlight')
		extras = ExtraExtension()
		content = self.converter()
		markdown_content = markdown(content, extensions=[hilite, extras])
		#       oembed_content = parse_html(
		#               markdown_content,
				#       oembed_providers,
		#               urlize_all=True,
		#               maxwidth=SITE_WIDTH)

		return Markup(markdown_content)


	def converter(self):
                conv = ''
		content = self.about_me
		while 1:
        		try:
                        	if '<pre>' in content:
                                        first, rest = content.split('<pre>',1)
					code, content = rest.split('</pre>',1)
					conv = conv+first.replace('\n','<br>')+'<pre>'+code+'</pre>'
				else:
					conv = conv + content.replace('\n','<br>')
					break
			except:
				break
		return conv


	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)
	
	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	
	@login_manager.user_loader
	def load_user(user_id):
		return User.get(User.id == int(user_id))

class Post(flask_db.Model):
	title = CharField()
	slug = CharField(unique=True)
	published = BooleanField(default=False,index=True)
	timestamp = DateTimeField(default=datetime.datetime.utcnow, index=True)
	content = TextField()
	face_book = CharField(default='') # This is the field that will hold our face_book share link
	
	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = re.sub('[^\w]+', '-', self.title.lower())
		ret = super(Post, self).save(*args, **kwargs)
		return ret


	def converter(self):
		conv = ''
		content = self.content
		while 1:
			try:
				if '<pre>' in content:
					first, rest = content.split('<pre>',1)
					code, content = rest.split('</pre>',1)
					conv = conv+first.replace('\n','<br>')+'<pre>'+code+'</pre>'
				else:
					conv = conv + content.replace('\n','<br>')
					break
			except:
				break
		return conv

	@classmethod
	def max_post_page_all(self):
		m = float(Post.select().count())/ ppp
		n = Post.select().count()/ ppp
		if m>n:
			n = n +1
		return n
		
	@classmethod
	def max_post_page_public(self):
		m = float(Post.public().count())/ ppp
		n = Post.public().count() / ppp
		if m>n:
			n = n + 1
		return n
		

	@property
	def html_content(self):
	# This function will be use to turn our post content into html
		hilite = CodeHiliteExtension(linenums=False, css_class='highlight')
		extras = ExtraExtension()
		content = self.converter()
		markdown_content = markdown(content, extensions=[hilite, extras])
	#	oembed_content = parse_html(
	#		markdown_content,
		#	oembed_providers,
	#		urlize_all=True,
	#		maxwidth=SITE_WIDTH)

		return Markup(markdown_content)





	@classmethod
	def public(cls):
		return Post.select().where(Post.published == True)


	
	@classmethod
	def private(cls):
		return Post.select().where(Post.published == False)


	

	

class Staff(flask_db.Model):
        name = CharField()
        email = CharField(default='')
        bio = TextField(default='')
        position = CharField(default='')

        @property
        def html_content(self):
                # This function will be used to turn our biography into html code
                hilite = CodeHiliteExtension(linenums=False, css_class='highlight')
                extras = ExtraExtension()
                content = self.converter()
                markdown_content = markdown(content, extensions=[hilite, extras])
                return Markup(markdown_content)

	def avatar(self, size):
		return 'https://secure.gravatar.com/avatar/%s?d=identicon&s=%d' %( md5(self.email.encode('utf-8')).hexdigest(), size)


        def converter(self):
                conv = ''
                content = self.bio
                while 1:
                        try:
                                if '<pre>' in content: # <pre> is use to signify the begining of a code sample
                                        first, rest = content.split('<pre>',1)
                                        code, content = rest.split('</pre>',1) # get the code side
                                        conv = conv +first.replace('\n','<br>')+'<pre>'+code+'</pre>'
                                else:
                                        conv = conv + content.replace('\n','<br>')
                                        break

                        except:
                                break
                return conv
	@classmethod
	def max_staff_page_all(self):
		m = float(Staff.select().count()) / ppp
		n = Staff.select().count() / ppp
		if m > n:
			n = n +1
		return n        

database.create_tables([User, Post, Staff], safe=True)
