Notification
=====================

This project is depreacted.

Tensorflow2 and Keras have enough APIs.

- 0.5 (2020.6.29)

  - project has been deprecated

- 0.4 (2020.6.24)

  - integrate tfserver into dnn.tfserver
  - data processing utils were moved to rs4.mldp

- 0.3:

  - remove trainale ()
  - add set_learning_rate ()
  - add argument to set_train_dir () for saving chcekpoit
  - make compatible with tf 1.12.0

- 0.2

  - add tensorflow lite conversion and interpreting

- 0.1: project initialized


tfserver History
=============================

- 0.3 (2020.6.24) integrated to dnn
- 0.2 (2018. 12.1): integrated with dnn 0.3
- 0.1b8 (2018. 4.13): fix grpc trailers, skitai upgrade is required
- 0.1b6 (2018. 3.19): found works only grpcio 1.4.0
- 0.1b3 (2018. 2. 4): add @app.umounted decorator for clearing resource
- 0.1b2: remove self.tfsess.run (tf.global_variables_initializer())
- 0.1b1 (2018. 1. 28): Beta release
- 0.1a (2018. 1. 4): Alpha release



