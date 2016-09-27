# attention-score-calculator (school project)
component of a larger project. Analyzes incoming images (webcam point of view) of students in a classroom every 15 seconds to determine to what extent the students are paying attention during a specific class. 

This project is meant to enable teachers to improve the quality of their lessons. 
    - the teacher starts a "session" when his/her class starts on the heads up web app
    - the raspberry pi client starts recording the teacher (and only the teacher!) through an usb webcam, this recording is stored in a file storage
    - the clients installed on students' laptops are triggered, they upload an image every 15 seconds to the attention score calculator (this component)
    - these images are processed every 15 seconds, resulting in an average attention score per class (ie. the percentage of the class that is paying attention)
    - this score is made visible to the teacher through LED lights during the lesson. The hue of the lights corresponds to the score (eg. red == low, green == high)
    - the teacher can view reports of his classes in the web app. He/she can see a graph of the attention scores during a class alongside an embedded video player that shows the recording of the corresponding lesson, allowing the teacher to see the effect of his/her teaching style on the attention of his/her class

This module uses OpenFace (https://cmusatyalab.github.io/openface/) to determine the head poses of students relative to the camera.
These poses are interpreted through machine learning (1), resulting in a preliminary attention score. 
The preliminary attention score is adjusted in scale to the average observed attention score during data collection(2). 
All images of students are deleted after head pose extraction.




*(1) I used WEKA to train an SVM (SMO) based on a dataset of 94 images, 47 labeled as "paying_attention" and 47 labeled as "not_paying"attention". 
Labeling was done manually, 94 images remained after manual cleaning and balancing. This dataset is too small to produce reliable results, but had to suffice due to time constraints.
The choice of SMO was due to ease of implementation (time constraints); iBk, j48 and random forests performed better in accuracy and precision.*

*(2) The average attention score from all collected data (125 images) is 37.6%. This means nothing, as this dataset is far too small!*
