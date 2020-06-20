import keras
import time
from keras import layers
from keras import models
from keras.datasets import mnist
from keras.utils import to_categorical
from datadog import initialize, statsd
from ddtrace import tracer
import logging

options = {
    'statsd_socket_path': '/var/run/datadog/dsd.socket'
}

initialize(**options)

FORMAT = ('%(asctime)s %(levelname)s [%(filename)s:%(lineno)d] '
          '- %(message)s')

logging.basicConfig(filename='/opt/services/keras/models/logs/training.log', filemode='w', format=FORMAT)
log = logging.getLogger(__name__)
log.level = logging.INFO

class LogsAndMetricsCallback(keras.callbacks.Callback):
    def on_epoch_end(self, epoch, accuracy, logs=None):
        statsd.gauge('keras.epoch', (epoch+1))
        statsd.gauge('keras.accuracy', accuracy['accuracy'])
        statsd.gauge('keras.loss', accuracy['loss'])
        log.info('MNIST Convolutional Neural Network Training - Epoch: {}, Accuracy: {}, Loss: {}.'.format((epoch+1), accuracy['accuracy'], accuracy['loss']))

while(True):

    with tracer.trace('model.add_layers'):
        model = models.Sequential()
        model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)))
        model.add(layers.MaxPooling2D((2, 2)))
        model.add(layers.Conv2D(64, (3, 3), activation='relu'))
        model.add(layers.MaxPooling2D((2, 2)))
        model.add(layers.Conv2D(64, (3, 3), activation='relu'))

        model.add(layers.Flatten())
        model.add(layers.Dense(64, activation='relu'))
        model.add(layers.Dense(10, activation='softmax'))

    with tracer.trace('mnist.load_data'):
        (train_images, train_labels), (test_images, test_labels) = mnist.load_data()

    with tracer.trace('model.reshape_images'):
        train_images = train_images.reshape((60000, 28, 28, 1))
        train_images = train_images.astype('float32') / 255

        test_images = test_images.reshape((10000, 28, 28, 1))
        test_images = test_images.astype('float32') / 255

    train_labels = to_categorical(train_labels)
    test_labels = to_categorical(test_labels)

    with tracer.trace('model.compile'):
        model.compile(optimizer='rmsprop',
                    loss='categorical_crossentropy',
                    metrics=['accuracy'])

    epochs_train = 5
    batch_size_train = 64

    statsd.event('Convolutional Netual Network Model Training Starting', 'Training starting with Batch Size {} for {} Epochs.'.format(epochs_train, batch_size_train), alert_type='info')

    with tracer.trace('model.fit'):
        model.fit(train_images, train_labels, epochs=epochs_train, batch_size=batch_size_train, callbacks=[LogsAndMetricsCallback()])

    with tracer.trace('model.evaluate'):
        test_loss, test_acc = model.evaluate(test_images, test_labels)

    statsd.event('Convolutional Netual Network Model Training Finished', 'Training finished with Accuracy {} and Loss {}.'.format(test_acc, test_loss), alert_type='success')

    print(test_acc)

    statsd.gauge('keras.epoch', 0)
    statsd.gauge('keras.accuracy', 0)
    statsd.gauge('keras.loss', 0)
    time.sleep(500)