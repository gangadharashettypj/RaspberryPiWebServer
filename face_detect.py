import cv2

faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier('Mouth.xml')
nose_cascade = cv2.CascadeClassifier('Nariz.xml')

cap = cv2.VideoCapture(0)
cap.set(3, 640)  # set Width
cap.set(4, 480)  # set Height
while True:
    ret, img = cap.read()
    img = cv2.flip(img, 1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(20, 20)
    )

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.putText(img, 'face', (x, y - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 1, cv2.LINE_AA)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]

    eyes = eye_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=20,
        minSize=(20, 20)
    )
    for (ex, ey, ew, eh) in eyes:
        cv2.rectangle(img, (ex, ey), (ex + ew, ey + eh), (0, 0, 0), -1)
        cv2.putText(img, 'eyes', (ex, ey - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 1, cv2.LINE_AA)

    # smile = smile_cascade.detectMultiScale(
    #     gray,
    #     scaleFactor=1.1,
    #     minNeighbors=20,
    #     minSize=(20, 20)
    # )
    # for (ex, ey, ew, eh) in smile:
    #     cv2.rectangle(img, (ex, ey), (ex + ew, ey + eh), (0, 0, 0), -1)
    #     cv2.putText(img, 'mouth', (ex, ey - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 1, cv2.LINE_AA)

    # nose = nose_cascade.detectMultiScale(
    #     gray,
    #     scaleFactor=1.1,
    #     minNeighbors=20,
    #     minSize=(20, 20)
    # )
    # for (ex, ey, ew, eh) in nose:
    #     cv2.rectangle(img, (ex, ey), (ex + ew, ey + eh), (0, 0, 0), -1)
    #     cv2.putText(img, 'nose', (ex, ey - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 1, cv2.LINE_AA)

    cv2.imshow('video', img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:  # press 'ESC' to quit
        break
cap.release()
cv2.destroyAllWindows()
