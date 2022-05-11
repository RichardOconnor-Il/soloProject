from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Game:
    db_name = "game_review"
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.genre = data['genre']
        self.image = data['image']
        self.dev_id = data['dev_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO games (name, description, genre, image, dev_id) VALUES (%(name)s, %(description)s, %(genre)s, %(image)s, %(dev_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM games;"
        results = connectToMySQL(cls.db_name).query_db(query)
        games = []
        for row in results:
            games.append(cls(row))
        return games

    @classmethod
    def update(cls, data):
        query = "UPDATE games SET name = %(name)s, description = %(description)s, genre = %(genre)s, image = %(image)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM games WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_one_game(cls, data):
        query = "SELECT * FROM games WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return cls(results[0])

    @classmethod
    def get_all_by_dev(cls, data):
        query = "SELECT * FROM games WHERE dev_id = %(id)s"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        games = []
        for row in results:
            games.append(cls(row))
        return games

    @staticmethod
    def validate_game(game):
        is_vaild = True
        if len(game['name']) < 4:
            flash('The game name needs at minimum 4 characters', 'game_error')
            is_vaild = False
        if len(game['description']) < 25:
            flash('Description must be a minimum of 25 characters', 'game_error')
            is_vaild = False
        if len(game['genre']) < 3:
            flash("The genre must have a 3 character minimum", 'game_error')
            is_vaild = False
        return is_vaild