from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
import re
from flask_app import bcrypt

DATABASE = "user_login"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.pw = data['pw']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, pw) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(pw)s);"
        users_id = connectToMySQL(DATABASE).query_db(query, data) #returs id of the new row created
        return users_id

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"

        results = connectToMySQL(DATABASE).query_db(query)

        if results:
            users_names = []
            for user in results:
                users_names.append(cls(user))
            return users_names
        return []

    @classmethod
    def get_one(cls, data:dict) -> object:
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data) #returns us a LIST of DICTIONARIES
        if result:
            return cls(result[0])
        return False

    @classmethod
    def get_one_by_email(cls, data:dict) -> object:
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query, data) #returns us a LIST of DICTIONARIES
        print(result)
        if result:
            return cls(result[0])
        return False

    # ------------------- CREATE/REGISTER VALIDATION----------------------------

    @staticmethod
    def validator(form_data):
        is_valid = True

        if len(form_data['first_name']) < 2:
            is_valid = False
            flash("First name must be atleast 2 characters long", "err_user_first_name")
        
        if len(form_data['last_name']) < 2:
            is_valid = False
            flash("Last name must be atleast 2 characters long", "err_user_last_name")

        if len(form_data['email']) < 2:
            is_valid = False
            flash("Email is required", "err_user_email")

        if not EMAIL_REGEX.match(form_data['email']): 
            flash("Invalid email address!", "err_user_email")
            is_valid = False

        if len(form_data['pw']) < 2:
            is_valid = False
            flash("Password is required", "err_user_pw")

        if len(form_data['confirm_pw']) < 2:
            is_valid = False
            flash("Confirm password is required", "err_user_confirm_pw")

        elif form_data['confirm_pw'] != form_data['pw']:
            is_valid = False
            flash("Passwords do not match", "err_user_confirm_pw")

        return is_valid

        # -------------LOGIN VALIDATION----------------------

    @staticmethod
    def validator_login(form_data):
        is_valid = True

        if len(form_data['email']) < 2:
            is_valid = False
            flash("Email is required", "err_user_email_login")

        elif not EMAIL_REGEX.match(form_data['email']): 
            flash("Invalid email address!", "err_user_email_login")
            is_valid = False

        if len(form_data['pw']) < 2:
            is_valid = False
            flash("Password is required", "err_user_pw_login")

        else:
            potential_user = User.get_one_by_email({'email': form_data['email']})
            print(potential_user)
            if not potential_user:
                is_valid = False
                flash("invalid credentials", "err_user_pw_login")
            elif not bcrypt.check_password_hash(potential_user.pw, form_data['pw']):
                flash('invalid credentials', 'err_user_pw_login')
            else:
                session['uuid'] = potential_user.id
                
        return is_valid


    # @classmethod
    # def update_one(cls, data):
    #     query = "UPDATE table SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, WHERE id = %(id)s;"
    #     return connectToMySQL(DATABASE).query_db(query, data)

    # @classmethod
    # def update(cls, data):
    #     query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, updated_at=NOW() WHERE id = %(id)s;"
    #     updated_result = connectToMySQL(DATABASE).query_db(query, data)
    #     return updated_result

    # @classmethod
    # def delete_one(cls, data):
    #     query = "DELETE FROM table WHERE id = %(id)s;"
    #     return connectToMySQL(DATABASE).query_dba(query, data)

    # @classmethod
    # def save(cls, data):
    #     query = "INSERT INTO users (first_name, last_name, email) VALUES(%(first_name)s, %(last_name)s, %(email)s);"
    #     result = connectToMySQL(DATABASE).query_db(query,data)
    #     return result