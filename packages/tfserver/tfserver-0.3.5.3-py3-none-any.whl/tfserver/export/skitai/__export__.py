from atila import Atila
import tensorflow as tf
import tfserver
from tfserver.pb2 import prediction_service_pb2, predict_pb2
from tensorflow.python.framework import tensor_util, dtypes
import numpy as np
import os

app = Atila (__name__)

@app.before_mount
def before_mount (wasc):
	for alias, model_dir in tfserver.load_models ():
		wasc.logger ("app", "serve tensorflow model '{}' on {}".format (alias, model_dir), 'info')

@app.umounted
def umounted (wasc):
	tfserver.close ()


# gRPC predict services ------------------------------------
@app.route ("/tensorflow.serving.PredictionService/Predict")
def Predict (was, request, timeout = 10):
	"For GRPC features"
	sess = tfserver.tfsess.get (request.model_spec.name)
	interp = sess.interp
	signature_name = request.model_spec.signature_name

	result = tfserver.run (request.model_spec.name, signature_name, **request.inputs)
	response = predict_pb2.PredictResponse()
	for k, v in result.items ():
		response.outputs [k].CopyFrom (tensor_util.make_tensor_proto (v, np.float32))
	return response


# JSON services --------------------------------------------
@app.route ("/models")
def models (was):
	return was.API (models = tfserver.models ())

@app.route ("/models/<alias>", methods = ['GET'])
def model (was, alias):
	model = tfserver.get_model (alias)
	return was.API (
        path = model.model_dir,
        version = model.version,
        labels = {lb.name: lb.items () for lb in model.labels or []}
    )

@app.route ("/models/<alias>", methods = ['DELETE'])
def delete_model (was, alias):
	tfserver.delete_model (alias)
	return was.API ('204 No Content')

@app.route ("/models/<alias>/versions", methods = ['DELETE'])
@app.inspect (lists = ['versions'])
def delete_model_versions (was, alias, versions):
	tfserver.delete_model_versions (alias, versions)
	return was.API ('204 No Content')

@app.route ("/models/<alias>/versions/<int:version>", methods = ['DELETE'])
def delete_model_version (was, alias, version):
	tfserver.delete_model_versions (alias, version)
	return was.API ('204 No Content')

@app.route ("/models/<alias>/versions/<int:version>", methods = ['POST'])
@app.inspect (booleans = ['refresh', 'overwrite'])
def put_model (was, alias, version, model, refresh = True, overwrite = False):
	with model.flashfile () as zfile:
		try:
			tfserver.add_model_version (alias, version, zfile, refresh, overwrite)
		except AssertionError:
			raise was.Error ('409 Conflict')
	return was.API ('201 Created')

@app.route ("/models/<alias>/reload", methods = ['POST'])
def reload_model (was, alias):
	tfserver.refresh (alias)
	return was.API ('200 OK')

@app.route ("/models/<alias>/predict")
def predict (was, alias, signature_name = "predict", **inputs):
	"For JSON features, but very slow"
	sess = tfserver.tfsess.get (alias)
	interp = sess.interp

	result = tfserver.run (alias, signature_name, **inputs)
	response = {}
	for k, v in result.items ():
		response [k] = v.tolist ()
	return was.API (result = response)

@app.route ("/model/<alias>/version", methods = ['GET']) # lower versoion compat
@app.route ("/models/<alias>/version", methods = ['GET'])
def version (was, alias):
	sess = tfserver.tfsess.get (alias)
	if sess is None:
		return was.response ("404 Not Found")
	return was.API (version = sess.get_version ())
