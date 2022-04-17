import io
import os

import numpy as np
from flask import Flask, render_template, Response, send_file, make_response
import flask
import cv2
import time

from werkzeug.wsgi import FileWrapper

from camera import VideoCamera
import PIL.Image as Image

app = Flask(__name__)
# Setup camera

image = None
frame = None


@app.route('/')
def index():
    return render_template('index.html')


def gen(camera):
    global image, frame
    while True:
        image, frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video/capture')
def video():
    global image, frame
    directory = r'/Users/gangadharashetty/Code/GitHub/Mine/Video-Streaming-with-Flask/camWebServer/'
    filename = 'savedImage.jpg'
    os.chdir(directory)
    print("Before saving image:")
    print(os.listdir(directory))
    cv2.imwrite(filename, image)
    print(os.listdir(directory))
    return send_file(directory + filename, mimetype='image/jpeg')
    return Response(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n',
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=3400)
