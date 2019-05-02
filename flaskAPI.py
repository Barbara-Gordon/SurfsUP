import sqlite3
from datetime import datetime
from flask import Flask, jsonify, render_template

app = Flask(__name__)

@app.route("/")
def welcome():
 
    return render_template('home.html')

@app.route("/api/v1.0/precipitation")
def make_it_rain():
    conn = sqlite3.connect("c://Users//enc82//Documents//Github//Surfs_UP//Resources//hawaii.sqlite")
    cur = conn.cursor()

    cur.execute('SELECT date, prcp FROM measurement')
    rows = cur.fetchall()
    rain_list = []
    for r in rows:
        rain_list.append(r)
    
    return jsonify(rain_list)

@app.route("/api/v1.0/stations")
def stations():
    conn = sqlite3.connect("c://Users//enc82//Documents//Github//Surfs_UP//Resources//hawaii.sqlite")
    cur = conn.cursor()
    
    cur.execute('SELECT * FROM station')
    rows = cur.fetchall()
    stat_list = []
    for r in rows:
        stat_list.append(r)
    
    return jsonify(stat_list)

@app.route("/api/v1.0/tobs")
def hot_in_hurr():
    conn = sqlite3.connect("c://Users//enc82//Documents//Github//Surfs_UP//Resources//hawaii.sqlite")
    cur = conn.cursor()
    cur.execute('SELECT date, tobs FROM measurement order by date DESC limit 365')
    rows = cur.fetchall()
    temp_data = []
    for r in rows:
        temp_data.append(r)
    
    return jsonify(temp_data)   


############## CHECK the FLASK API thing that Sean updated for GET/POST 

@app.route("/api/v1.0/<start>")
def MMA_Temps(start):
    conn = sqlite3.connect("c://Users//enc82//Documents//Github//Surfs_UP//Resources//hawaii.sqlite")
    cur = conn.cursor()

    start = str(start)
    date = start[:-2] + "-" + start[-2:]

    cur.execute('SELECT min(tobs),max(tobs),avg(tobs) FROM measurement WHERE date like ?', ('%'+date+"%",))

    rows = cur.fetchall()
    for r in rows:
        results = r
    min_temp,max_temp,avg_temp = results
    if None in results:
        return("Bummer dude, did you enter your date correctly? Make sure you enter the date in the following format - 'MMDD'.")
    return (f"The chillest temperature recorded on {date} was {min_temp}, but it's gotten all the way up to {max_temp}! Woah. But you can expect it to be around {avg_temp}. Radical!")

@app.route("/api/v1.0/<start>/<end>")
def vacation_Temps(start,end):
    conn = sqlite3.connect("c://Users//enc82//Documents//Github//Surfs_UP//Resources//hawaii.sqlite")
    cur = conn.cursor()

    start = str(start)
    Sdate ="2017-" + start[:-2] + "-" + start[-2:]

    end = str(end)
    Edate = "2017-" + end[:-2] + "-" + end[-2:]

    cur.execute('SELECT min(tobs),max(tobs),avg(tobs) FROM measurement WHERE date BETWEEN ? AND ?', (Sdate,Edate))

    rows = cur.fetchall()
    for r in rows:
        results = r
    min_temp,max_temp,avg_temp = results

    if None in results:
        return("Bummer dude, did you enter your dates correctly? Make sure you only include the date in the following format - 'MMDD'.")

    return (f"Last year, the lowest temperature was {min_temp}, but it's got all the way up to {max_temp}! Woah. But you can expect it to be around {avg_temp}. Radical!")


if __name__ == '__main__':

    app.run(debug=True)
