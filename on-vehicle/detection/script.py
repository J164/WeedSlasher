import cv2
import numpy as np
import tensorflow as tf
import time

cam = cv2.VideoCapture(0)
model = tf.saved_model.load("build/model")

def classify(model_path):
  time.sleep(2)
  _, image = cam.read()
  height, width = image.shape[:2]
  new_height = height - (height // 3)
  left_crop = (width - new_height) // 2
  cv2.imwrite('before.jpg', image)
  image = image[0:new_height, left_crop:left_crop+new_height]
  cv2.imwrite('during.jpg', image)
  image = cv2.resize(image,dsize=(256,256),interpolation=cv2.INTER_CUBIC)
  cv2.imwrite('after.jpg', image)
  image_data = np.asarray(image)
  image_data = np.expand_dims(image_data, axis=0)
  return (model.serve(image_data)[0,0] < 0.5).numpy()