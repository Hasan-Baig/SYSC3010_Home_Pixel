# import required modules
from flask import Flask, render_template, url_for, redirect, Response, request
import sqlite3
import os
from random import randint
from camera_pi import Camera
from securitysystem.pantilt import PanTilt
from lightclapper.constants import ON_INT
import math

app = Flask(__name__)

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

# Global variables definition and initialization
global panServoAngle
global tiltServoAngle
panServoAngle = 90
tiltServoAngle = 90

#start up pantilt servos
servo_control = PanTilt()
servo_control.start_servo()
servo_control.change_pan_angle(panServoAngle)
servo_control.change_tilt_angle(tiltServoAngle)

# RUN ALL THREE NODE_CLIENTS to create three local databases 
# ALL info should be updated on the tables of all pages

#methods to access all databases
def get_ss_db_connection():
    conn = sqlite3.connect('securitysystem/securitysystem.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_lp_db_connection():
    conn = sqlite3.connect('lightclapper/lightclapper.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_ts_db_connection():
    conn = sqlite3.connect('tempsensor/tempsensor.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    return render_template("home.html")

# *************************************************************************************************

@app.route("/about")
def about():
    return render_template("about.html")

# *************************************************************************************************

@app.route("/security")
def security():
    templateData = {
      'panServoAngle'	: panServoAngle,
      'tiltServoAngle'	: tiltServoAngle
	}

    conn = get_ss_db_connection()
    rows = conn.execute('SELECT * FROM securitysystem').fetchall()
    conn.close()

    return render_template("security.html", title='SecuritySystem', rows=rows, **templateData)


def gen(camera):
   """Video streaming generator function."""
   while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route("/video_feed")
def video_feed():
   """Video streaming route. Put this in the src attribute of an img tag."""
   return Response(gen(Camera()),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/<servo>/<angle>")
def move(servo, angle):
	global panServoAngle
	global tiltServoAngle
	if servo == 'pan':
		if angle == '+':
			panServoAngle = panServoAngle + 10
		else:
			panServoAngle = panServoAngle - 10
		servo_control.change_pan_angle(panServoAngle)
	if servo == 'tilt':
		if angle == '+':
			tiltServoAngle = tiltServoAngle + 10
		else:
			tiltServoAngle = tiltServoAngle - 10
		servo_control.change_tilt_angle(tiltServoAngle)

	templateData = {
      'panServoAngle'	: panServoAngle,
      'tiltServoAngle'	: tiltServoAngle
	}

	return render_template('security.html', **templateData)

# *************************************************************************************************

@app.route("/light")
def light():
    # Intialize data for graph
    data = {}
    activity = []
    current_status = []
    labels = []
    colors = []

    conn = get_lp_db_connection()
    rows = conn.execute('SELECT * FROM lightclapper').fetchall()
    conn.close()

    # Iterate to check for new locations
    for row in rows:
        location = row['location']
        status = row['lightStatus']
        if location not in data.keys():
            # tuple: (sum of LED on, latest LED status)
            data[location] = (0, status)
        data[location] = (data[location][0] + status, status)

    # Iterate for colors and lists
    # Note: random colors for dynamic color assignment (scalability)
    for location, v in data.items():
        R = randint(0, 255)
        G = randint(0, 255)
        B = randint(0, 255)
        colors.append("rgb({r},{g},{b})".format(r=R,g=G,b=B))

        sum_of_activity = v[0]
        latest_status = v[1]

        # Hover color for ON (yellow) / OFF (grey)
        if latest_status == ON_INT:
            current_status.append("rgb(255,255,0)")
        else:
            current_status.append("rgb(128,128,128)")

        labels.append(location)
        activity.append(sum_of_activity)

    return render_template("light.html", title='LightClapper', rows=rows,
        lightData=activity, colorData=colors, lightLabels=labels, status=current_status)

# *************************************************************************************************

@app.route("/temperature")
def temperature():
    data = {}
    labels = []
    current_status = []
    tempValues = []
    colors = []

    conn = get_ts_db_connection()
    rows = conn.execute('SELECT * FROM tempsensor').fetchall()
    conn.close()

    # Iterate to check for new locations
    for row in rows:
        location = row['location']
        status = row['fanStatus']
        temperature = round(row['tempVal'],2)
        if location not in data.keys():
            # tuple: (temperature, latest fan status)
            data[location] = (0, status)
        data[location] = (temperature, status)

    # Iterate for colors and lists
    for k, v in data.items():
        R = randint(0, 255)
        G = randint(0, 255)
        B = randint(0, 255)
        colors.append("rgb({r},{g},{b})".format(r=R,g=G,b=B))

        labels.append(k)
        tempValues.append(v[0])
        latest_status = v[1]
        colors.append("rgb({r},{g},{b})".format(r=R,g=G,b=B))

        # Hover color for ON (yellow) / OFF (grey)
        if latest_status == ON_INT:
            current_status.append("rgb(255,255,0)")
        else:
            current_status.append("rgb(128,128,128)")

    return render_template("temperature.html", title='TempSensor', rows=rows, 
        tempValues=tempValues, colorData=colors, tempLabels=labels, status=current_status)

# *************************************************************************************************

if __name__ == "__main__":
    app.run(debug=True, threaded=True)
