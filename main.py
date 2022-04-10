import cv2
from detecto.core import Model
from flask import Flask, render_template, Response
from camera import VideoCamera

app = Flask(__name__)
# model = Model.load('model_weights_final.pth',
#                    ['Banana Bacterial Wilt', 'Black sigatoka disease', 'Healthy'])


@app.route('/')
def index():
    return render_template('index.html')


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video/<command>')
def video(command):
    if command == "CAPTURE":

        # cap = cv2.VideoCapture(0)
        # cap.set(3, 640)
        # cap.set(4, 480)
        # ret, img = cap.read()
        # image = cv2.flip(img, 1)
        # labels, boxes, scores = model.predict(image)
        #
        # print(labels[0])
        # print(scores[0])
        description = ""
        title = ""
        # if labels[0] == 'Black sigatoka disease':
        #     description = 'Pesticide: Thlophanate metryl (1g / 1 Litre of H2O) or Thlophanate methyle (1g / 1 liter of H2O'
        #     title = 'Disease: Black Sigatoka,  Score: ' + str(scores[0])
        # elif labels[0] == 'Banana Bacterial Wilt':
        #     description = 'Spraying of chlorothanoil (0.2%) and Bavistin (1%) 4 times at 15 days interval'
        #     title = 'Disease: Anthracnose,  Score: ' + str(scores[0])
        # else:
        #     title = 'Disease: No Disease,  Score: ' + str(scores[0])


        title = 'Disease: No Disease,  Score: '
        return render_template('index.html', label=title, description=description)
    else:
        return render_template('index.html', label='')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=3400)
