from flask_app import app, bcrypt
from flask import render_template, redirect, request, session
from flask_app.models.model_user import User
#from flask_app.models.model_table_name import class_name

@app.route('/')
def index():
    if 'uuid' in session:
        return redirect('/success')
    return render_template('index.html')

@app.route('/success')
def success():
    if 'uuid' not in session:
        return redirect('/')
    return render_template('success.html')

@app.route("/login/user", methods=['post'])
def login():
    is_valid = User.validator_login(request.form)

    if not is_valid:
        return redirect('/')

    return redirect('/')

@app.route('/logout')
def logout():
    del session['uuid']
    return redirect('/')


@app.route("/create/user", methods=["post"])
def create_User():
    # Run Validation before creating user
    is_valid = User.validator(request.form)

    if is_valid == False:
        return redirect('/')

    hash_pw = bcrypt.generate_password_hash(request.form['pw'])
    data = {
        **request.form,
        'pw': hash_pw
    }

    id = User.create(data)
    return redirect('/')

# @app.route("/tablename/<int:id>")
# def show_tablename():
#     pass

# @app.route("/tablename/<int:id>/edit")
# def edit_tablename(id):
#     tablename = tablename.get_one({'id':id})
#     return render_template('tablename_edit.html', tablename=tablename)

# @app.route("/tablename/<int:id>/update", methods=["post"])
# def update_tablename(id):
#     tablename.update_one(request.form)
#     return redirect('/')

# @app.route("/tablename/<int:id>/delete")
# def delete_tablename(id):
#     tablename.delete_one({'id': id})
#     return redirect('/')

# @app.route("/tablename/new")
# def new_tablename():
#     return render_template('tablename_new.html')