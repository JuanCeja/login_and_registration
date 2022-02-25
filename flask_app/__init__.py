from flask import Flask, session

app=Flask(__name__)

app.secret_key = "21"

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)