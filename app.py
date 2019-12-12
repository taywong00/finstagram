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
    else: return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if session.get('username'): # User logged in
        return redirect('/home') # redirect to hompage
    else:
        return render_template("register.html") # bring them to register form


@app.route('/process_register', methods=['GET', 'POST'])
def process_register():
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
            print("user found in database, exists already")
            return render_template("register.html", error=error)
        else: # User doesn't exist yet, account can be created
            insert_query = "INSERT INTO Person (username, password) VALUES(%s, %s)"
            cursor.execute(insert_query, (username, password))
            # commit changes for insert to go through
            connection.commit()
            cursor.close() # close cursor when done
            print("User doesn't exist yet, account can be created")
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
            (SELECT username_followed FROM Follow WHERE username_follower = %s))
    	OR
    	(allFollowers = 0 AND photoID IN
            (SELECT photoID FROM SharedWith NATURAL JOIN BelongTo
            WHERE owner_username = groupOwner AND member_username = %s))
        )
        ORDER BY postingdate DESC
    '''
    cursor.execute(query, (session["username"], session["username"]))
    # store result of query in variable (if more than one row, use fetchall())
    data = cursor.fetchall()
    cursor.close() # close cursor when done

    return render_template("home.html", data = data)




@app.route('/details', methods=['GET', 'POST'])
def details():
    if not session.get('username'): # User logged in
        return redirect('/') # redirect to hompage

    try: # got photoID through the details button in home (form)
        photoID = request.form.get("photoID")
        session["photoID"] = photoID
        # print("********** DETAILS FORM VERION: " + photoID)
    except: # got photoID from session through approve/decline tag routes
        photoID = session["photoID"]
        # print("********** DETAILS SESSION VERION: " , photoID)


    # cursor used to execute queries
    cursor = connection.cursor()

    # general post data
    query = '''
    SELECT * FROM Photo NATURAL JOIN Person
    WHERE photoID = %s AND username = photoPoster
    '''
    cursor.execute(query, (photoID))
    data = cursor.fetchone()

    # likes
    query = "SELECT * FROM Likes WHERE photoID = %s"
    cursor.execute(query, (photoID))
    # store result of query in variable (if more than one row, use fetchall())
    likes = cursor.fetchall()

    # tags
    query = '''
    SELECT * FROM Tagged NATURAL JOIN Person
    WHERE photoID = %s
    '''
    cursor.execute(query, (photoID))
    # store result of query in variable (if more than one row, use fetchall())
    tags = cursor.fetchall()



    cursor.close() # close cursor when done

    myusername = session["username"]
    return render_template("details.html", likes = likes, tags = tags, data = data, myusername = myusername)





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




    # testing

    query = '''
    SELECT * FROM Photo WHERE photoID = %s
    '''
    cursor.execute(query, (curr_photoID))
    photo_data = cursor.fetchone()
    print(photo_data)

    print(selected_friendgroups)





    # share with friendgroups -- add to SharedWith table
    for curr_ind in range(0, len(selected_friendgroups)):
        curr_groupName = selected_friendgroups[curr_ind].split(",")[0]
        curr_owner_username = selected_friendgroups[curr_ind].split(",")[1]

        print(curr_groupName)
        print(curr_owner_username)

        query = '''
        INSERT INTO `SharedWith`(`groupOwner`, `groupName`, `photoID`)
        VALUES (%s,%s,%s)
        '''
        cursor.execute(query, (curr_owner_username, curr_groupName, curr_photoID))
        connection.commit()

    cursor.close()

    return redirect("/home")



@app.route('/myposts', methods=['GET', 'POST'])
def myposts():
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

    # load my photos
    query = '''
    SELECT photoID, filepath
    FROM Photo
    WHERE photoPoster = %s
    ORDER BY postingdate DESC
    '''
    cursor.execute(query, (session["username"]))
    # store result of query in variable (if more than one row, use fetchall())
    myphotos = cursor.fetchall()


    cursor.close() # close cursor when done

    return render_template("myposts.html", data = data,
    postNum = postNum["value"], followerNum = followerNum["value"], followingNum = followingNum["value"],
    myphotos = myphotos)






@app.route('/taggedin', methods=['GET', 'POST'])
def taggedin():
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

    # load my photos
    query = '''
    SELECT photoID, filepath
    FROM `Tagged` NATURAL JOIN Photo
    WHERE username = %s AND tagstatus = 1
    ORDER BY postingdate DESC
    '''
    cursor.execute(query, (session["username"]))
    # store result of query in variable (if more than one row, use fetchall())
    taggedphotos = cursor.fetchall()


    cursor.close() # close cursor when done

    return render_template("taggedin.html", data = data,
    postNum = postNum["value"], followerNum = followerNum["value"], followingNum = followingNum["value"],
    taggedphotos = taggedphotos)


@app.route('/follows', methods=['GET', 'POST'])
def follows():
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

    # follow_requests
    query = '''
    SELECT username_follower FROM `Follow` WHERE username_followed = %s AND followstatus = 0
    '''
    cursor.execute(query, (session["username"]))
    follow_requests = cursor.fetchall()


    cursor.close() # close cursor when done

    return render_template("follows.html", data = data,
    postNum = postNum["value"], followerNum = followerNum["value"], followingNum = followingNum["value"],
    follow_requests = follow_requests)




@app.route('/search_user_to_follow', methods=['GET', 'POST'])
def search_user_to_follow():
    if not session.get('username'): # User logged in
        return redirect('/') # redirect to hompage

    searched_username = request.form.get("searched_username")

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

    # follow_requests
    query = '''
    SELECT username_follower FROM `Follow` WHERE username_followed = %s AND followstatus = 0
    '''
    cursor.execute(query, (session["username"]))
    follow_requests = cursor.fetchall()


    # user entered a searched username
    if searched_username:
        #check if user exists in db

        query = "SELECT * FROM Person WHERE username = %s"
        cursor.execute(query, (searched_username))
        # store result of query in variable (if more than one row, use fetchall())
        user_data = cursor.fetchone()


        if user_data: # user found/exists
            try: # try adding a follow request to the database
                query = '''
                INSERT INTO `Follow`(`username_followed`, `username_follower`, `followstatus`)
                VALUES (%s,%s,0)
                '''
                cursor.execute(query, (searched_username))
                # commit changes for insert to go through
                connection.commit()
            except: # query could not be executed, entry exists
                error = "You have already requested to follow this user."
        else: # user not found/does not exist
            error = "That user does not exist."


    cursor.close() # close cursor when done

    return render_template("follows.html", data = data,
    postNum = postNum["value"], followerNum = followerNum["value"], followingNum = followingNum["value"],
    follow_requests = follow_requests, error = error)





@app.route('/approve_follow_request', methods=['GET', 'POST'])
def approve_follow_request():
    if not session.get('username'): # User logged in
        return redirect('/') # redirect to hompage

    user_who_requested_me = request.form.get("user_who_requested_me")

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

    # update follow table
    query = '''
    UPDATE `Follow` SET `followstatus`= 1
    WHERE `username_followed`=%s AND `username_follower`=%s
    '''
    cursor.execute(query, (session["username"], user_who_requested_me))
    # commit changes for insert to go through
    connection.commit()
    message = user_who_requested_me + " approved."

    # follow_requests
    query = '''
    SELECT username_follower FROM `Follow` WHERE username_followed = %s AND followstatus = 0
    '''
    cursor.execute(query, (session["username"]))
    follow_requests = cursor.fetchall()



    cursor.close() # close cursor when done

    return render_template("follows.html", data = data,
    postNum = postNum["value"], followerNum = followerNum["value"], followingNum = followingNum["value"],
    follow_requests = follow_requests, message = message)



@app.route('/delete_follow_request', methods=['GET', 'POST'])
def delete_follow_request():
    if not session.get('username'): # User logged in
        return redirect('/') # redirect to hompage

    user_who_requested_me = request.form.get("user_who_requested_me")

    # cursor used to execute queries
    cursor = connection.cursor()

    query = "SELECT * FROM Person WHERE username = %s"
    cursor.execute(query, (session["username"]))
    # store result of query in variable (if more than one row, use fetchall())
    data = cursor.fetchone()

    # update follow table
    query = '''
    DELETE FROM `Follow`
    WHERE username_followed = %s AND username_follower = %s
    '''
    cursor.execute(query, (session["username"], user_who_requested_me))
    # commit changes for insert to go through
    connection.commit()
    message = user_who_requested_me + " removed from Follow Requests."

    # follow_requests
    query = '''
    SELECT username_follower FROM `Follow` WHERE username_followed = %s AND followstatus = 0
    '''
    cursor.execute(query, (session["username"]))
    follow_requests = cursor.fetchall()


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


    cursor.close() # close cursor when done

    return render_template("follows.html", data = data,
    postNum = postNum["value"], followerNum = followerNum["value"], followingNum = followingNum["value"],
    follow_requests = follow_requests, message = message)



@app.route('/tags', methods=['GET', 'POST'])
def tags():
    if not session.get('username'): # User logged in
        return redirect('/') # redirect to hompage

    # user_who_requested_me = request.form.get("user_who_requested_me")

    # cursor used to execute queries
    cursor = connection.cursor()

    query = "SELECT * FROM Person WHERE username = %s"
    cursor.execute(query, (session["username"]))
    # store result of query in variable (if more than one row, use fetchall())
    data = cursor.fetchone()

    # # update follow table
    # query = '''
    # DELETE FROM `Follow`
    # WHERE username_followed = %s AND username_follower = %s
    # '''
    # cursor.execute(query, (session["username"], user_who_requested_me))
    # # commit changes for insert to go through
    # connection.commit()
    # message = user_who_requested_me + " removed from Follow Requests."

    # load my photos
    query = '''
    SELECT *
    FROM `Tagged` NATURAL JOIN Photo
    WHERE username = %s AND tagstatus = 0
    ORDER BY postingdate DESC
    '''
    cursor.execute(query, (session["username"]))
    # store result of query in variable (if more than one row, use fetchall())
    taggedphotos = cursor.fetchall()


    # follow_requests
    query = '''
    SELECT username_follower FROM `Follow` WHERE username_followed = %s AND followstatus = 0
    '''
    cursor.execute(query, (session["username"]))
    follow_requests = cursor.fetchall()


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


    cursor.close() # close cursor when done

    return render_template("tags.html", data = data,
    postNum = postNum["value"], followerNum = followerNum["value"], followingNum = followingNum["value"],
    follow_requests = follow_requests, taggedphotos = taggedphotos)






@app.route('/approve_tag', methods=['GET', 'POST'])
def approve_tag():
    if not session.get('username'): # User logged in
        return redirect('/') # redirect to hompage

    photoID = request.form.get("photoID")

    # cursor used to execute queries
    cursor = connection.cursor()

    # set tagstatus to 1
    query = '''
    UPDATE `Tagged` SET tagstatus = 1
    WHERE username = %s AND photoID = %s
    '''
    cursor.execute(query, (session["username"], photoID))
    # commit changes for insert to go through
    connection.commit()

    cursor.close() # close cursor when done

    # put photoID in session to "refresh page"
    session["photoID"] = photoID
    # if session["photoID"]:
    #     print("******************session photoid exists: ", session["photoID"])
    # else: print("******************session photoid doesnt exist")
    return redirect("/details")



@app.route('/decline_tag', methods=['GET', 'POST'])
def decline_tag():
    if not session.get('username'): # User logged in
        return redirect('/') # redirect to hompage

    photoID = request.form.get("photoID")

    # cursor used to execute queries
    cursor = connection.cursor()

    # delete tag request from table
    query = '''
    DELETE FROM `Tagged`
    WHERE username = %s AND photoID = %s
    '''
    cursor.execute(query, (session["username"], photoID))
    # commit changes for insert to go through
    connection.commit()

    cursor.close() # close cursor when done

    # put photoID in session to "refresh page"
    session["photoID"] = photoID
    # if session["photoID"]:
    #     print("******************session photoid exists: ", session["photoID"])
    # else: print("******************session photoid doesnt exist")
    return redirect("/details")





@app.route('/suggestTags', methods=['GET', 'POST'])
def suggestTags():
    if not session.get('username'): # User logged in
        return redirect('/') # redirect to hompage

    photoID = session["photoID"]
    if 'error' in session:
        error = session["error"]
        session.pop('error')
        # print(error, "***** SUGGEST TAGS ******")

    else: error = None


    # cursor used to execute queries
    cursor = connection.cursor()

    # general post data
    query = '''
    SELECT * FROM Photo NATURAL JOIN Person WHERE photoID = %s AND username = photoPoster
    '''
    cursor.execute(query, (int(photoID)))
    data = cursor.fetchone()


    # tags
    query = '''
    SELECT * FROM Tagged NATURAL JOIN Person
    WHERE photoID = %s
    '''
    cursor.execute(query, (photoID))
    # store result of query in variable (if more than one row, use fetchall())
    tags = cursor.fetchall()


    cursor.close() # close cursor when done

    return render_template("suggesttags.html", tags = tags, data = data, myusername = session["username"], error = error)



# for both suggesting a new tag and approving self tag
@app.route('/tag_suggestion_made', methods=['GET', 'POST'])
def tag_suggestion_made():
    if not session.get('username'): # User logged in
        return redirect('/') # redirect to hompage

    suggested_username = request.form.get("suggested_username")
    approved = request.form.get("approved")
    error = None

    # cursor used to execute queries
    cursor = connection.cursor()

    # regarding self tag
    if approved:
        if approved == "1": # approved
            # set tagstatus to 1
            print("approved")

            query = '''
            UPDATE `Tagged` SET tagstatus = 1
            WHERE username = %s AND photoID = %s
            '''

        else: #declined
            # delete tag request from table
            print("declined")

            query = '''
            DELETE FROM `Tagged`
            WHERE username = %s AND photoID = %s
            '''
        cursor.execute(query, (session["username"], session["photoID"]))
        # commit changes for insert to go through
        connection.commit()

    # regarding others
    else:
        #check if user exists in db

        query = "SELECT * FROM Person WHERE username = %s"
        cursor.execute(query, (suggested_username))
        # store result of query in variable (if more than one row, use fetchall())
        user_data = cursor.fetchone()

        if user_data:
            # check if user suggested yet in table
            query = '''
            SELECT * FROM `Tagged`
            WHERE username = %s AND photoID = %s
            '''
            cursor.execute(query, (suggested_username, session["photoID"]))
            user_suggested = cursor.fetchone()

            # if user has already been suggested
            if user_suggested:
                error = "This tag has already been suggested."
                # print(error, "***** TAG SUGGESTION MADE ******")
            # else (user not yet suggested/not in table)
            else:
                # if the user can see the photo --> add (username, photoID, 1)
                    # they follow photoPoster and the photo's allFollowers == 1
                    # if photoid shared with friendgroup and user in friendgroup
                query = '''
                    SELECT * FROM Photo
                    WHERE photoID = %s
                    AND (
                	(allFollowers = 1 AND photoPoster IN
                        (SELECT username_followed FROM Follow WHERE username_follower = %s))
                	OR
                	(allFollowers = 0 AND photoID IN
                        (SELECT photoID FROM SharedWith NATURAL JOIN BelongTo
                        WHERE owner_username = groupOwner AND member_username = %s))
                    )
                '''
                cursor.execute(query, (session["photoID"], suggested_username, suggested_username))
                photo_data = cursor.fetchone()

                if photo_data: # means user can see the photo
                    query = '''
                    INSERT INTO `Tagged`(`username`, `photoID`, `tagstatus`)
                    VALUES (%s,%s,0)
                    '''
                    cursor.execute(query, (suggested_username, session["photoID"]))
                    # commit changes for insert to go through
                    connection.commit()
                # else
                else:
                    error = "This post is not visible to that user."
        else:
            error = "There is no such user with that username."

    if error != None: session["error"] = error
    cursor.close() # close cursor when done
    return redirect('/suggestTags')

# @app.route("/goback",methods=['POST','GET'])
# def goback():
#     if 'username' in session:
#         session.pop('username')
#         return render_template('index.html', message = 'Logout was successful.')
#     else:
#         return redirect("/")


@app.route("/logout",methods=['POST','GET'])
def logout():
    if 'username' in session:
        session.pop('username')
    if 'photoID' in session:
        session.pop('photoID')
    if 'error' in session:
        session.pop('error')

        return render_template('index.html', message = 'Logout was successful.')
    else:
        return redirect("/")

if __name__ == "__main__":
    app.debug = True
    app.run()
