# import required modules
from flask import Flask, render_template, url_for, redirect, Response, request
import sqlite3
import os
from random import randint
from camera_pi import Camera
from securitysystem.pantilt import PanTilt

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

# RUN ALL THREE NODE_CLIENTS to create three local dbs 
# and all info should be updated on all pages
# **** TODO ****
# i need to exit these after shutdown since they are infinite loops

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

# @app.route("/<servo>/<angle>")
# def move(servo, angle):
# 	global panServoAngle
# 	global tiltServoAngle

# 	if (servo == 'pan'):
#         if (angle == '+'):
#             panServoAngle = panServoAngle + 10
#         else: 
#             panServoAngle = panServoAngle - 10
#         servo_control.change_pan_angle(panServoAngle) 
	
#     if (servo == 'tilt'):
# 		if (angle == '+'):
# 			tiltServoAngle = tiltServoAngle + 10
# 		else:
# 			tiltServoAngle = tiltServoAngle - 10
#         servo_control.change_tilt_angle(tiltServoAngle) 

# 	templateData = {
#         'panServoAngle'	: panServoAngle,
#         'tiltServoAngle'	: tiltServoAngle
# 	}
	
#     return render_template('security.html', **templateData)

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
	return render_template('index.html', **templateData)

# *************************************************************************************************

@app.route("/light")
def light():
    conn = get_lp_db_connection()
    rows = conn.execute('SELECT * FROM lightclapper').fetchall()
    conn.close()
    return render_template("light.html", title='LightClapper', rows=rows)

# *************************************************************************************************

@app.route("/temperature")
def temperature():
    data = {}
    temperature = []
    labels = []
    colors = []

    conn = get_ts_db_connection()
    rows = conn.execute('SELECT * FROM tempsensor').fetchall()
    conn.close()

    for row in rows:
        location = row['location']
        tempVal = row['tempVal']
        if location not in data.keys():
            data[location] = 0
        data[location] = data[location]+tempVal

    for k, v in data.items():
        R = randint(0, 255)
        G = randint(0, 255)
        B = randint(0, 255)
        labels.append(k)
        temperature.append(v)
        colors.append("rgb({r},{g},{b})".format(r=R,g=G,b=B))

    return render_template("temperature.html", title='TempSensor', rows=rows, tempData=temperature, colorData=colors, tempLabels=labels)

# *************************************************************************************************

if __name__ == "__main__":
    app.run(debug=True, threaded=True)
