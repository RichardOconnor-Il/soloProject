from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Review:
    db_name = "game_review"
    def __init__(self, data):
        self.id = data['id']
        self.review = data['review']
        self.rating = data['rating']
        self.game_id = data['game_id']
        self.dev_id = data['dev_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO reviews (review, rating, game_id, dev_id) VAULES (%(review)s, %(rating)s, %(game_id)s, %(dev_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM reviews;"
        results = connectToMySQL(cls.db_name).query_db(query)
        reviews = []
        for row in results:
            reviews.append(cls(row))
        return reviews

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM reviews WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @staticmethod
    def validate_review(review):
        is_valid = True
        if len(review['review']) < 25:
            flash('The review must be at least 25 characters')
            is_valid = False
        return is_valid