from flask import Flask, url_for, render_template, jsonify, request
import matplotlib.pyplot
from env.passwords import sqlpassword
import mysql.connector
import random, math, os
import matplotlib



app = Flask(__name__)




@app.route("/")
def index():
    return render_template("index.html", 
                           font_url1 = "https://fonts.googleapis.com/css2?family=Poppins:wght@200;300;400;600;700&display=swap",
                           font_url2 = "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css")





@app.route("/login")
def loginpage():
    return render_template("login.html",
                           box_url='https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css',
                           font_url = 'https://kit.fontawesome.com/81cbcd9b09.js')





@app.route('/homepage/<username>')
def homepage(username):
    return render_template('homepage.html',
                           username = username)





@app.route('/profile/<username>')
def profile(username):
    try:
        conn = mysql.connector.connect(host='localhost',
                                       username='root',
                                       password=sqlpassword,
                                       database='mp2a')
        
        cursor = conn.cursor()

        cursor.execute("select * from profile where username = %s;", (username,))
        
        result = cursor.fetchone()
        if result:
            userdata = {'username': result[0], 'fname': result[1], 'lname': result[2], 'joiningdate': str(result[3]), 'userlevel': str(result[4])}
        
                
            return render_template('profile.html',
                                    userdata = userdata)
        
        else:
            return 
    
    #USE DOMContentLoad for better practise        

    except Exception as e:
        print("\n\n", e, "\n\n")

    finally:
        cursor.close()
        conn.close()



    return render_template('profile.html',
                           userdata = username)





@app.route("/updateprofile/<username>", methods = ['POST',])
def updateprofile(username):
    data = request.get_json()
    try:
        
        conn = mysql.connector.connect(host='localhost',
                                    username='root',
                                    password=sqlpassword,
                                    database='mp2a')
        
        cursor = conn.cursor()
        query = "update profile set fname = %s, lname = %s where username = %s;"
        cursor.execute(query, (data['fname'], data['lname'], username))
        # print("\n\n",data)
        conn.commit()
        

        
    except Exception as e:
        print("\n\n", e, "\n\n")
        return jsonify({"status": "ERROR=> " + str(e)})

    finally:
        cursor.close()
        conn.close()
        
    return jsonify({"status": "ok"})





@app.route("/handleLogin", methods=['POST',])
def handleLogin():
    data = request.get_json()
    username = data['username']
    password = data['password']

    try:
        conn = mysql.connector.connect(host='localhost',
                                       username='root',
                                       password=sqlpassword,
                                       database='mp2a')
        
        cursor = conn.cursor()

        cursor.execute("select * from login where username = %s and password = %s", (username, password))
        
        result = cursor.fetchone()
        if result:
            return ({'status': 'ok'})
        else:
            return ({'status': 'error'})
        

    except Exception as e:
        print("\n\n", e, "\n\n")

    finally:
        cursor.close()
        conn.close()





@app.route('/handleRegister', methods=['POST',])
def handleRegister():
    payload = request.get_json()
    try:
        conn = mysql.connector.connect(host = 'localhost',
                                       username = 'root',
                                       password = sqlpassword,
                                       database = 'mp2a')
    
        cursor = conn.cursor()

        cursor.execute("insert into login values( %s, %s );", (payload['username'], payload['password']))
        cursor.execute("insert into profile(username, fname, lname, joining) values( %s, %s, %s, NOW() );", (payload['username'], payload['fname'], payload['lname']))
        cursor.execute("insert into scores(username) values(%s);", (payload['username'],))
        cursor.execute("insert into streaks(username) values(%s);", (payload['username'],))
        
        cursor.execute("select word_id from words;")
        word_ids = cursor.fetchall()
        for word_id in word_ids:
            cursor.execute("insert into userprogress(username, word_id) values( %s, %s );", (payload['username'], word_id[0]))


        conn.commit()

        return jsonify({})
    
    except mysql.connector.errors.IntegrityError as e:
        print("\n\n{} Error type: {}\n\n".format(e, type(e)))
        return jsonify({'integrityError': 'Integrity ERROR => '+ str(e)})

    except Exception as e:
        print("\n\n{} Error type: {}\n\n".format(e, type(e)))
        return jsonify({'otherError': 'Other ERROR => '+ str(e)})


    finally:
        cursor.close()
        conn.close()





@app.route("/learn/<username>")
def learn(username):
    return render_template("learn.html")





@app.route("/getwords/<username>")
def getwords(username):
    
    try:
        conn = mysql.connector.connect(host='localhost',
                                       username='root',
                                       password=sqlpassword,
                                       database='mp2a')
        
        cursor = conn.cursor()

        query = "select word, meaning, correct_answers, incorrect_answers, box_level, word_id from userprogress natural join words where username = %s and difficulty = (select userlevel from profile where username = %s) and box_level != 5;"
        cursor.execute(query, (username, username))
        result = cursor.fetchall()

        words = []

        for i in range(5):
            word_index = math.floor(random.random() * len(result))
            temp_word = result[word_index]

            words.append({"word": temp_word[0], "meaning": temp_word[1], "correct_answers": temp_word[2], "incorrect_answers": temp_word[3], "box_level": temp_word[4], "word_id": temp_word[5]})

        return jsonify(words)
        

    except Exception as e:
        print("\n\n", e, "\n\n")

    finally:
        cursor.close()
        conn.close()





@app.route("/updatewords/<username>", methods = ['POST',])
def updatewords(username):
    data = request.get_json()
    try:

        for word in data:
            conn = mysql.connector.connect(host='localhost',
                                        username='root',
                                        password=sqlpassword,
                                        database='mp2a')
            
            cursor = conn.cursor()

            query = "update userprogress set box_level = %s, correct_answers = %s, incorrect_answers = %s where username = %s and word_id = %s;"
            cursor.execute(query, (word['box_level'], word['correct_answers'], word['incorrect_answers'], username, word['word_id']))
            # print(word)
            conn.commit()
        

        
    except Exception as e:
        print("\n\n", e, "\n\n")
        return jsonify({"status": "ERROR=> " + str(e)})

    finally:
        cursor.close()
        conn.close()
        
    return jsonify({"status": "ok"})





@app.route("/getstreak/<username>")
def getstreak(username):

    try:

        conn = mysql.connector.connect(host='localhost',
                                        username='root',
                                        password=sqlpassword,
                                        database='mp2a')
            
        cursor = conn.cursor()

        query = "select username, laststreak, streak_count from streaks where username = %s"
        cursor.execute(query, (username,))

        result = cursor.fetchone()
        # print("GET STREAK: ",result)
            
        return jsonify({"username": result[0], "laststreak": result[1], "streak_count": result[2]})
    

    except Exception as e:
        print("\n\n", e, "\n\n")
        return jsonify({"status": "ERROR=> " + str(e)})

    finally:
        cursor.close()
        conn.close()






@app.route("/updatestreak/<username>", methods = ['POST',])
def updatestreak(username):
    data = request.get_json()

    try:
        conn = mysql.connector.connect(host='localhost',
                                        username='root',
                                        password=sqlpassword,
                                        database='mp2a')
            
        cursor = conn.cursor()

        query = "update streaks set laststreak = %s, streak_count = %s where username = %s;"
        cursor.execute(query, (data['laststreak'], data['streak_count'], username))
        # print("SET STREAK : ", data)
        conn.commit()
        

        
    except Exception as e:
        print("\n\n", e, "\n\n")
        return jsonify({"status": "ERROR=> " + str(e)})

    finally:
        cursor.close()
        conn.close()
        
    return jsonify({"status": "ok"})





@app.route("/getuserlevel/<username>")
def getuserlevel(username):
    try:
        conn = mysql.connector.connect(host='localhost',
                                        username='root',
                                        password=sqlpassword,
                                        database='mp2a')
            
        cursor = conn.cursor()

        query = "select username, userlevel from profile where username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
            
        return jsonify({"username": result[0], "userlevel": result[1]})
    

    except Exception as e:
        print("\n\n", e, "\n\n")
        return jsonify({"status": "ERROR=> " + str(e)})

    finally:
        cursor.close()
        conn.close()





@app.route("/updateuserlevel/<username>", methods = ['POST',])
def updateuserlevel(username):
    data = request.get_json()

    try:
        conn = mysql.connector.connect(host='localhost',
                                        username='root',
                                        password=sqlpassword,
                                        database='mp2a')
            
        cursor = conn.cursor()

        query = "update profile set userlevel = %s where username = %s;"
        cursor.execute(query, (data['userlevel'], username))
        conn.commit()
        

        
    except Exception as e:
        print("\n\n", e, "\n\n")
        return jsonify({"status": "ERROR=> " + str(e)})

    finally:
        cursor.close()
        conn.close()
        
    return jsonify({"status": "ok"})





@app.route("/getscores/<username>")
def getscores(username):
    try:
        conn = mysql.connector.connect(host='localhost',
                                        username='root',
                                        password=sqlpassword,
                                        database='mp2a')
            
        cursor = conn.cursor()

        query = "select username, score1, score2, score3, score4, score5 from scores where username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
            
        return jsonify({"username": result[0], "score1": result[1], "score2": result[2], "score3": result[3], "score4": result[4], "score5": result[5]})
    

    except Exception as e:
        print("\n\n", e, "\n\n")
        return jsonify({"status": "ERROR=> " + str(e)})

    finally:
        cursor.close()
        conn.close()





@app.route("/updatescores/<username>", methods = ['POST',])
def updatescores(username):
    data = request.get_json()
    # print("\n\n Update Scores: ", data)
    try:
        conn = mysql.connector.connect(host='localhost',
                                        username='root',
                                        password=sqlpassword,
                                        database='mp2a')
            
        cursor = conn.cursor()

        query = "update scores set score1 = %s, score2 = %s, score3 = %s, score4 = %s, score5 = %s  where username = %s;"
        cursor.execute(query, (data['score1'], data['score2'], data['score3'], data['score4'], data['score5'], username))
        conn.commit()


    except Exception as e:
        print("\n\n", e, "\n\n")
        return jsonify({"status": "ERROR=> " + str(e)})

    finally:
        cursor.close()
        conn.close()
        
    return jsonify({"status": "ok"})





@app.route("/review/<username>")
def review(username):
    return render_template("quiz.html")





@app.route("/getmasteredwords/<username>")
def getmasteredwords(username):
    try:
        conn = mysql.connector.connect(host='localhost',
                                        username='root',
                                        password=sqlpassword,
                                        database='mp2a')
            
        cursor = conn.cursor()

        query = "select word, meaning from words natural join userprogress where username = %s and box_level = 5;"
        cursor.execute(query, (username,))
        result = cursor.fetchall()

        if len(result) < 5:
            return jsonify({"error": "You need to master more words :D"})

        mastered_words = []
        for i in range(5):
            word_index = math.floor(random.random() * len(result))
            temp_word = result.pop(word_index)
            temp = {"word": temp_word[0], "meaning": temp_word[1]}
            mastered_words.append(temp)
            
        # print(mastered_words)
        return jsonify(mastered_words)
    

    except Exception as e:
        print("\n\n", e, "\n\n")
        return jsonify({"status": "ERROR=> " + str(e)})

    finally:
        cursor.close()
        conn.close()





@app.route("/stats/<username>")
def stats(username):
    try:
        conn = mysql.connector.connect(host='localhost',
                                        username='root',
                                        password=sqlpassword,
                                        database='mp2a')
            
        cursor = conn.cursor()
        query = "select username, score1, score2, score3, score4, score5 from scores where username = %s"
        cursor.execute(query, (username,))

        result = cursor.fetchone()

        scores = [result[i + 1] for i in range(5)]
        xlabels = [" ", "  ", "   ", "    ", "     "]
        matplotlib.use('agg')
        matplotlib.pyplot.plot(xlabels, scores, color="g")
        matplotlib.pyplot.xlabel("Practise")
        matplotlib.pyplot.ylabel("Scores")
        matplotlib.pyplot.grid()
        matplotlib.pyplot.savefig("static/images/stat.png")
        matplotlib.pyplot.close()


        query = "select box_level from userprogress where username = %s and box_level = 5;"
        cursor.execute(query, (username,))
        result = cursor.fetchall()
        mastered_words = len(result)
        mastered_words_progress = (mastered_words * 100) / 370


        query = "select box_level from userprogress where username = %s and box_level != 0;"
        cursor.execute(query, (username,))
        result = cursor.fetchall()
        learning_words = len(result)
        learning_words_progress = (learning_words * 100) / 370


        query = "select count(word_id) from words;"
        cursor.execute(query)
        result = cursor.fetchall()
        totalwords = result[0][0]

        # print(mastered_words_progress, learning_words_progress)


    except Exception as e:
        print("\n\n", e, "\n\n")
        return jsonify({"status": "ERROR=> " + str(e)})

    finally:
        cursor.close()
        conn.close()

    return render_template("stats.html", 
                           mastered_words_progress = str(mastered_words_progress), 
                           mastered_words = str(mastered_words),
                           learning_words_progress = learning_words_progress, 
                           learning_words = learning_words,
                           totalwords = totalwords)






if __name__ == "__main__":
    app.run(debug=True)