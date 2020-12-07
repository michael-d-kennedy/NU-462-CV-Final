# Is my gate open?

## Computer Vision Inference on a Raspberry Pi with Coral Usb Accelerator
### an edge-based computer vision solution


![0_Raspberry_Pi_In_Production.jpg](https://github.com/michael-d-kennedy/NU-462-CV-Final/blob/main/0_Raspberry_Pi_In_Production.jpg?raw=true)

### Problem Definition
Landscapers have been in and out of the back yard frequently over the past few weeks.  On numerous occasions they have left the gate open allowing my dogs to get out.  The purpose of this project is to deploy a computer vision model onto an edge device that can deliver a warning whenever the gate is found to be open.   

### Project Methodology
To accomplish this, I will deploy a TensorFlow Lite model onto a Raspberry Pi with a camera module attached for capturing images and a Coral USB Accelerator for inference.  That device will be fixed pointed at the gate so that it may take a picture once every few minutes, pass it through the model and determine whether the gate is opened or closed and at what certainty.  If determined to be open, the device will send an MMS message with a copy of the image taken. 

### Data Acquisition & Preparation
Data was created by taking 1000 images each of various opened and closed states.  To account for changing environments such as different levels of sunlight, I applied a random adjustment to camera brightness and contrast.  Each photo was taken at a high definition 1944x1994 pixels and then cropped to an image of 224x224 pixels focused on the gate latching mechanism and the area to the right side where the door opens.

### Model Design & Execution
The cropped images were used to train a classification model with transfer learning using the pretrained MobileNet V2 model as a base.  After initial training was complete, 125 of 155 layers were frozen such that the remaining could be retrained and fine-tuned.  Once finished the model was then converted to TensorFlow Lite so that it could then be compiled for the Coral Edge TPU.  

### Deployment
The model and label file were then deployed to the Raspberry Pi so that we can run inference on images taken every few minutes by the Pi camera.  Those images are taken in high def and cropped in the same manner as the training set before running the classification model using the PyCoral API.  An email session is created and if the image is determined to be of an open gate, email to text sends a warning MMS with a copy of the full HD photo and the % certainty the model returns.      

### Results
The trained and fine tunned model produced a validation accuracy of 0.9350.  Validation loss vs training loss shows a bit of overfitting, however, the model produced is better than expected considering the data collection circumstances.  Once deployed the results have been quite good in real time.  As darkness approaches however, the model has a bit of trouble due to lack of night vision on the camera. 

### Future Iterations
The model can certainly be improved by retraining with more and better data.  More efforts can be made to train the model as well using other data augmentation processes, trying other pretrained models, or building from scratch without the use of transfer learning to see if it can improve performance. 

<img src="https://github.com/michael-d-kennedy/NU-462-CV-Final/blob/main/5_Final_Output_MMS_Warning.png?raw=true">
