from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.dev import Dev
from flask_app.models.game import Game

@app.route('/add/game')
def newGame():
    if 'dev_id' not in session:
        return redirect('/logout')
    data = {
        "id" : session['dev_id']
    }
    return render_template('add_game.html', dev = Dev.get_by_id(data))

@app.route('/post/game', methods=["POST"])
def add_Game():
    if 'dev_id' not in session:
        return redirect('/logout')
    if not Game.validate_game(request.form):
        return redirect('/add/game')
    data = {
        "name" : request.form['name'],
        "description" : request.form['description'],
        "genre" : request.form['genre'],
        "image" : request.form['image'],
        "dev_id" : request.form['dev_id']
    }
    Game.save(data)
    return redirect('/home')

@app.route('/edit/game/<int:id>')
def edit(id):
    if "dev_id" not in session:
        return redirect('/logout')
    data = {
        "id" : id
    }
    dev_data = {
        "id" : session['dev_id']
    }
    return render_template('edit_game.html', edit = Game.get_one_game(data), dev = Dev.get_by_id(dev_data))

@app.route('/update/game', methods=["POST"])
def update():
    if 'dev_id' not in session:
        return redirect('/logout')
    if not Game.validate_game(request.form):
        return redirect('/edit/game/<int:id>')
    data = {
        "name" : request.form['name'],
        "description" : request.form['description'],
        "genre" : request.form['genre'],
        "image" : request.form['image'],
        "dev_id" : request.form['dev_id']
    }
    Game.update(data)
    return redirect('/home')

