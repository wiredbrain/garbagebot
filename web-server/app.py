from flask import Flask, render_template, request
import datetime
from gpiozero import Motor
from time import sleep

app = Flask(__name__)

right = Motor(9, 10)
left = Motor(8, 7)

@app.route("/")
def controller():
    now = datetime.datetime.now()
    timestring = now.strftime("%Y-%m-%d %H:%M")
    templateData = {
        'title': "HELLO",
        'time': timestring
        }
    return render_template('main.html', **templateData)

@app.route('/move', methods=['GET', 'POST'])
def move():
    movement = request.form['movement']
    print "post request received with movement: ", movement
    if movement == 'forward':
        print "triggering forward action"
        right.forward()
        left.forward()
        sleep(2)
        right.stop()
        left.stop()
    if movement == 'left':
        print 'triggering left action'
        left.forward()
        right.backward()
        sleep(2)
        right.stop()
        left.stop()
    if movement == 'right':
        print 'triggering right action'
        right.forward()
        left.backward()
        sleep(2)
        right.stop()
        left.stop()
    if movement == 'backward':
        print "triggering backward action"
        right.backward()
        left.backward()
        sleep(2)
        right.stop()
        left.stop()
    return "Moving " + movement

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
