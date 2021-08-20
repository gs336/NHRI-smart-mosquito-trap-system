# NHRI-smart-mosquito-trap-system
A smart mosquito trap system which can capture living mosquito and seperate aedes and non-aedes by Neural Networks.

The whole system contains two concept,

(1)Data Collecting: To identify captured mosquito is adeds or not, we using transfer learning using keras squeezenet model, even with transfer learning, training a neural netwroks still needs lots of data, for that we build two mechanism capturing both static and dynamic mosquito images.

(a)For static images, we develope a specimen imaging system which can take images from mosquito specimen under several brightness at different angles along two orientations, makes we can obtain any kind of mosquito images from every possible angle. The specimen imaging system consists of a platform that can be rotated by a stepper motor along the z-axis in which a mosquito specimen can be attached to through an insect pin  which is controlled by an Arduino, and a camera holder that holds the camera and rotates it along the x-axis. On the side of the camera controllable LED’s are placed to create the desired lighting conditions, both Arduino and the camera are both controlled by a MATLAB script, and the whole system is placed in a studio to obtain a white background to ensure the taken images only contain the targeted mosquito.
