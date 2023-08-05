==========================================
Tensorflow gRPC and RESTful API Server
==========================================


Notice
===============

This project had been integrate into dnn_. No more updates.


Introduce
==============


**tfserver** is an example for serving Tensorflow model with `Skitai App Engine`_.

It can be accessed by gRPC and JSON RESTful API.

This project is inspired by `issue #176`_.

.. _`issue #176` : https://github.com/tensorflow/serving/issues/176
.. _`Skitai App Engine`: https://pypi.python.org/pypi/skitai
.. _dnn: https://pypi.python.org/pypi/dnn


.. contents:: Table of Contents

Saving Tensorflow Model
===================================

See `tf.saved_model.builder.SavedModelBuilder`_, but for example:

.. code:: python

  from dnn import tf

  # your own neural network
  class DNN:
    ...

  net = DNN (phase_train=False)

  sess = tf.Session()
  sess.run (tf.global_variables_initializer())

  # restoring checkpoint
  saver = tf.train.Saver (tf.global_variables())
  saver.restore (sess, "./models/model.cpkt-1000")

  # save model with builder
  builder = tf.saved_model.builder.SavedModelBuilder ("exported/1/")

  prediction_signature = (
    tf.saved_model.signature_def_utils.build_signature_def(
      inputs = {'x': tf.saved_model.utils.build_tensor_info (net.x)},
      outputs = {'y': tf.saved_model.utils.build_tensor_info (net.predict)])},
      method_name = tf.saved_model.signature_constants.PREDICT_METHOD_NAME)
  )
  # Remember 'x', 'y' for I/O

  legacy_init_op = tf.group (tf.tables_initializer (), name = 'legacy_init_op')
  builder.add_meta_graph_and_variables(
    sess,
    [ tf.saved_model.tag_constants.SERVING ],
    signature_def_map = {'predict': prediction_signature},
    legacy_init_op = legacy_init_op
  )
  # Remember 'signature_def_name'

  builder.save()

.. _`tf.saved_model.builder.SavedModelBuilder`: https://www.tensorflow.org/api_docs/python/tf/saved_model/builder/SavedModelBuilder


Running Server
===================================

You just setup model path and tensorflow configuration, then you can have gRPC and JSON API services.

Example of api.py

.. code:: python

  import tfserver
  import skitai
  from dnn import tf

  pref = skitai.pref ()
  pref.max_client_body_size = 100 * 1024 * 1024 # 100 MB

  # we want to serve 2 models:
  # alias and (model_dir, optional session config)
  pref.config.tf_models ["model1"] = "exported/2"
  pref.config.tf_models ["model2"] = (
  	"exported/3",
  	tf.ConfigProto(
  	  gpu_options=tf.GPUOptions (per_process_gpu_memory_fraction = 0.2),
  	  log_device_placement = False
    )
  )

  # If you want to activate gRPC, should mount on '/'
  skitai.mount ("/", tfserver, pref = pref)
  skitai.run (port = 5000)

And run,

.. code:: bash

  python3 api.py


Adding Custom APIs
-------------------------------------

You can create your own APIs.

If your APIs are located in,

.. code:: bash

  /api/service/loader.py
  /api/service/apis.py

For example,

.. code:: python

  # apis.py

  import tfserver

  def predict (spec_name, signature_name, **inputs):
      result = tfserver.run (spec_name, signature_name, **inputs)
      pred = np.argmax (result ["y"][0])
      return dict (
          confidence = float (result ["y"][0][pred]),
          code = tfserver.tfsess [spec_name].labels [0].item (pred)
      )

  def __mount__ (app):
      import os
      from dnn import tf
      from .helpers.unspsc import datautil

      def load_latest_model (app, model_name, loc, per_process_gpu_memory_fraction = 0.03):
          if not os.path.isdir (loc) or not os.listdir (loc):
              return
          version = max ([int (ver) for ver in os.listdir (loc) if ver.isdigit () and os.path.isdir (os.path.join (loc, ver))])
          model_path = os.path.join (loc, str (version))
          tfconfig = tf.ConfigProto(gpu_options=tf.GPUOptions (
            per_process_gpu_memory_fraction = per_process_gpu_memory_fraction),
            log_device_placement = False
          )
          app.config.tf_models [model_name] = (model_path, tfconfig)
          return model_path

      def initialize_models (app):
          for model in os.listdir (app.config.model_root):
              model_path = load_latest_model (app, model, os.path.join (app.config.model_root, model), 0.1)
              if model == "f22":
                  datautil.load_features (os.path.join (model_path, 'features.pkl'))

      initialize_models (app)

      @app.route ("/", methods = ["GET"])
      def models (was):
          return was.API (models = list (tfserver.tfsess.keys ()))

      @app.route ("/unspsc", methods = ["POST"])
      def unspsc (was, text, signature_name = "predict"):
          x, seq_length = datautil.encode (text)
          result = predict ("unspsc", signature_name, x = [x], seq_length = [seq_length])
          return was.API (result = result)

Then mount these services and run.

.. code:: python

  # serve.py
  import tfserver

	pref = tfserver.preference ("/api")
	from services import apis, loader

	pref.mount ("/tfserver/apis", loader, apis)
	pref.config.model_root = skitai.joinpath ("api/models")
	pref.debug = True
	pref.use_reloader = True
	pref.access_control_allow_origin = ["*"]
	pref.max_client_body_size = 100 * 1024 * 1024 # 100 MB

	skitai.mount ("/", tfserver, pref = pref)
	skitai.run (port = 5000, name = "tfapi")


Request Examples
====================================

gRPC Client
--------------

Using grpcio library,

.. code:: python

  from tfserver import cli
  from tensorflow.python.framework import tensor_util
  import numpy as np

  stub = cli.Server ("http://localhost:5000")
  problem = np.array ([1.0, 2.0])

  resp = stub.predict (
    'model1', #alias for model
    'predict', #signature_def_name
    x = tensor_util.make_tensor_proto(problem.astype('float32'), shape=problem.shape)
  )
  # then get 'y'
  resp.y
  >> np.ndarray ([-1.5, 1.6])

Using aquests for async request,

.. code:: python

  import aquests
  from tfserver import cli
  from tensorflow.python.framework import tensor_util
  import numpy as np

  def print_result (resp):
    cli.Response (resp.data).y
    >> np.ndarray ([-1.5, 1.6])

  stub = aquests.grpc ("http://localhost:5000/tensorflow.serving.PredictionService", callback = print_result)
  problem = np.array ([1.0, 2.0])

  request = cli.build_request (
    'model1',
    'predict',
    x = problem
  )
  stub.Predict (request, 10.0)

  aquests.fetchall ()


RESTful API
-------------

Using requests,

.. code:: python

  import requests

  problem = np.array ([1.0, 2.0])
  api = requests.session ()
  resp = api.post (
    "http://localhost:5000/predict",
    json.dumps ({"x": problem.astype ("float32").tolist()}),
    headers = {"Content-Type": "application/json"}
  )
  data = json.loads (resp.text)
  data ["y"]
  >> [-1.5, 1.6]

Another,

.. code:: python

  from aquests.lib import siesta

  problem = np.array ([1.0, 2.0])
  api = siesta.API ("http://localhost:5000")
  resp = api.predict.post ({"x": problem.astype ("float32").tolist()})
  resp.data.y
  >> [-1.5, 1.6]



Performance Note Comparing with Proto Buffer and JSON
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

- 0.2 (2018. 12.1): integrated with dnn 0.3

- 0.1b8 (2018. 4.13): fix grpc trailers, skitai upgrade is required

- 0.1b6 (2018. 3.19): found works only grpcio 1.4.0

- 0.1b3 (2018. 2. 4): add @app.umounted decorator for clearing resource

- 0.1b2: remove self.tfsess.run (tf.global_variables_initializer())

- 0.1b1 (2018. 1. 28): Beta release

- 0.1a (2018. 1. 4): Alpha release

