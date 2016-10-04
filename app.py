from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, logout_user, login_required, login_user
from playhouse.flask_utils import FlaskDB, get_object_or_404
from wtfpeewee.orm import model_form
from my_forms import *
from config import POST_PER_PAGE as ppp



application = Flask(__name__)
application.config.from_object('config')
#bootstrap = Bootstrap(application)


login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = '/login'


flask_db = FlaskDB(application)
database = flask_db.database
login_manager.init_app(application)
from models import *

@application.route('/login/', methods=['GET', 'POST'])
def login():
        form = LoginForm()
        if request.method == 'GET':
                u = User.select().count()
                if u != 0:
                        form = LoginForm()
                        return render_template('login.html',form=form)
                else:
                        content = 'There are no users, please create a user'
                        return render_template('info.html', content=content)
        if request.method == 'POST':
                print 'POST'
                if form.validate_on_submit():
                        print 'Trying out user'
                        try:
                                user = User.get(User.username==form.username.data)
                                if user is not None and user.verify_password(form.password.data):
                                        login_user(user, form.remember_me.data)
                                        print 'Authenticated'
                                        flash('You have been logged in')
                                        return redirect(request.args.get('next') or url_for('index'))
                        except User.DoesNotExist:
                                flash('Login Details Invalid','danger')
        return render_template('login.html', form=form)

@application.route('/logout')
@login_required
def logout():
        logout_user()
        flash('You have been logged out')
        return redirect('/')

@application.route('/create', methods=['GET','POST'])
@login_required
def create():
        form = BlogForm()
        if request.method == 'GET':
                return render_template('create.html', form=form)

        elif request.method == 'POST':
                if form.validate_on_submit():
                        try:
                                print 'Hello' *100
                                post = Post.get(Post.title == form.title.data)
                                post.published = form.publish.data
                                post.content = form.post.data
                                print form.post.data
                                post.face_book = form.face_book.data
                                print form.face_book.data
                                post.save()
                                flash('You post have been saved')
                  
                        except Post.DoesNotExist:
                                post = Post()
                                post.title = form.title.data
                                post.published = form.publish.data
                                post.content = form.post.data
                                post.face_book = form.face_book.data
                                post.save()
                                flash('You post have been saved')

                        except Exception, e:
                                print str(e)
                        
                return render_template('create.html', form=form)


@application.route('/post/<slug>')
def post(slug):
        query = Post.select()
        post = get_object_or_404(query, Post.slug ==slug)
        return render_template('detail.html', post=post)

@application.route('/edit/<slug>', methods=['GET','POST'])
@login_required
def edit(slug):
        form = BlogForm()
        if request.method == 'GET':
                try:
                        query = Post.select()
                        post = get_object_or_404(query,Post.slug==slug)
                        form.title.data = post.title
                        form.publish.data = post.published
                        form.post.data = post.content
                        form.face_book.data = post.face_book
                except:
                        return render_template('info.html', content='No post found for that address')
                
        elif request.method == 'POST':
                try:
                        post = Post.get(Post.title == form.title.data)
                        post.published = form.publish.data
                        post.content = form.post.data
                        print form.post.data
                        post.face_book = form.face_book.data
                        print form.face_book.data
                        post.save()
                        flash('You post have been saved')
                except:
                        flash('Post not saved')

        return render_template('create.html',form=form)
                

@application.route('/delete/<slug>')
@login_required
def delete(slug):
        try:
                query = Post.select()
                post = get_object_or_404(query, Post.slug==slug)
                title = post.title
                post.delete_instance()
                print title +' deleted'
                flash(title + ' have been deleted from the database')
        except:
                flash('Could Not delete ' + title)

        return redirect('/admin')
                

        
@application.route('/admin')
@login_required
def admin_page():
         posts = Post.select()
         return render_template('admin_list.html', posts=posts)

        
@application.route('/page')
@application.route('/<int:page>')
def page(page=1):
        max_page = Post.max_post_page_public()
        posts = Post.public()
        posts = posts.order_by(Post.timestamp.desc()).paginate(page,ppp)
        print page
        type(page)
        return render_template('list.html',posts=posts, page=page, max_page=max_page)


@application.route('/')
def index():
        query = Post.select()
        post = get_object_or_404(query, Post.title=='Welcome')
        return render_template('detail.html',post=post)



@application.errorhandler(404)
def page_not_found(e):
        return render_template('404.html'), 404

@application.errorhandler(500)
def internal_server_error(e):
        return render_template('500.html'), 500


@application.route('/secret')
@login_required
def secret():
        return render_template('info.html',content='Only autheenticated users are allowed!')





if __name__ =='__main__':
	application.run()
