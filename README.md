# NHRI-smart-mosquito-trap-system
A smart mosquito trap system which can capture living mosquito and seperate aedes and non-aedes by Neural Networks.

The whole system contains two concept,

(1)Data Collecting: To identify captured mosquito is adeds or not, we using transfer learning using keras squeezenet model, even with transfer learning, training a neural netwroks still needs lots of data, for that we build two mechanism capturing both static and dynamic mosquito images. For static images, we develope a specimen imaging system which can take images from mosquito specimen under several brightness at different angles along two orientations, makes we can obtain any kind of mosquito images from every possible angle. In specimen imaging system, the specimen is placed on an insect pin on the plate which can be rotated by a step motor controled by arduino uno, 
