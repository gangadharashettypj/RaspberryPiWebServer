import cv2

# Cascade classifier takes the model as input and which can be used to predict the faces with the give image
# haarcascade_frontalface_default.xml is the model trained with the following steps
# 1. Getting face dataset
# 2. resize the iamge to 100 * 100
# 3. Label the image using image laballing software which generates the xml for each image with the given labels
# 4. split the data set into train and test data set ( 80 - 20 )
# 5. Train the model with the training image dataset and generate haarcascade model for faces detection
# 6. Test the model with the test data and compute model accuracy
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
cap.set(3, 640)  # set Width
cap.set(4, 480)  # set Height
while True:
    ret, img = cap.read()
    img = cv2.flip(img, 1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # get the faces in the given white & black image. It will give list of rectangular coordinates
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(20, 20)
    )

    # Parse each coordinates and add a rectangle indicator on top of the image
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]

    # update the image with rectangle
    cv2.imshow('video', img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:  # press 'ESC' to quit
        break
cap.release()
cv2.destroyAllWindows()
