# ServoMotor-calibration
This repository aims to propose a concrete methodology for calibrating servo motors that do not have an encoder.

## 💻 Materials
In this work, a Futaba s-3003 servo motor was used. This servomotor can be purchased on [Amazon].

We also use a green 3d-printed piece to make easier the segmentation. The STL file can be found in the stl directory of this repository.

Finally, we use Arduino Uno and a low-cost webcam to control and take photos of the servo motor. 

* [Arduino]
* [WebCam] 


## 🔧 Dependencies and Installation 
* Python == 3.7.11
* OpenCV == 4.5.4.58 
* numpy == 1.21.2 
* matplotlib == 3.4.3
* scikit-image == 0.19.2


## 🚀 Code
The functions developed in this work can be found in the utils.py file in the scripts folder. In the same way, simple use of these functions is presented in demo.py

For example, the segment() function was necessary to separate the green 3d-printed piece from the background. The code and figure below show the results of applying a segmentation.
```py
from utils import segment

evaluated_degree = 145
# Open an image from samples directory
image = plt.imread('../samples/' + str(evaluated_degree) + '_degree.jpg')
# Use of the function segment() to get the desired shape
# hue_low = 0.3, hue_high = 0.45, transparency = 0.2
segmented_image = segment(image, [0.3, 0.45, 0.2]) 
```

![alt text](/images/First.png/)


After the segmentation process, it is necessary to perform some contour detection using OpenCV. The code and figure below show the effect of applying two different functions, draw_contour() to detect the contour (filled) and draw_line() to calculate its centroid and draw a line in the middle. 

```py
from utils import draw_contour, draw_line

# Use the function draw_contour() to draw the filled contour the segmented image
image_contour = draw_contour(segmented_image)
# Use the function draw_line() to calculate the centroid and draw a line from its center 
image_contour = draw_line(image_contour, evaluated_degree)
```

![alt text](/images/Second.png/)

Finally, before converting the Cartesian coordinates of the line to polar coordinates, it is necessary to centre the X and Y coordinates. This is performed by using center_line_coordinates(). The output of these functions gives us the new X and Y coordinates. After that, we use cart2polar() to obtain rho and theta and plot() to represent de polar coordinates.  


```py
from utils import center_line_coordinates, cart2polar, plot

# Use the function center_line_coordinates() to center the original coordinates from the line to convert it in polar coordinates 
# 145 indicates the actual degree you are studying
image_contour, x, y = center_line_coordinates(image_contour)

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
```

![alt text](/images/Third.png/)

To average out the error it is necessary to have labelled the photos correctly. So that the webcam will take pictures synchronously with the Arduino one when controlling the servo motor. Thus, to calculate the error with this methodology it is only necessary to subtract the degree information provided by the image label with the average theta calculation.

```py
import numpy as np

mean_theta = np.mean(theta) * 180 / np.pi # degree conversion
error = np.abs(mean_theta - evaluated_degree)
````

## 📜 License
This project is released under the MIT 2.0 license.

## 📧 Contact
If you have any question, please email antoniogalvanhernandez1998@gmail.com.


[Arduino]: https://es.aliexpress.com/item/1005003363526075.html?spm=a2g0o.order_list.0.0.7026194d5T4FYp&gatewayAdapt=glo2esp

[WebCam]: https://es.aliexpress.com/item/1005003265292702.html?spm=a2g0o.productlist.0.0.58841a76OqW3ZT&algo_pvid=08db5076-2ad3-4326-88de-2f07b57a44f2&algo_exp_id=08db5076-2ad3-4326-88de-2f07b57a44f2-27&pdp_ext_f=%7B%22sku_id%22%3A%2212000026444826842%22%7D&pdp_npi=2%40dis%21EUR%21%2110.53%21%21%21%21%21%400b0a01f816534735215556053e6cb1%2112000026444826842%21sea

[Amazon]:https://www.amazon.co.uk/Standard-Torque-Compatible-Helicopter-Airplane/dp/B081N98S6R/ref=sr_1_5?crid=3OAKPZK7MXMOF&keywords=futaba+servo+s-3003&qid=1653311690&sprefix=futaba+servo+%2Caps%2C214&sr=8-5

