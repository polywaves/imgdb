import cv2

# reading image 
image = cv2.imread('in/2024-12-12 11.40.49.jpg')

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
# blur = cv2.GaussianBlur(gray, (13, 13), 0)
thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9,5))
dilate = cv2.dilate(thresh, horizontal_kernel, iterations=2)
vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,9))
dilate = cv2.dilate(dilate, vertical_kernel, iterations=2)

# Find contours, filter using contour threshold area, and draw rectangle
cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    area = cv2.contourArea(c)
    if area > 20000:
        x,y,w,h = cv2.boundingRect(c)
        cv2.rectangle(image, (x, y), (x + w, y + h), (36, 255, 12), 3)

# cv2.imshow('thresh', thresh)
# cv2.imshow('dilate', dilate)
cv2.imshow('image', image)
cv2.waitKey()
