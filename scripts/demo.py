import matplotlib.pyplot as plt
import numpy as np
from utils import segment, draw_contour, draw_line, center_line_coordinates, cart2polar, plot

import matplotlib

# Select your font
font = {'family' : 'Times New Roman',
        'size'   : 22}
matplotlib.rc('font', **font)

# Open an image from samples directory
evaluated_degree = 145
image = plt.imread('../samples/' + str(evaluated_degree) + '_degree.jpg')

fig = plt.figure()
fig.add_subplot(121)
plt.imshow(image)
plt.title('Original image')
plt.axis('off')

# Use of the function segment() to get the desired shape
segmented_image = segment(image, [0.3, 0.45, 0.2]) # hue_low = 0.3, hue_high = 0.45, transparency = 0.2

fig.add_subplot(122)
plt.imshow(segmented_image)
plt.title('Segmented image')
plt.axis('off')
plt.show()

# Use the function draw_contour() to draw the filled contour the segmented image
image_contour = draw_contour(segmented_image)

fig.add_subplot(223)
plt.imshow(image_contour)
plt.title('Image contour (filled)')
plt.axis('off')
# Use the function draw_line() to calculate the centroid and draw a line from its center 
image_contour = draw_line(image_contour, evaluated_degree)

# Use the function center_line_coordinates() to center the original coordinates from the line to convert it in polar coordinates 
# 145 indicates the actual degree you are studying

image_contour, x, y = center_line_coordinates(image_contour)

fig.add_subplot(224)
plt.imshow(image_contour)
plt.title('Image contour with the draw line')
plt.axis('off')
plt.show()

# Use the function cart2polar() to convert cartesian coordinates to polar coordinates
rho, theta = cart2polar(x, y)

# Some transformation necessary to the correct representation
if evaluated_degree <= 90:
    theta = theta
elif evaluated_degree > 90 and evaluated_degree <= 180:
    theta = np.pi - theta
else:
    pass

# Use the function plot() to show the contour of the image and the polar transformation
plot(image_contour, rho, theta)