from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash 
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Dev:
    db_name = "game_review"
    def __init__(self, data):
        self.id = data['id']
        self.username = data['username']
        self.company = data['company']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO devs (username, company, email, password) VALUES (%(username)s, %(company)s, %(email)s, %(password)s );"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM devs;"
        results = connectToMySQL(cls.db_name).query_db(query)
        devs = []
        for row in results:
            devs.append(cls(row))
        return devs

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM devs WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return cls(results[0])

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM devs WHERE email = %(email)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @staticmethod
    def validate_register(dev):
        is_valid = True
        query = "SELECT * FROM devs WHERE email = %(email)s;"
        results = connectToMySQL(Dev.db_name).query_db(query, dev)
        if len(results) >= 1:
            flash("Email is already taken")
            is_valid = False
        if not EMAIL_REGEX.match(dev['email']):
            flash("Invalid email address try again", 'register_error')
            is_valid = False
        if len(dev['username']) < 3:
            flash("Username must have at least 3 characters", 'register_error')
            is_valid = False
        if len(dev['company']) < 3:
            flash("Company must have at least 3 characters", 'register_error')
            is_valid = False
        if len(dev['password']) < 8:
            flash("Password must have at least 8 charaters", 'register_error')
            is_valid = False
        if dev['password'] != dev['confirm_password']:
            flash("Password does not match confirmation")
            is_valid = False
        return is_valid