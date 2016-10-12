from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
app = Flask(__name__)
mysql = MySQLConnector(app,'full_friend')

@app.route('/')
def index():
    query = "SELECT * FROM friends"
    friends = mysql.query_db(query)
    return render_template('index.html', friends = friends)

@app.route('/friends', methods=["POST"])
def add_friend():
    print 'add_friend'
    query = "INSERT INTO friends(first_name, last_name, occupation, created_at) VALUES(:first_name, :last_name, :occupation, NOW())"
    data = {
            "first_name": request.form["first_name"],
            "last_name": request.form["last_name"],
            "occupation": request.form["occupation"]
            }
    mysql.query_db(query, data)
    return redirect('/')

@app.route('/friends/<id>/edit', methods = ["GET", "POST"])
def edit(id):
    print 'edit'
    return render_template("update.html", id = id)

@app.route('/friends/<id>', methods = ["POST"])
def update(id):
    print 'update'
    query = "SELECT * FROM friends WHERE id = :id"
    data = {
            "id": id
            }
    current = mysql.query_db(query, data)[0]
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    occupation =  request.form["occupation"]
    if len(first_name)< 1:
        first_name = current["first_name"]
    if len(last_name) < 1:
        last_name = current["last_name"]
    if len(occupation) < 1:
        occupation = current["occupation"]
    query = 'UPDATE friends SET first_name = :first_name, last_name = :last_name, occupation = :occupation WHERE id = :id'
    data = {
            "first_name": first_name,
            "last_name": last_name,
            "occupation": occupation,
            "id": id
            }
    mysql.query_db(query, data)
    return redirect('/')

@app.route('/friends/<id>/deleted', methods = ["POST"])
def destroy(id):
    query = "DELETE FROM friends WHERE id = :id"
    data = {"id": id}
    mysql.query_db(query, data)
    return redirect('/')

@app.route("/friends/<id>/delete", methods =["POST"])
def confirm(id):
    return render_template('confirm.html', id = id)

app.run(debug=True)
