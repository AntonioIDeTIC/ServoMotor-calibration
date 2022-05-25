import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
from skimage.color import rgb2hsv


"""
   Matplotib function that allows passing graphs with 'enter' and exit with 'esc'.
   :param event: the keypress event
   :return: None
"""
def press(event):
    if event.key == 'enter':
        plt.close()
    if event.key == 'escape':
        exit()


"""
   Segment the green 3d-printed piece.
   :param image: the original RGB image
   :param treshold: the HSV treshold
   :return: RGB image masked
"""
def segment(image, treshold):
    hsv = rgb2hsv(image)  # Convert RGB to HSV

    # Define the general thresholds (hue channel and transparency channel)
    lower_mask = hsv[:, :, 0] > treshold[0]
    upper_mask = hsv[:, :, 0] < treshold[1]
    saturation_mask = hsv[:, :, 1] > treshold[2]

    # Apply the thresholds with a mask
    mask = upper_mask * lower_mask * saturation_mask
    red = image[:, :, 0] * mask
    green = image[:, :, 1] * mask
    blue = image[:, :, 2] * mask
    image_masked = np.dstack((red, green, blue))

    return image_masked

"""
   Binarize the segmented image and draw the contour.
   :param image_masked: the RGB image masked
   :return: image contour filled
"""
# Function that 
def draw_contour(image_masked):
    # Binarize the image with OpenCV
    gray_image = cv.cvtColor(image_masked, cv.COLOR_RGB2GRAY)
    _, im_bw = cv.threshold(gray_image, 30, 255, cv.THRESH_BINARY)
    binarized_image = np.asarray(im_bw, dtype=np.uint8)

    # Calculate the contours of the image and Fill the contour
    contours, _ = cv.findContours(binarized_image, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    # Copy the original image
    image_copy = image_masked.copy()
    # Create black canvas with the original image dimensions and draw a filled contour
    canvas = np.zeros_like(image_copy)
    image_contour = cv.drawContours(image=canvas, contours=contours, contourIdx=-1, color=(0, 255, 0),
                                    thickness=cv.FILLED,
                                    lineType=cv.LINE_AA)

    return image_contour


"""
   Calculate the centroid and draw a line in the middel of the image contour.
   :param image_contour: image contour filled
   :param evaluated_degree: current degree evaluated
   :return: image contour after drawing the line
"""
def draw_line(image_contour, evaluated_degree):
    # Calculate the centroid and make a line
    M = cv.moments(image_contour[:, :, 1])
    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
    theta = 0.5 * np.arctan2(2 * M["mu11"], M["mu20"] - M["mu02"])

    if evaluated_degree <= 90:
        endx = int(800 * np.cos(theta) + center[0])  # linelength 800
        endy = int(800 * np.sin(theta) + center[1])
    else:
        endx = int(-800 * np.cos(theta) + center[0])  # linelength 800
        endy = int(-800 * np.sin(theta) + center[1])

    # Draw a line from centroid to endx and endy
    image_contour = cv.line(image_contour, (center[0], center[1]), (endx, endy), (255, 255, 255), 1)
    
    return image_contour
    
"""
   Center the X and Y line coordinates to convert in Polar coordinates.
   :param image_contour: image contour after drawing the line
   :return: image contour after the center process, new x coordinates of the draw line, new y coordinates of the draw line
"""
def center_line_coordinates(image_contour):
    # Calculate the non zero values of the line (without the contour)
    image_contour_green = image_contour[:, :, 2]
    indices = np.where(image_contour_green != [0])
    x, y = indices[1], indices[0]

    # Loop to center the coordinates to later transformation into Polar coordinates
    new_x = []
    new_y = []
    x_value = x[0]
    y_value = y[0]
    for x_, y_ in zip(x, y):
        x_temp = np.abs(x_ - x_value)
        y_temp = np.abs(y_ - y_value)
        new_x.append(x_temp)
        new_y.append(y_temp)

    new_x = np.asarray(new_x)
    new_y = np.asarray(new_y)

    # Draw a center line from centroid to endx and endy
    #image_contour = cv.line(image_contour, (new_x[0], new_y[::-1][0]), (new_x[-1], new_y[::-1][-1]), (255, 0, 255), 1)

    return image_contour, new_x, new_y


"""
   Transform the cartesian values to polar values.
   :param x: x coordinates of the draw line
   :param y: y coordinates of the draw line
   :return: rho values and theta values after the conversion
"""
def cart2polar(x, y):
    rho = np.sqrt(x ** 2 + y ** 2)
    theta = np.arctan2(y, x)
    return rho, theta


# Function that 
"""
   Plot the polar data.  
   :param image_contour: image contour after the center process
   :param rho: rho values
   :param theta: theta values
   :return: None
"""
def plot(image_contour, rho, theta):
    fig = plt.figure()
    fig.add_subplot(121)
    plt.imshow(image_contour)
    plt.title('Segmented image')
    ax = plt.subplot(1, 2, 2, projection='polar')
    plt.plot(theta, rho)
    plt.title('Polar representation')
    plt.axis('off')

    plt.show()
