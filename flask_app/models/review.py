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
        query = "INSERT INTO reviews (review, rating, game_id, dev_id) VALUES (%(review)s, %(rating)s, %(game_id)s, %(dev_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all_by_game(cls, data):
        query = "SELECT * FROM reviews WHERE game_id = %(id)s"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        reviews = []
        for row in results:
            reviews.append(cls(row))
        return reviews

    @classmethod
    def get_avg_rating_for_all(cls):
        query = "select games.id, reviews.game_id, AVG(rating) 'avg' from games left join reviews on games.id = reviews.game_id group by id "
        results = connectToMySQL(cls.db_name).query_db(query)
        print(results)
        return results

    @classmethod
    def get_avg_rating_for_game(cls, data):
        query = "SELECT AVG(rating) 'avg' FROM reviews where game_id = %(id)s"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results[0]

    @staticmethod
    def validate_review(review):
        is_valid = True
        if len(review['review']) < 25:
            flash('The review must be at least 25 characters', "review_error")
            is_valid = False
        return is_valid