# NHRI-smart-mosquito-trap-system
A smart mosquito trap system which can capture living mosquito and seperate aedes and non-aedes by Neural Networks.

The whole system contains three concept,

(1)Data Collecting: To identify captured mosquito is adeds or not, we using transfer learning using keras squeezenet model, even with transfer learning, training a neural netwroks still needs lots of data, for that we build two mechanism capturing both static and live mosquito images.

(i)For static images, we develope a specimen imaging system which can take images from mosquito specimen under several brightness at different angles along two orientations, makes we can obtain any kind of mosquito images from every possible angle. The specimen imaging system consists of a platform that can be rotated by a stepper motor along the z-axis in which a mosquito specimen can be attached to through an insect pin  which is controlled by an Arduino, and a camera holder that holds the camera and rotates it along the x-axis. On the side of the camera controllable LED’s are placed to create the desired lighting conditions, both Arduino and the camera are both controlled by a MATLAB script, and the whole system is placed in a studio to obtain a white background to ensure the taken images only contain the targeted mosquito.
![image](https://user-images.githubusercontent.com/61857351/130176348-57ea9465-64e4-462e-b5d1-7881eecd62f8.png)


(ii)Other than obtaining specimen images for training the neural network we also developed a system to obtain images of live, moving mosquitoes. In this design we set up a small box that and a camera that resembles the capturing area of our mosquito trap. One side of the box is transparent to let the camera to monitor the inside of the box, and the top of the box can be closed by another transparent plate. With this design we would confine the mosquito in the box and use a rotating stick to disturb the whole system by hitting it like a swinging bat at a fixed rate. This disturbance makes the mosquito fly continuously inside the box. The camera then captures a video feed that resembles the data that would be observed when the mosquito trap do encounter a living mosquito that has just flied in the capturing area.

(2)
