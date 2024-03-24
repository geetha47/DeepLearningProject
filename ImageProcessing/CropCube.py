import cv2
import os
import numpy as np


# Callback function for trackbar changes
def nothing(x):
    pass


image = cv2.imread('Images/image.jpg')
#img = cv2.resize(image, (960, 540))
img=image
img_copy = image.copy()

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

threshold1 = 59
threshold2 = 24

cv2.namedWindow('Trackbars')

# Create trackbars for threshold1 and threshold2
cv2.createTrackbar('Threshold1', 'Trackbars', threshold1, 255, nothing)
cv2.createTrackbar('Threshold2', 'Trackbars', threshold2, 255, nothing)

while True:
    # Get current positions of trackbars
    threshold1 = cv2.getTrackbarPos('Threshold1', 'Trackbars')
    threshold2 = cv2.getTrackbarPos('Threshold2', 'Trackbars')
    n=0
    # Apply Canny edge detection with the updated threshold values
    edged = cv2.Canny(gray, threshold1, threshold2)
    dilated = cv2.dilate(edged, None, iterations=1)

    contours, _ = cv2.findContours(dilated, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    margin = 10  # Adjust this value as needed
    output_dir = 'cubes'
    os.makedirs(output_dir, exist_ok=True)

    img_copy = img.copy()
    for i, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)

        if w > 30 and h > 20:
            n=n+1
            x_relaxed = max(0, x - margin)
            y_relaxed = max(0, y - margin)
            w_relaxed = min(img.shape[1] - x_relaxed, w + 2 * margin)
            h_relaxed = min(img.shape[0] - y_relaxed, h + 2 * margin)
            print(f'{n}:{x},{y},{w},{h}')
            cv2.rectangle(img_copy, (x_relaxed, y_relaxed), (x_relaxed + w_relaxed, y_relaxed + h_relaxed),
                          (0, 255, 0), 2)
            cv2.putText(img_copy, f"Contour {i + 1}: (x={x}, y={y}, w={w}, h={h})", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            cube = image[y_relaxed:y_relaxed + h_relaxed, x_relaxed:x_relaxed + w_relaxed]
            cv2.imwrite(os.path.join(output_dir, f'cube{n}_{i+ 1}.png'), cube)

    #combined_image = cv2.resize(img_copy, (960, 540))
    cv2.imshow("Contours", img_copy)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cv2.destroyAllWindows()
