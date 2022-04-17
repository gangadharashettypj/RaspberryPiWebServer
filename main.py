from flask import Flask, render_template, Response, send_file
import flask
import cv2
import time
from camera import VideoCamera

app = Flask(__name__)
# Setup camera

frame = None

@app.route('/')
def index():
    return render_template('index.html')


def gen(camera):
    global frame
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video/capture')
def video():
    return Response(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n', mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=3400)
