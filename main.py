from detecto.core import Model
import os
from detecto import utils, visualize

from flask import Flask, render_template, Response, request, flash, url_for
from werkzeug.utils import redirect, secure_filename

app = Flask(__name__)
app.secret_key = "secret key"
UPLOAD_FOLDER = 'images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
model = Model.load('model_weights_final.pth',
                   ['Banana Bacterial Wilt', 'Black sigatoka disease', 'Healthy'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return render_template('upload.html')


@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('Image successfully uploaded and displayed below')

        image = utils.read_image(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        labels, boxes, scores = model.predict(image)

        print(labels[0])
        print(scores[0])
        description = ""
        title = ""
        if labels[0] == 'Black sigatoka disease':
            description = 'Pesticide: Thlophanate metryl (1g / 1 Litre of H2O) or Thlophanate methyle (1g / 1 liter of H2O'
            title = 'Disease: Black Sigatoka,  Score: ' + str(scores[0])
        elif labels[0] == 'Banana Bacterial Wilt':
            description = 'Spraying of chlorothanoil (0.2%) and Bavistin (1%) 4 times at 15 days interval'
            title = 'Disease: Anthracnose,  Score: ' + str(scores[0])
        else:
            title = 'Disease: No Disease,  Score: ' + str(scores[0])

        return render_template('upload.html', filename=filename, title=title, description=description)
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)


@app.route('/display/<filename>')
def display_image(filename):
    # print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=3400)
