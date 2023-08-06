==========================================
Tensorflow gRPC and RESTful API Server
==========================================

Introduce
==============

**tfserver** is an example for serving Tensorflow model with `Skitai App Engine`_.

It can be accessed by gRPC and JSON RESTful API.

This project is inspired by `issue #176`_.

From version 0.3, it is now TensorFlow 2+ compatible.


.. _`issue #176` : https://github.com/tensorflow/serving/issues/176
.. _`Skitai App Engine`: https://pypi.python.org/pypi/skitai
.. _dnn: https://pypi.python.org/pypi/dnn


.. contents:: Table of Contents


Saving Tensorflow Model
===================================

.. code:: python

  # MUST import top of the code for disabling eager execution
  from tfserver import saved_model
  import tensorflow as tf
  import numpy as np

  x = tf.keras.layers.Input (3)
  h = tf.keras.layers.Dense (10, activation='relu') (x)
  y = tf.keras.layers.Dense (2, activation='softmax') (h)

  model = tf.keras.Model (x, y)
  model.compile (
      optimizer=tf.keras.optimizers.Adam(0.001),
      loss = 'categorical_crossentropy',
      metrics = ['accuracy']
  )
  model.summary()

  train_xs = np.array ([
      (0.1, 0.2, 0.6),
      (0.3, 0.6, 0.7),
      (0.2, 0.9, 0.3),
      (0.3, 0.9, 0.1),
  ])

  train_ys = np.array ([
      (1.0, 0),
      (0, 1.0),
      (1.0, 0),
      (0, 1.0),
  ])

  model.fit(train_xs, train_ys, epochs=3, batch_size=32)
  model.evaluate(train_xs, train_ys)
  model.predict(train_xs)

  inputs, outputs = saved_model.save (
    './mymodel/123',
    {'x': model.inputs [0]},
    {'y': model.outputs [0]},
    classes = ['true', 'false'])
  )

**Saved Model**

- Inputs

  - x: placeholders/Placeholder:0

- Outputs

  - y: dnn/dense_3/BiasAdd:0
  - scores: TopKV2:0
  - classes: hash_table_Lookup/LookupTableFindV2:0


Running Server
===================================

You just setup model path and tensorflow configuration, then you can have gRPC and JSON API services.

Example of tfserve.py

.. code:: python

  # tfserve.py

  import tfserver
  import skitai

  tfserver.add_model ("model1", "exported/model1/200", gpu_usage = 0.1)
  tfserver.add_model ("model1", "exported/model2/100", 0.2)

  with skitai.pref () as pref:
    # If you want to activate gRPC, should mount on '/'
    skitai.mount ("/", tfserver, pref = pref)
    skitai.run (port = 5000, name = "tfserver")

And run,

.. code:: bash

  python3 tfserve.py

Using grpcio library,

.. code:: python

  from tfserver import cli
  from tensorflow.python.framework import tensor_util
  import numpy as np

  stub = cli.Server ("http://localhost:5000")
  problem = np.array ([1.0, 2.0])

  resp = stub.predict (
    'model1', #alias for model
    x = tensor_util.make_tensor_proto(problem.astype('float32'), shape=problem.shape)
  )
  # then get 'y'
  resp.y
  >> np.ndarray ([-1.5, 1.6])


Adding Custom APIs
===========================

You can create your own APIs.

For example,

.. code:: python

  # services/apis.py

  import tfserver

  def __mount__ (app):
      import os
      from .helpers.unspsc import datautil

      @app.route ("/models/unspsc/classify", methods = ["POST"])
      def unspsc (was, text):
          x, seq_length = datautil.encode (text)
          result = tfserver.predict ("unspsc", x = [x], seq_length = [seq_length])
          return was.API (
            classes = result ['classes'].aslist (),
            scores = result ['scores'].aslist ()
          )

      @app.route ("/models/facial_expression/classify", methods = ["POST"])
      def facial_expression (was, face, name):
          with face.flashfile () as path:
            x = cv2.resize (cv2.imread (path, cv2.IMREAD_GRAYSCALE), (48, 48)).reshape (48, 48, 1)
            result = tfserver.predict ("facial_expression", x = [x])
            return was.API (
              classes = result ['classes'].aslist (),
              scores = result ['scores'].aslist ()
            )

Then mount these service and run.

.. code:: python

  # tfserve.py
  import tfserver
  import skitai
  from services import apis # import your custom services

  tfserver.add_model ("model1", "exported/model1/200", gpu_usage = 0.1)
  tfserver.add_model ("model1", "exported/model2/100", 0.2)

  with skitai.preference () as pref:
      pref.mount ("/", apis) # mount your custom services
	    skitai.mount ("/", tfserver, pref = pref)
	skitai.run (port = 5000, name = "tfserver")

Request,

.. code:: python

  import requests

  resp = requests.post (
    "http://localhost:5000/models/unspsc/classify",
    json.dumps ({'text': 'Loem ipsum...'}),
    headers = {"Content-Type": "application/json"}
  )
  data = resp.json ()

  resp = requests.post (
    "http://localhost:5000/models/facial_expression/classify",
    data = {'name': 'Hans Roh'},
    files = {'face': open ('my-face.jpg', 'rb')}
  )
  data = resp.json ()


Model Management APIs
=============================

- getting information about models that served by tfserver
- upload new saved model top tfserver with version number
- remove version(s) of a model from tfserver
- remove a model from tfserver

Please see test_tfserver_.

.. _test_tfserver: https://gitlab.com/hansroh/skitai/-/blob/master/tests/level5/test_tfserver.py


Performance Note After Comparing with Proto Buffer and JSON
======================================================================

Test Environment
-------------------------------

- Input:

  - dtype: Float 32
  - shape: Various, From (50, 1025) To (300, 1025), Prox. Average (100, 1025)

- Output:

  - dtype: Float 32
  - shape: (60,)

- Request Threads: 16
- Requests Per Thread: 100
- Total Requests: 1,600

Results
--------------------

Average of 3 runs,

- gRPC with Proto Buffer:

  - Use grpcio
  - 11.58 seconds

- RESTful API with JSON

  - Use requests
  - 216.66 seconds

Proto Buffer is 20 times faster than JSON...


Release History
=============================

- 0.3 (2020. 6. 28)

  - add model management APIs
  - reactivate project and compatible with TF2+

- 0.2 (2020. 6. 26): integrated with dnn 0.3

- 0.1b8 (2018. 4. 13): fix grpc trailers, skitai upgrade is required

- 0.1b6 (2018. 3. 19): found works only grpcio 1.4.0

- 0.1b3 (2018. 2. 4): add @app.umounted decorator for clearing resource

- 0.1b2: remove self.tfsess.run (tf.global_variables_initializer())

- 0.1b1 (2018. 1. 28): Beta release

- 0.1a (2018. 1. 4): Alpha release



