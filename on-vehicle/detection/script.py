import cv2
import numpy as np
import tensorflow as tf

cam = cv2.VideoCapture(0)

def classify(model_path):
  model = tf.saved_model.load(model_path)
  _, image = cam.read()
  image = cv2.resize(image,dsize=(256,256),interpolation=cv2.INTER_CUBIC)
  image_data = np.asarray(image)
  image_data = np.expand_dims(image_data, axis=0)
  return (model.serve(image_data)[0,0] < 0.5).numpy()