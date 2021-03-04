import os
import requests
import time
from flask import Flask, session,render_template,request,redirect,url_for,flash,make_response,jsonify
# from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from db_script import TwitterDb, print_err
import json
from random import randint
from phrase_monitor.config import config
from phrase_monitor.controllers import api

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = config.SESSION_PERMANENT
app.config["SESSION_TYPE"] = config.SESSION_TYPE
# Session(app)

engine = create_engine(config.DATABASE_URL)
db = scoped_session(sessionmaker(bind=engine))
# twitter_db = TwitterDb()

app.register_blueprint(api)


@app.errorhandler(404)
def not_found(error):
    return jsonify(code="404", msg="Resource not found"), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify(code="405", msg="Method not allowed"), 405

#
# @app.route("/")
# def home():
#     return render_template('home.html')
#
# @app.route("/login")
# def log_in():
#     return render_template('login.html')
#
# @app.route("/handle_data", methods=['POST'])
# def handle_data():
#
#     data = request.form
#     email1 = data["email"]
#     pwd = data["pass"]
#     username = data["username"]
#
#     if db.execute("SELECT * from users WHERE username= :u AND password= :p",{"u":username,"p":pwd}).rowcount == 1 :
#         return render_template('already_hehe.html')
#     else:
#         db.execute("INSERT INTO users (email,username,password) VALUES (:e,:u,:p)",{"e":email1,"u":username,"p":pwd})
#         db.commit()
#         return render_template('login.html')
#
#
# @app.route("/after_loggin",methods=["GET","POST"])
# def after_login():
#     data = request.form
#     u = data["username"]
#
#     pwd = data["pwd"]
#
#     result = db.execute("SELECT * from users WHERE username=:u AND password=:p",{"u":u,"p":pwd}).fetchall()
#     for row in result:
#         print("ROW: ", row)
#         if(pwd==row.password):
#                 ts = time.gmtime()
#                 timestamp = time.strftime("%x", ts)
#                 mybool = db.execute("SELECT * FROM blogs WHERE user_id=:u AND created_date=:timestamp",{"u":row[0],"timestamp":timestamp}).rowcount > 0
#                 print(mybool)
#                 if(mybool):
#                     display = False
#                     session['username'] = u
#                     session['user_id'] = str(row[0])
#                     return redirect('/dashboard')
#
#                 else:
#                     display = True
#                     session['username'] = u
#                     session['user_id'] = str(row[0])
#                     return redirect('/dashboard')
#
#         else:
#             message2 = True
#             message = False
#             return render_template('empty.html',message=message,message2=message2)
#
#
# @app.route("/after_submit",methods=["POST"])
# def after_submit():
#     data = request.form
#     blog_text = data["blog-text"]
#     x = request.cookies.get('user_id')
#
#     ts = time.gmtime()
#     timestamp = time.strftime("%x", ts)
#
#     db.execute("INSERT INTO blogs (user_id,text,created_date) VALUES (:u,:t,:c)",{"u":x,"t":blog_text,"c":timestamp})
#     db.commit()
#
#     message = True
#     message2 = False
#
#     return render_template('empty.html',message=message,message2=message2)
#

#
# @app.route("/dashboard")
# def dashboard():
#
#     return render_template('dashboard.html')
#
#
# @app.route("/edit_phrase/<id>", methods=['GET','POST'])
# def edit_phrase(id):
#     if request.method == "POST":
#         try:
#             data = request.form
#             phrase = data["phrase"]
#             db.execute("UPDATE stream_phrases SET phrase = :phrase WHERE id = :id",{"phrase":phrase,"id":id})
#             db.commit()
#             os.system("sudo systemctl restart twitter-streamer-worker")
#             flash("Phrase updated successfully", "success")
#             return redirect('/phrases')
#         except Exception as e:
#             print_err(e)
#             db.rollback()
#             flash("Error updating phrase","error")
#
#
#     phrase = db.execute("SELECT * from stream_phrases WHERE id = :id", {"id": id}).fetchone()
#     print("PHRASE: ",phrase)
#     return render_template('edit_phrase.html',phrase=phrase)
#
#
# @app.route("/phrases", methods=['GET','POST'])
# def phrases():
#     if request.method == "POST":
#         data = request.form
#         phrase = data["phrase"]
#         u_id = request.cookies.get('user_id')
#         ts = time.gmtime()
#         timestamp = time.strftime("%x", ts)
#         try:
#             db.execute("INSERT INTO stream_phrases (user_id,phrase,created_date) VALUES (:u,:p,:c)",{"u":u_id,"p":phrase,"c":timestamp})
#             db.commit()
#             os.system("sudo systemctl restart twitter-streamer-worker")
#             flash("Phrase created successfully", "success")
#         except Exception as e:
#             print_err(e)
#             db.rollback()
#             flash("Phrase already exists","error")
#     result=db.execute("SELECT * from stream_phrases").fetchall()
#     for row in result:
#         print("User: ",row.user_id, "Phrase:",row.phrase, "Created_date:",row.created_date)
#     return render_template('phrases.html',result=result)
#
# @app.route("/phrase_occurrence")
# def phrase_occurrence():
#     data = twitter_db.get_tracked_phrases()
#     return jsonify(data)
#
# @app.route("/average_phrase_per_minute")
# def average_phrase():
#     data = twitter_db.get_average_phrase_per_minute()
#     print("DATA: ",data)
#     new_data = [ {"average_per_min": round(float(d["number_of_tweets"])/float(d["number_of_entries"]), 2), "phrase": d["phrase"]} for d in data]
#     print(new_data)
#     return json.dumps(new_data)
#
# @app.route("/home")
# def home_after_login():
#     return render_template('dashboard.html')
#
# @app.route("/monitor_phrases", methods=["GET","POST"])
# def monitor_phrases():
#     if request.method == "POST":
#         data = request.form
#         phrase = data["phrase"]
#         u_id = request.cookies.get('user_id')
#         ts = time.gmtime()
#         timestamp = time.strftime("%x", ts)
#         try:
#             db.execute("INSERT INTO stream_phrases (user_id,phrase,created_date) VALUES (:u,:p,:c)",{"u":u_id,"p":phrase,"c":timestamp})
#             db.commit()
#         except Exception as e:
#             print_err(e)
#             db.rollback()
#             flash("Phrase already exists","error")
#     result=db.execute("SELECT * from stream_phrases").fetchall()
#     for row in result:
#         print("User: ",row.user_id, "Phrase:",row.phrase, "Created_date:",row.created_date)
#
#     return render_template('monitor_phrases.html', result=results)
#
# @app.route('/chart_data/<duration_type>', methods=['GET'])
# def chart_data(duration_type):
#     final_data = {}
#     if duration_type == "minutes":
#
#         datasets = []
#         phrases = twitter_db.get_phrases()
#         data = twitter_db.get_chart_data_for_minutes()
#         labels = list(set([d["date"] for d in data]))
#         labels = [str(d) for d in labels]
#
#
#         print(labels)
#
#         for phrase in phrases:
#             datasets.append(
#                 {
#                     "label": phrase["phrase"],
#                     "borderColor": "rgb({r},{g},{b})".format(r=randint(0,255),g=randint(0,255),b=randint(0,255)),
#                     "data":[d["number_of_times"] for d in data if d["phrase"] == phrase["phrase"]]
#                  })
#         print("DATA: ",datasets)
#
#         final_data["labels"] = labels
#         final_data["datasets"] = datasets
#         return json.dumps(final_data)
#     # {
#     #   labels: ['9:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00'],
#     #   datasets: [{
#     #     label: 'Volcano',
#     #     // backgroundColor: 'rgb(255, 99, 132)',
#     #     borderColor: 'rgb(255, 99, 132)',
#     #     data: [0, 10, 5, 2, 20, 30, 45]
#     #   },
#     #   {
#     #     label: 'Earthquake',
#     #     // backgroundColor: 'rgb(0, 99, 132)',
#     #     borderColor: 'rgb(0, 99, 132)',
#     #     data: [16, 1, 18, 2, 20, 30, 65]
#     #   }
#     #   ]
#     # }
#
#
# @app.route('/chart_data_single/<id>/<duration_type>', methods=['GET'])
# def chart_data_single(id, duration_type):
#     bands = {
#         "1": {
#             "color": "blue",
#             "rolling_range": [0, 3],
#             "mentions_threshold": 10,
#         },
#         "2": {
#             "color": "green",
#             "rolling_range": [3, 9],
#             "mentions_threshold": 17,
#         },
#         "3": {
#             "color": "yellow",
#             "rolling_range": [9, 15],
#             "mentions_threshold": 27,
#         },
#         "4": {
#             "color": "cyan",
#             "rolling_range": [16, 25],
#             "mentions_threshold": 40,
#         },
#         "5": {
#             "color": "pink",
#             "rolling_range": [25, 40],
#             "mentions_threshold": 60,
#         },
#         "6": {
#             "color": "grey",
#             "rolling_range": [40, 60],
#             "mentions_threshold": 90,
#         },
#         "7": {
#             "color": "black",
#             "rolling_range": [60, 80],
#             "mentions_threshold": 120,
#         }
#     }
#     final_data = {}
#     datasets = []
#     phrase = twitter_db.get_phrase(id)
#
#     data = twitter_db.get_chart_data_by_phrase(id, duration_type)
#     print("data: ",data)
#     labels = list(set([d["date"] for d in data]))
#     labels = [str(d) for d in labels]
#     print("ID: ", id)
#
#     print(labels)
#     datasets.append(
#         {
#             "label": phrase["phrase"],
#             "borderColor": 'rgb(255, 99, 132)',#.format(r=randint(0,255),g=randint(0,255),b=randint(0,255)),
#             "data":[d["number_of_times"] for d in data if d["phrase"] == phrase["phrase"]]
#             })
#     print("DATA: ",datasets)
#
#     rolling_average = twitter_db.get_rolling_average(id)
#     current_average = twitter_db.get_average_phrase_per_minute_by_id(id)
#     current_band = None
#     current_band_type = None
#     for band in bands:
#         if rolling_average > bands[band]["rolling_range"][0] and rolling_average <= bands[band]["rolling_range"][1] and current_average >= bands[band]["mentions_threshold"]:
#             current_band = bands[band]
#             current_band_type = band
#             break
#     if current_band:
#         band_message = "Something serious happened"
#         band_type = current_band_type
#         band_color = current_band["color"]
#     else:
#         band_message = ""
#         band_type = ""
#         band_color = ""
#
#     final_data["band"] = {
#                             "rolling_average": rolling_average,
#                             "message": band_message,
#                             "type": band_type,
#                             "color": band_color
#                         }
#     final_data["canvas_data"] = { "labels": labels, "datasets": datasets }
#
#     return json.dumps(final_data)
#
# @app.route('/<id>/monitor_page', methods=['GET'])
# def monitor_page(id):
#     phrase = twitter_db.get_phrase(id)
#     rolling_average = twitter_db.get_average_phrase_per_minute_by_id(id)
#     return render_template("phrase_monitor_page.html", data={"id": id, "phrase": phrase["phrase"]}, rolling_average=rolling_average)

#
# if __name__ == "__main__":
#     app.run(port=6060)
