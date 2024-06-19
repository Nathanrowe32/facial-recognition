import cv2

img = cv2.imread('../input/image.png')

cv2.imshow('Image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

print("OpenCV is working")