from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.dev import Dev
from flask_app.models.game import Game
from flask_app.models.review import Review
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=["POST"])
def login():
    dev = Dev.get_by_email(request.form)
    if not dev:
        flash("Invaild Email", 'login_error')
        return redirect('/')
    if not bcrypt.check_password_hash(dev.password , request.form['password']):
        flash('Invaild Password', 'login_error')
        return redirect('/')
    session['dev_id'] = dev.id
    return redirect('/home')

@app.route('/register', methods=["POST"])
def register():
    if not Dev.validate_register(request.form):
        return redirect('/')
    data = {
        "username" : request.form['username'],
        "company" : request.form['company'],
        "email" : request.form['email'],
        "password" : bcrypt.generate_password_hash(request.form["password"])
    }
    id = Dev.save(data)
    session['dev_id'] = id
    return redirect('/home')

@app.route('/home')
def home():
    if 'dev_id' not in session:
        return redirect('/logout')
    data = {
        "id" : session['dev_id']
    }
    return render_template('home.html', dev = Dev.get_by_id(data), games = Game.get_all(), reviews = Review.get_all())

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')