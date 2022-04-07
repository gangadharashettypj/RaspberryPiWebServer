import cv2
from detecto.core import Model

model = Model.load('model_weights_final.pth',
                   ['Banana Bacterial Wilt', 'Black sigatoka disease', 'Healthy'])


cap = cv2.VideoCapture(0)
cap.set(3, 640)  # set Width
cap.set(4, 480)  # set Height
ret, img = cap.read()
image = cv2.flip(img, 1)
labels, boxes, scores = model.predict(image)
predictions = model.predict(image)

labels, boxes, scores = predictions
print(labels[0])
print(scores[0])

cv2.destroyAllWindows()

