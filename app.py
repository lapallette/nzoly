from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import re
from datetime import datetime
import mysql.connector
from mysql.connector import FieldType
import connect

app = Flask(__name__)
dbconn = None
connection = None

def getCursor():
    global dbconn
    global connection
    connection = mysql.connector.connect(user=connect.dbuser, \
    password=connect.dbpass, host=connect.dbhost, \
    database=connect.dbname, autocommit=True)
    dbconn = connection.cursor()
    return dbconn

@app.route("/")
def home():
    return render_template("base.html")

@app.route("/listmembers")
def listmembers():
    connection = getCursor()
    connection.execute("SELECT m.MemberID, t.TeamName, m.FirstName, m.LastName, m.City, m.Birthdate FROM members AS m JOIN teams AS t ON m.TeamID = t.TeamID;")
    memberList = connection.fetchall()
    # print(memberList)
    return render_template("memberlist.html", memberlist = memberList)    

@app.route("/listevents")
def listevents():
    connection = getCursor()
    connection.execute("SELECT * FROM events;")
    eventList = connection.fetchall()
    return render_template("eventlist.html", eventlist = eventList)

@app.route("/member/<memberid>")
def memberdetails(memberid):
    sql = """SELECT M.FirstName, M.LastName, 
    ER.PointsScored, ER.Position, 
    ES.StageName, ES.StageDate, ES.Qualifying, ES.PointsToQualify, ES.Location,
    E.EventName, E.Sport
    from members as M
    LEFT Join event_stage_results as ER ON M.MemberID = ER.MemberID
    LEFT Join event_stage as ES ON ER.StageID = ES.StageID
    LEFT Join events as E ON ES.EventID = E.EventID
    WHERE M.MemberID = %s"""
    connection = getCursor()
    connection.execute(sql, (memberid,))
    memberdetails = connection.fetchall()
    print(memberdetails)
    return render_template("memberdetails.html", memberdetails = memberdetails)  

@app.route("/admin", methods=['GET'])
def admin():
    return render_template("admin.html")


@app.route("/admin_search", methods=['GET'])
def admin_search():
    events = request.args.get('events') 
    members = request.args.get('members')    
    search_results = perform_search(events, members) 
    return render_template("admin_search.html", search_results=search_results)
def get_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="luckyGRACE1023",
        database="nzoly"
    )
    return connection
def perform_search(events, members):
    connection = get_connection()
    cursor = connection.cursor()

    sql = "SELECT * FROM members WHERE FirstName LIKE %s OR LastName LIKE %s"
    query = f"%{members}%"
    
    cursor.execute(sql, (query, query))
    search_results = cursor.fetchall()

    cursor.close()
    connection.close()

    return search_results

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'luckyGRACE1023',
    'database': 'nzoly',
    'port': '3306'
}
conn = mysql.connector.connect(**db_config)

@app.route('/add_member', methods=['GET', 'POST'])
def add_member():
    if request.method == 'POST':
        member_id = request.form.get('member_id')
        team_id = request.form.get('team_id')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        city = request.form.get('city')
        birthday = request.form.get('birthday')
        cursor = conn.cursor()
        sql = "INSERT INTO members (MemberID, TeamID, FirstName, LastName, City, Birthdate) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (member_id, team_id, first_name, last_name, city, birthday)
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        return "Member added to the database successfully"
    else:
        return render_template('add_member.html')

@app.route("/add_event", methods=['GET', 'POST'])
def add_event():
    if request.method == 'POST':
        event_id = request.form.get('event_id')
        event_name = request.form.get('event_name')
        sport = request.form.get('sport')
        nz_team = request.form.get('nz_team')
        cursor = conn.cursor()
        sql = "INSERT INTO events (EventID, EventName, Sport, NZTeam) VALUES (%s, %s, %s, %s)"
        values = (event_id, event_name, sport, nz_team)
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        return "Event added to the database successfully"
    else:
        return render_template('add_event.html')

@app.route("/event_stage", methods=['GET', 'POST'])
def event_stage():
    if request.method == 'POST':
        stage_id = request.form.get('stage_id')
        stage_name = request.form.get('stage_name')
        location = request.form.get('location')
        stage_date = request.form.get('stage_date')
        qualifying = request.form.get('qualifying')
        points_to_qualify = request.form.get('points_to_qualify')
        cursor = conn.cursor()
        sql = "INSERT INTO event_stage (StageID, StageName, Location, StageDate, Qualifying, PointsToQualify) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (stage_id, stage_name, location, stage_date, qualifying, points_to_qualify)
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        return "Event Stage added to the database successfully"
    else:
        return render_template('add_event_stage.html')

@app.route("/add_scores", methods=['POST'])
def add_scores():
    event_stage = request.form.get('event_stage')  
    score = request.form.get('score') 
    return "Scores added to the database successfully"

@app.route("/reports", methods=['GET'])
def generate_reports():
    gold_count = 10
    silver_count = 8
    bronze_count = 6
    winners = [
        {'name': 'John Doe', 'team': 'Team A'},
        {'name': 'Jane Smith', 'team': 'Team B'},
    ]
    winners_sorted = sorted(winners, key=lambda x: (x['name'].split(' ')[-1], x['name'].split(' ')[0]))

    grouped_members = {}  
    for winner in winners_sorted:
        team = winner['team']
        if team not in grouped_members:
            grouped_members[team] = []
        grouped_members[team].append(winner)
    return render_template("reports.html", gold_count=gold_count, silver_count=silver_count, bronze_count=bronze_count, grouped_members=grouped_members)

app.run(debug=True)


