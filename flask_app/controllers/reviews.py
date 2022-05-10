from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.dev import Dev
from flask_app.models.game import Game
from flask_app.models.review import Review

@app.route('/view/review/<int:id>')
def reviews(id):
    if 'dev_id' not in session:
        return redirect('/logout')
    data = {
        "id" : id
    }
    dev_data = {
        "id" : session['dev_id']
    }
    return render_template('view_game.html', game = Game.get_one_game(data), dev = Dev.get_by_id(dev_data))
