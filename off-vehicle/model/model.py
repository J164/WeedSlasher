import matplotlib.pyplot as plt
import tensorflow as tf
import time
import os

def prepare_base_model(url, initial_epochs, fine_tune_epochs, dataset_path=None):
  # Find the training and validation datasets
  path_to_zip = tf.keras.utils.get_file('base_dataset.zip', origin=url, extract=True)
  PATH = os.path.join(os.path.dirname(path_to_zip), 'base_dataset')

  train_dir = os.path.join(PATH, 'train')
  validation_dir = os.path.join(PATH, 'validate')
  test_dir = os.path.join(PATH, 'test')

  BATCH_SIZE = 32
  IMG_SIZE = (256, 256)

  train_dataset = tf.keras.utils.image_dataset_from_directory(train_dir, shuffle=True, batch_size=BATCH_SIZE, image_size=IMG_SIZE)
  validation_dataset = tf.keras.utils.image_dataset_from_directory(validation_dir, shuffle=True, batch_size=BATCH_SIZE, image_size=IMG_SIZE)
  test_dataset = tf.keras.utils.image_dataset_from_directory(test_dir, shuffle=True, batch_size=BATCH_SIZE, image_size=IMG_SIZE)

  # Prefetch datasets
  AUTOTUNE = tf.data.AUTOTUNE

  train_dataset = train_dataset.prefetch(buffer_size=AUTOTUNE)
  validation_dataset = validation_dataset.prefetch(buffer_size=AUTOTUNE)
  test_dataset = test_dataset.prefetch(buffer_size=AUTOTUNE)

  # Augment data
  data_augmentation = tf.keras.Sequential([
    tf.keras.layers.RandomFlip('horizontal'),
    tf.keras.layers.RandomFlip('vertical'),
    tf.keras.layers.RandomRotation(0.2)
  ])

  # Preproccess data
  preprocess_input = tf.keras.applications.mobilenet_v2.preprocess_input

  # Create base model
  IMG_SHAPE = IMG_SIZE + (3,)
  base_model = tf.keras.applications.MobileNetV2(input_shape=IMG_SHAPE, include_top=False, weights='imagenet')
  base_model.trainable = False

  # Classification head
  global_average_layer = tf.keras.layers.GlobalAveragePooling2D()
  prediction_layer = tf.keras.layers.Dense(1)

  # Build our custom model
  prediction_layer = tf.keras.layers.Dense(1)
  inputs = tf.keras.Input(shape=(256, 256, 3))
  x = data_augmentation(inputs)
  x = preprocess_input(x)
  x = base_model(x, training=False)
  x = global_average_layer(x)
  x = tf.keras.layers.Dropout(0.2)(x)
  outputs = prediction_layer(x)
  model = tf.keras.Model(inputs, outputs)

  # Compile the model
  base_learning_rate = 0.0001
  model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=base_learning_rate), loss=tf.keras.losses.BinaryCrossentropy(from_logits=True), metrics=[tf.keras.metrics.BinaryAccuracy(threshold=0, name='accuracy')])

  # Collect initial accuracy data
  init_loss, init_accuracy = model.evaluate(validation_dataset)

  # Top layer training
  begin_time = time.time()

  history = model.fit(train_dataset, epochs=initial_epochs, validation_data=validation_dataset)

  # Log accuracy data
  acc = history.history['accuracy']
  val_acc = history.history['val_accuracy']

  loss = history.history['loss']
  val_loss = history.history['val_loss']

  mid_loss, mid_accuracy = model.evaluate(test_dataset)

  # Fine tune model

  # Fetch supplemental data
  additional_dataset = tf.keras.utils.image_dataset_from_directory(dataset_path, shuffle=True, batch_size=1, image_size=IMG_SIZE)
  train, validate = tf.keras.utils.split_dataset(additional_dataset, left_size=0.6)
  test, validate = tf.keras.utils.split_dataset(additional_dataset, left_size=0.5)

  train_dataset = train_dataset.concatenate(train)
  validation_dataset = validation_dataset.concatenate(validate)
  test_dataset = test_dataset.concatenate(test)

  # Prefetch datasets
  train_dataset = train_dataset.prefetch(buffer_size=AUTOTUNE)
  validation_dataset = validation_dataset.prefetch(buffer_size=AUTOTUNE)
  test_dataset = test_dataset.prefetch(buffer_size=AUTOTUNE)

  base_model.trainable = True

  fine_tune_at = 100
  for layer in base_model.layers[:fine_tune_at]:
    layer.trainable = False

  model.compile(loss=tf.keras.losses.BinaryCrossentropy(from_logits=True), optimizer=tf.keras.optimizers.RMSprop(learning_rate=base_learning_rate/10),metrics=[tf.keras.metrics.BinaryAccuracy(threshold=0, name='accuracy')])

  history_fine = model.fit(train_dataset, epochs=initial_epochs + fine_tune_epochs, initial_epoch=history.epoch[-1], validation_data=validation_dataset)

  end_time = time.time()

  acc += history_fine.history['accuracy']
  val_acc += history_fine.history['val_accuracy']

  loss += history_fine.history['loss']
  val_loss += history_fine.history['val_loss']

  end_loss, end_accuracy = model.evaluate(test_dataset)

  # Save model to build directory
  model.save('off-vehicle/build/model.keras')
  model.save('off-vehicle/build/model/', save_format='tf')
  
  # Print metrics
  print(f"Model took {(end_time - begin_time):.2f}s to train")
  
  print("initial loss: {:.2f}".format(init_loss))
  print("initial accuracy: {:.2f}".format(init_accuracy))

  print("mid loss: {:.2f}".format(mid_loss))
  print("mid accuracy: {:.2f}".format(mid_accuracy))

  print("end loss: {:.2f}".format(end_loss))
  print("end accuracy: {:.2f}".format(end_accuracy))

  plt.figure(figsize=(16, 16))
  plt.subplot(2, 2, 1)
  plt.plot(acc, label='Training Accuracy')
  plt.plot(val_acc, label='Validation Accuracy')
  plt.ylim([0, 1.0])
  plt.plot([initial_epochs, initial_epochs],
            plt.ylim(), label='Start Fine Tuning')
  plt.legend(loc='lower right')
  plt.title('Training and Validation Accuracy')

  plt.subplot(2, 2, 3)
  plt.plot(loss, label='Training Loss')
  plt.plot(val_loss, label='Validation Loss')
  plt.ylim([0, 1.0])
  plt.plot([initial_epochs, initial_epochs],
          plt.ylim(), label='Start Fine Tuning')
  plt.legend(loc='upper right')
  plt.title('Training and Validation Loss')
  plt.xlabel('epoch')

  plt.subplot(2, 2, 2)
  plt.bar(['initial', 'after general training', 'after fine tuning'], [init_accuracy, mid_accuracy, end_accuracy])
  plt.ylim([0, 1.0])
  plt.title('Testing Accuracy')
  plt.xlabel('training stage')

  plt.subplot(2, 2, 4)
  plt.bar(['initial', 'after general training', 'after fine tuning'], [init_loss, mid_loss, end_loss])
  plt.ylim([0, 1.0])
  plt.title('Testing Loss')
  plt.xlabel('training stage')

  plt.show()

url = 'https://www.dropbox.com/scl/fi/etvihp98kjka3sqwnygg4/base_dataset.zip?rlkey=gx5e2q464a29jk5s7tpy2o1o7&dl=1'
path = 'off-vehicle/build/regions/0'
prepare_base_model(url, 10, 10, dataset_path=path)