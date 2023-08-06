
import tensorflow as tf
if tf.__version__ [0] == '2':
    import warnings
    warnings.warn ("dnn use tf.compat.v1.disable_v2_behavior ()", DeprecationWarning)
    tf.compat.v1.disable_v2_behavior ()

import os
import numpy as np
import time
import pickle
from tensorflow.python.framework import tensor_util
from tensorflow.core.framework import tensor_pb2
import sys
from . import saved_model
from .label import Label

__version__ = "0.3.1.1"

def preference (path = None):
    import skitai
    pref =  skitai.preference (path = path)
    pref.config.tf_models = {}
    return pref

def convert_label (model_path, labels):
    new_labels = [(label._origin, label.name) for label in labels]
    os.rename (os.path.join (model_path, 'labels'), os.path.join (model_path, 'labels.old2'))
    with open (os.path.join (model_path, "labels"), "wb") as f:
        pickle.dump (new_labels, f)

def get_labels (model_path):
    with open (os.path.join (model_path, "labels"), "rb") as f:
        labels = pickle.load (f)
        if str (labels [0].__class__).find ('dnn.label') != -1:
            convert_label (model_path, labels)
            return get_labels (model_path)
    return [Label (*label) for label in labels]


class Session:
    def __init__ (self, model_dir, tfconfig = None):
        self.model_dir = model_dir
        try:
            self.version = int (os.path.basename (model_dir))
        except:
            self.version = 0
        self.tfconfig = tfconfig
        self.graph = tf.Graph ()
        self.tfsess = tf.compat.v1.Session (config = tfconfig, graph = self.graph)
        self.interp =  saved_model.load (model_dir, self.tfsess)
        try:
            self.labels = get_labels (model_dir)
        except OSError:
            self.labels = None

    def get_version (self):
        return self.version

    def run (self, feed_dict, signature_def_name = tf.saved_model.DEFAULT_SERVING_SIGNATURE_DEF_KEY):
        return self.interp._run (feed_dict, signature_def_name)

    def close (self):
        self.tfsess.close ()

tfsess = {}
def load_model (alias, model_dir, tfconfig = None):
    global tfsess
    tfsess [alias] = Session (model_dir, tfconfig)

added_models = {}
def load_models ():
    global tfsess, added_models
    loaded = []
    for alias, (model_dir, tfconfig) in added_models.items ():
        if isinstance (tfconfig, float):
            tfconfig = tf.compat.v1.ConfigProto(
                gpu_options = tf.compat.v1.GPUOptions (per_process_gpu_memory_fraction = tfconfig),
                log_device_placement = False
            )
        tfsess [alias] = Session (model_dir, tfconfig)
        loaded.append ((alias, model_dir))
    return loaded

def add_model (alias, model_dir, gpu_usage):
    global added_models
    added_models [alias] = (model_dir, gpu_usage)

def run (spec_name, signature_name, **inputs):
    global tfsess

    feed_dict = {}
    sess = tfsess [spec_name]
    interp = sess.interp
    for k, v in inputs.items ():
        tensor_name, tensor, dtype, shape = interp.input_map [signature_name][k]
        if isinstance(v, tensor_pb2.TensorProto):
            v = tensor_util.MakeNdarray (v)
        elif type (v) is not np.ndarray:
            v = np.array (v)
        if k == "x": v = interp.normalize (v)
        feed_dict [tensor] = v
    predict_results = sess.run (feed_dict, signature_name)

    response = {}
    for i, result in enumerate (interp.outputs [signature_name]):
        predict_result = predict_results [i]
        response [interp.outputs [signature_name][i][0]] = predict_result
    return response

def close ():
    global tfsess

    for sess in tfsess.values ():
        sess.close ()
    tfsess = {}


