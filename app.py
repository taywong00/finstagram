import json, os #requests #url_for, urllib2
from flask import Flask, render_template, request, session, redirect, url_for, flash, send_file
# from util import translate, feed_help, datamuse
import pymysql.cursors

app = Flask(__name__)
app.secret_key = os.urandom(32)

connection = pymysql.connect(host="localhost",
                             user="root",
                             password="root",
                             db="Finstagram",
                             charset="utf8mb4",
                             port=8889,
                             cursorclass=pymysql.cursors.DictCursor,
                             autocommit=True)

@app.route("/")
def welcome():
    if session.get('username'): # User logged in
        return redirect("/home") # redirect to hompage
    else: # User not logged in
        return render_template("index.html") # present form

@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('username'): # User logged in
        return redirect('/home') # redirect to hompage

    # User entered the login form
    elif request.form.get("login") == "Login":
        # get form info
        username = request.form.get("username")
        password = request.form.get("password")

        # cursor used to execute queries
        cursor = connection.cursor()
        # execute query: look up credentials in database
        query = "SELECT * FROM Person WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        # store result of query in variable (if more than one row, use fetchall())
        data = cursor.fetchone()
        cursor.close() # close cursor when done

        if (data): # user exists/credentials correct
            # create session for the user
            session["username"] = username
            return redirect("/home")
        else: # user does not exist/credentials incorrect
            error = "Invalid login." # *** MAY WANT TO SPECIFY LOGIN ISSUE, ex username vs pass problem ***
            return render_template("index.html", error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if session.get('username'): # User logged in
        return redirect('/home') # redirect to hompage

    # User entered the sign up form
    elif request.form.get("register") == "Register":
        # get form info
        username = request.form.get("username")
        password = request.form.get("password")

        # cursor used to execute queries
        cursor = connection.cursor()
        # execute query: look up username in database
        query = "SELECT * FROM Person WHERE username = %s"
        cursor.execute(query, (username))
        # store result of query in variable (if more than one row, use fetchall())
        data = cursor.fetchone()

        if (data): # User found in database, exists already
            error = "That username is taken."
            cursor.close() # close cursor when done
            return render_template("register.html", error=error)
        else: # User doesn't exist yet, account can be created
            insert_query = "INSERT INTO Person (username, password) VALUES(%s, %s)"
            cursor.execute(insert_query, (username, password))
            # commit changes for insert to go through
            connection.commit()
            cursor.close() # close cursor when done
            return redirect("/login")


@app.route('/home', methods=['GET', 'POST'])
def home():
    if not session.get('username'): # User logged in
        return redirect('/') # redirect to hompage

    # cursor used to execute queries
    cursor = connection.cursor()
    query = '''
        SELECT * FROM Photo WHERE
    	(allFollowers = 1 AND photoPoster IN
            (SELECT username_followed FROM Follow WHERE username_follower = "TestUser"))
    	OR
    	(allFollowers = 0 AND photoID IN
            (SELECT photoID FROM SharedWith NATURAL JOIN BelongTo WHERE member_username = "TestUser"))
        ORDER BY postingdate DESC
    '''
    cursor.execute(query)
    # store result of query in variable (if more than one row, use fetchall())
    data = cursor.fetchall()
    cursor.close() # close cursor when done

    return render_template("home.html", data = data)



@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if not session.get('username'): # User logged in
        return redirect('/') # redirect to hompage

    # cursor used to execute queries
    cursor = connection.cursor()
    query = "SELECT * FROM Person WHERE username = %s"
    cursor.execute(query, (session["username"]))
    # store result of query in variable (if more than one row, use fetchall())
    data = cursor.fetchone()
    cursor.close() # close cursor when done

    return render_template("profile.html", data = data)




@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username')
    return redirect("/")

if __name__ == "__main__":
    app.debug = True
    app.run()
