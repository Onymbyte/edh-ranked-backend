from app import app, db, render_template, request, redirect, url_for
from forms import *
from models import User, PlayRating, EnemyRating, Comment
from flask_login import login_user, login_required, current_user, logout_user, AnonymousUserMixin


@app.route('/', methods=['GET', 'POST'])
def index():
    # print("Getting cursor")
    if isinstance(current_user, AnonymousUserMixin):
        return render_template("base.html")
    else:
        return render_template("base.html", user=current_user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter((User.username==form.username.data) | (User.email==form.email.data)).first() is not None:
            print("User already exists with that Username or Email.")
            return render_template('register.html', form=RegisterForm())
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
    return render_template('register.html', form=form)
@app.route('/login', methods=['GET','POST'])
def login():
  form = LoginForm(csrf_enabled=False)
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    if user and user.check_password(form.password.data):
        print("User exists and password was correct")
        login_user(user, remember=form.remember.data)
        print("User was logged in.")
        next_page = url_for('profile', username=user.username)
        return redirect(next_page) if next_page else redirect(url_for('index', _external=True, _scheme='https'))
    else:
        return redirect(url_for('login', _external=True, _scheme='https'))
  return render_template('login.html', form=form)

@app.route('/profile/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first()
    playRatings = PlayRating.query.filter_by(author_id=user.id).all()
    enemyRatings = EnemyRating.query.filter_by(author_id=user.id).all()
    comments = Comment.query.filter_by(author_id=user.id).all()
    return render_template('profile.html', user=user, play=playRatings, enemy=enemyRatings, comments=comments)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))