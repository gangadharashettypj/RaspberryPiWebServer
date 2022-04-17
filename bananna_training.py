import cv2
from detecto.core import Model
model = Model.load('bananna_model.pth',['Banana Bacterial Wilt', 'Black sigatoka disease', 'Healthy'])
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
ret, img = cap.read()
image = cv2.flip(img, 1)
labels, boxes, scores = model.predict(image)
print(labels[0])
print(scores[0])

cv2.destroyAllWindows()