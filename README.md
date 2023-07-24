# Furniture_yolo_vision
The project is an experiment.
Creating a synthetic data set using 3D object and Unity to train Yolov5 to recognise objects on video.

Using free assets for the Unity and a C# script (3D_img_generator_v3.cs), 
the desired number of 3d images of various furniture on a gray background is generated. 
A sample of the resulting images is in the folder (3D_img_expl)
Scale and position parameters can be adjusted.

The Python program (Data_set_generator.py) overlays object images on a set of random backgrounds.
Label files creat for each result image.
Based on the original name, the program arranges images and labels into folders.
Then creates .yaml file that is needed to start training with yolov5.

Test video created in the Unity can be viewed at the link:
https://youtu.be/yTYo0UyHuVY

And the finished result:
https://youtu.be/XPY2i-l7CJ8