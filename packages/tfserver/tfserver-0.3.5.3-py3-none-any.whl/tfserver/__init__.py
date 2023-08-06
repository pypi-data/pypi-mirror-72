__version__ = "0.3.5.3"

import tensorflow as tf
if tf.__version__ [0] == '2':
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
import threading
from rs4 import pathtool
import shutil

glock = threading.RLock ()

def preference (path = None):
    import skitai
    pref =  skitai.preference (path = path)
    pref.config.tf_models = {}
    return pref

def convert_labels (model_path, labels):
    new_labels = [(label._origin, label.name) for label in labels]
    os.rename (os.path.join (model_path, 'labels'), os.path.join (model_path, 'labels.old2'))
    with open (os.path.join (model_path, "labels"), "wb") as f:
        pickle.dump (new_labels, f)

def load_labels (model_path):
    with open (os.path.join (model_path, "labels"), "rb") as f:
        labels = pickle.load (f)
        if str (labels [0].__class__).find ('dnn.label') != -1:
            convert_labels (model_path, labels)
            return load_labels (model_path)
    return [Label (*label) for label in labels]


class Session:
    def __init__ (self, model_dir, tfconfig = None):
        self.model_dir = model_dir
        try:
            self.version = int (os.path.basename (model_dir))
        except:
            self.version = 0
        self.model_root = os.path.dirname (model_dir)
        self.tfconfig = tfconfig
        self.graph = tf.Graph ()
        self.tfsess = tf.compat.v1.Session (config = tfconfig, graph = self.graph)
        self.interp = saved_model.load (model_dir, self.tfsess)
        try:
            self.labels = load_labels (model_dir)
        except OSError:
            self.labels = None

    def remove_all_resources (self):
        shutil.rmtree (self.model_root)

    def remove_version (self, version):
        deletable = os.path.join (self.model_root, str (version))
        if not os.path.isdir (deletable):
            return
        shutil.rmtree (deletable)

    def add_version (self, version, asset_zfile):
        target = os.path.join (self.model_root, str (version))
        pathtool.unzipdir (asset_zfile, target)

    def get_version (self):
        return self.version

    def run (self, feed_dict, signature_def_name = tf.saved_model.DEFAULT_SERVING_SIGNATURE_DEF_KEY):
        return self.interp._run (feed_dict, signature_def_name)

    def close (self):
        self.tfsess.close ()

    def get_latest_version (self):
        vs = [ int (v) for v in os.listdir (self.model_root) if v.isdigit () ]
        if not vs:
            return None
        return sorted (vs) [-1]


tfsess = {}
def load_model (alias, model_dir, tfconfig = None):
    global tfsess
    if isinstance (tfconfig, float):
        tfconfig = tf.compat.v1.ConfigProto(
            gpu_options = tf.compat.v1.GPUOptions (per_process_gpu_memory_fraction = tfconfig),
            log_device_placement = False
        )
    sess = Session (model_dir, tfconfig)
    with glock:
        tfsess [alias] = sess

added_models = {}
def load_models ():
    global added_models
    loaded = []
    for alias, (model_dir, tfconfig) in added_models.items ():
        load_model (alias, model_dir, tfconfig)
        loaded.append ((alias, model_dir))
    return loaded

def add_model (alias, model_dir, gpu_usage):
    global added_models
    with glock:
        added_models [alias] = (model_dir, gpu_usage)

def close (alias = None):
    global tfsess
    if alias:
        with glock:
            if alias not in tfsess:
                return
            tfsess [alias].close ()
            del tfsess [alias]
            return

    with glock:
        for sess in tfsess.values ():
            sess.close ()
        tfsess = {}

# public methods --------------------------
def predict (alias, signature_name = 'predict', **inputs):
    global tfsess
    feed_dict = {}
    sess = tfsess [alias]
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
run = predict

def get_labels (alias):
    with glock:
        return tfsess [alias].labels

def get_model (alias):
    global tfsess
    with glock:
        return tfsess.get (alias)

def models ():
    global tfsess
    with glock:
        return list (tfsess.keys ())

def delete_model (alias):
    model = get_model (alias)
    close (alias)
    model.remove_all_resources ()

def refresh_model (alias):
    model = get_model (alias)
    close (alias)
    version = model.get_latest_version ()
    if not version:
        return
    load_model (alias, os.path.join (model.model_root, str (version)), model.tfconfig)

def guesss_model_root ():
    dirs = {}
    for model_name in models ():
        m = get_model (model_name)
        root = os.path.dirname (m.model_root)
        try: dirs [root] += 1
        except KeyError: dirs [root] = 1
    return sorted (dirs.items (), key = lambda x: x [1]) [-1][0]

def delete_model_versions (alias, versions):
    if isinstance (versions, int):
        versions = [versions]
    versions = sorted (map (int, versions))
    model = get_model (alias)
    for version in versions:
        model.remove_version (version)
        if model.version == version:
            refresh_model (alias)

def add_model_version (alias, version, asset_zfile, refresh = True, overwrite = False):
    model = get_model (alias)
    if model:
        model_dir = os.path.join (model.model_root, str (version))
        if not overwrite:
            assert not os.path.exists (model_dir)
        model.add_version (version, asset_zfile)
        refresh and refresh_model (alias)
        return

    root_dir = guesss_model_root ()
    model_dir = os.path.join (root_dir, alias, str (version))
    pathtool.unzipdir (asset_zfile, model_dir)
    refresh and load_model (alias, model_dir, 0.1)
