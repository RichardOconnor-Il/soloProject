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
        "dev_id" : session['dev_id']
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

@app.route('/update/game/<int:id>', methods=["POST"])
def update(id):
    if 'dev_id' not in session:
        return redirect('/logout')
    if not Game.validate_game(request.form):
        return redirect('/edit/game/'+ str(id))
    data = {
        "id" : id,
        "name" : request.form['name'],
        "description" : request.form['description'],
        "genre" : request.form['genre'],
        "image" : request.form['image'],
        
    }
    Game.update(data)
    return redirect('/home')

@app.route('/delete/game/<int:id>')
def delete_game(id):
    if 'dev_id' not in session:
        return redirect('/logout')
    data = {
        "id" : id
    }
    Game.delete(data)
    return redirect('/home')

@app.route('/view/games/<int:id>')
def devGames(id):
    if 'dev_id' not in session:
        return redirect('logout')
    if session['dev_id'] != id:
        return redirect('/home')
    print(session['dev_id'])
    data = {
        "id" : id
    }
    dev_data = {
        "id" : session['dev_id']
    }
    return render_template('your_games.html', games = Game.get_all_by_dev(data), dev = Dev.get_by_id(dev_data))