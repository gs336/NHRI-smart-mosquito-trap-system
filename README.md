# NHRI-smart-mosquito-trap-system
A smart mosquito trap system that utilizes computer vision technology and deep learning networks to identify features of live adult Aedes aegypti and Cx. quinquefasciatus and identify them in real time.

The whole system contains two concept,

(1)Mosquito Data Collecting and Model Training: To identify captured mosquito is adeds or not with fast speed on Raspberry Pi, we using transfer learning using keras squeezenet model, even with transfer learning, training a neural netwroks still needs lots of data, for that we build two mechanism capturing both specimen(i) and dynamic(ii) mosquito images.

(i)For specimen images, we develope a specimen imaging system which can take images from mosquito specimen under several brightness at different angles along two orientations, makes we can obtain any kind of mosquito images from every possible angle. The specimen imaging system consists of a platform that can be rotated by a stepper motor along the z-axis in which a mosquito specimen can be attached to through an insect pin  which is controlled by an Arduino, and a camera holder that holds the camera and rotates it along the x-axis. On the side of the camera controllable LED’s are placed to create the desired lighting conditions, both Arduino and the camera are both controlled by a MATLAB script, and the whole system is placed in a studio to obtain a white background to ensure the taken images only contain the targeted mosquito.

![image](https://user-images.githubusercontent.com/61857351/130550321-3b7be44c-a914-455a-969d-e663b456bc5a.png)


(ii)Other than obtaining specimen images for training the neural network we also developed a system to obtain dynamic images, moving mosquitoes. In this design we set up a small box that and a camera that resembles the capturing area of our mosquito trap. One side of the box is transparent to let the camera to monitor the inside of the box, and the top of the box can be closed by another transparent plate. With this design we would confine the mosquito in the box and use a rotating stick to disturb the whole system by hitting it like a swinging bat at a fixed rate. This disturbance makes the mosquito fly continuously inside the box. The camera then captures a video feed that resembles the data that would be observed when the mosquito trap do encounter a living mosquito that has just flied in the capturing area.

![image](https://user-images.githubusercontent.com/61857351/130550374-208689f4-1aac-4e7c-9924-c6e847d70057.png)


After collecting mosquito data as above, use keras API to train a custom squeezenet model to identify captured mosquito is Aedes or Culex.


(2)Identify & Seperate Mosquitos in Mosquito Trap: After we training squeezenet properly, we then deploy the model in the Raspberry Pi in the mosquito trap, witch is designed with two chambers, one of which stores mosquitoes that are determined to be Aedes Aegypti or Aedes Albopictus, the other stores mosquitoes that are determined to be Culex. Above these two chambers, a circular capturing plate is paired with a camera that captures entering mosquitoes to the bottom two chambers. The core of the mosquito trap is placed in a black container that can be filled with mosquito attractant to lure the mosquito in the capturing plate for recognition and capture of the mosquito (Figure 3). The mosquito trap is also equipped with a MG811 carbon dioxide sensor module for CO2 concentration, and a DHT22(also known as AM2302) for humidity and temperature.A Raspberry Pi micro controller controls all electrical components. Once a mosquito enters the entry box and its type determined with the image recognition software described below, the mosquito is then captured into the respective chamber according to its type. 

![image](https://user-images.githubusercontent.com/61857351/130189133-9bffd872-fec0-4f56-aa1d-f00293999b3b.png)

![image](https://user-images.githubusercontent.com/61857351/130550409-4157db4f-9a7f-4083-9593-62cb0d555aec.png)
