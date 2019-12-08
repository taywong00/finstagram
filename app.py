import json, os #requests #url_for, urllib2
from flask import Flask, render_template, request, session, redirect, url_for, flash, send_file
# from util import translate, feed_help, datamuse
import pymysql.cursors
import datetime

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
        SELECT * FROM Photo NATURAL JOIN Person WHERE photoPoster = username
        AND (
    	(allFollowers = 1 AND photoPoster IN
            (SELECT username_followed FROM Follow WHERE username_follower = "TestUser"))
    	OR
    	(allFollowers = 0 AND photoID IN
            (SELECT photoID FROM SharedWith NATURAL JOIN BelongTo WHERE member_username = "TestUser"))
        )
        ORDER BY postingdate DESC
    '''
    cursor.execute(query)
    # store result of query in variable (if more than one row, use fetchall())
    data = cursor.fetchall()
    cursor.close() # close cursor when done

    return render_template("home.html", data = data)




@app.route('/details', methods=['GET', 'POST'])
def details():
    if not session.get('username'): # User logged in
        return redirect('/') # redirect to hompage

    photoID = request.form.get("photoID")
    print(photoID)

    # cursor used to execute queries
    cursor = connection.cursor()

    # general post data
    query = '''
    SELECT * FROM Photo NATURAL JOIN Person WHERE photoID = %s AND username = photoPoster
    '''
    cursor.execute(query, (int(photoID)))
    data = cursor.fetchone()

    # likes
    query = "SELECT * FROM Likes WHERE photoID = %s"
    cursor.execute(query, (photoID))
    # store result of query in variable (if more than one row, use fetchall())
    likes = cursor.fetchall()

    # tags
    query = "SELECT * FROM Tagged NATURAL JOIN Person WHERE photoID = %s AND tagstatus = 1"
    cursor.execute(query, (photoID))
    # store result of query in variable (if more than one row, use fetchall())
    tags = cursor.fetchall()

    cursor.close() # close cursor when done

    return render_template("details.html", likes = likes, tags = tags, data = data)





@app.route('/create', methods=['GET', 'POST'])
def create():
    if not session.get('username'): # User logged in
        return redirect('/') # redirect to hompage

    # cursor used to execute queries
    cursor = connection.cursor()

    query = "SELECT * FROM Person WHERE username = %s"
    cursor.execute(query, (session["username"]))
    # store result of query in variable (if more than one row, use fetchall())
    data = cursor.fetchone()

    # postNum
    query = "SELECT COUNT(photoID) AS value FROM Photo WHERE photoPoster = %s"
    cursor.execute(query, (session["username"]))
    postNum = cursor.fetchone()

    # followerNum
    query = "SELECT COUNT(username_follower) AS value FROM `Follow` WHERE username_followed = %s AND followstatus = 1"
    cursor.execute(query, (session["username"]))
    followerNum = cursor.fetchone()

    # followingNum
    query = "SELECT COUNT(username_followed) AS value FROM `Follow` WHERE username_follower = %s AND followstatus = 1"
    cursor.execute(query, (session["username"]))
    followingNum = cursor.fetchone()

    # FriendGroups
    query = "SELECT groupName, owner_username FROM `BelongTo` WHERE member_username = %s"
    cursor.execute(query, (session["username"]))
    friendgroups = cursor.fetchall()

    cursor.close() # close cursor when done

    return render_template("create.html", data = data,
    postNum = postNum["value"], followerNum = followerNum["value"], followingNum = followingNum["value"],
    friendgroups = friendgroups)




@app.route('/submitPost', methods=['GET', 'POST'])
def submitPost():
    if not session.get('username'): # User logged in
        return redirect('/') # redirect to hompage

    filepath_input = request.form.get("filepath_input")
    caption_input = request.form.get("caption_input")
    allFollowers_input = request.form.get("allFollowers_input")
    selected_friendgroups = request.form.getlist("selected_friendgroups")
    date_time = datetime.datetime.now()

    # cursor used to execute queries
    cursor = connection.cursor()
    query = "SELECT max(PhotoID) AS value FROM Photo"
    cursor.execute(query)
    curr_photoID = int((cursor.fetchone())["value"]) + 1

    # add photo post to db -- add to Photo table
    query = '''
    INSERT INTO Photo(`photoID`, `postingdate`, `filepath`, `allFollowers`, `caption`, `photoPoster`)
    VALUES (%s, %s, %s, %s, %s, %s)
    '''
    cursor.execute(query, (curr_photoID, date_time, filepath_input, int(allFollowers_input), caption_input, session["username"]))
    connection.commit()


    # share with friendgroups -- add to SharedWith table
    for curr_ind in range(0, len(selected_friendgroups)):
        curr_groupName = selected_friendgroups[curr_ind].split(",")[0]
        curr_owner_username = selected_friendgroups[curr_ind].split(",")[1]

        query = '''
        INSERT INTO `SharedWith`(`groupOwner`, `groupName`, `photoID`)
        VALUES (%s,%s,%s)
        '''
        cursor.execute(query, (curr_owner_username, curr_groupName, curr_photoID))
        connection.commit()

    cursor.close()


    return redirect("/home")



@app.route("/logout",methods=['POST','GET'])
def logout():
    if 'username' in session:
        session.pop('username')
        return render_template('index.html', message = 'Logout was successful.')
    else:
        return redirect("/")

if __name__ == "__main__":
    app.debug = True
    app.run()
