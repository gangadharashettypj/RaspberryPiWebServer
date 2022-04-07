#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  	appCam.py
#  	based on tutorial ==> https://blog.miguelgrinberg.com/post/video-streaming-with-flask
# 	PiCam Local Web Server with Flask
# MJRoBot.org 19Jan18
import cv2
from detecto.core import Model
from flask import Flask, render_template, Response

# Raspberry Pi camera module (requires picamera package)
from camera_pi import Camera

app = Flask(__name__)


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/main/<command>")
def move_forward(command):
    if command == "capture":
        model = Model.load('model_weights_final.pth',
                           ['Banana Bacterial Wilt', 'Black sigatoka disease', 'Healthy'])

        cap = cv2.VideoCapture(0)
        cap.set(3, 640)  # set Width
        cap.set(4, 480)  # set Height
        ret, img = cap.read()
        image = cv2.flip(img, 1)
        labels, boxes, scores = model.predict(image)
        print(labels[0])
        print(scores[0])

        cv2.destroyAllWindows()
        return render_template('index.html', label=labels[0], score=str(scores[0]))

    return render_template('index.html', label='--', score='--')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True, threaded=True)
