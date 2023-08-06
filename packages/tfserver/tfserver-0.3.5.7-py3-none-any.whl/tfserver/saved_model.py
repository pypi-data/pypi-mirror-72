import tensorflow as tf
if tf.__version__ [0] == '2':
    tf.compat.v1.disable_v2_behavior ()
from . import normalizer, label
import os
import pickle
import shutil
from rs4 import pathtool
import requests

def check_or_create (sess, graph):
    if sess is None:
        sess = tf.compat.v1.Session ()
    if graph is None:
        graph = sess.graph
    return sess, graph

def check_or_get (sess, graph):
    if sess is None:
        from tensorflow.compat.v1.keras.backend import get_session
        sess = get_session ()
    return check_or_create (sess, graph)

def get_classified_info (inputs_, outputs_, labels = []):
    from tensorflow.python.ops import lookup_ops
    from tensorflow.python.framework import dtypes

    if not labels:
        return outputs_
    if not isinstance (labels, list):
        labels = [labels]

    if len (labels) != 1:
        return outputs_
    x, y = list (inputs_.values ()) [0], list (outputs_.values ()) [0]
    class_names = labels [0].items ()
    outputs_ ['scores'], indices = tf.nn.top_k (y, min (len (class_names), 16))
    table = lookup_ops.index_to_string_table_from_tensor (
        vocabulary_list = tf.constant (class_names),
        default_value = "UNK",
        name = None
    )
    outputs_ ['classes'] = table.lookup (tf.cast(indices, dtype=dtypes.int64))
    return outputs_

def save (model_dir, inputs, outputs = None, signature_name = 'predict', sess = None, graph = None, labels = [], classes = [], train_dir = None):
    if not isinstance (input, dict): # keras model
        model = inputs
        inputs = { model.inputs [0].name.split (":")[0].split ('/')[0]: model.inputs [0] }
        outputs = { model.outputs [0].name.split (":")[0].split ('/')[0]: model.outputs [0] }
    assert outputs
    if classes:
        labels = [label.Label (classes)]

    sess, graph = check_or_get (sess, graph)
    with graph.as_default ():
        if labels:
            outputs = get_classified_info (inputs, outputs, labels)

        inputs = dict ([(k, tf.compat.v1.saved_model.build_tensor_info (v)) for k, v in inputs.items ()])
        outputs = dict ([(k, tf.compat.v1.saved_model.build_tensor_info (v)) for k,v in outputs.items ()])
        prediction_signature = (
            tf.compat.v1.saved_model.signature_def_utils.build_signature_def (
                inputs = inputs,
                outputs = outputs,
                method_name = tf.saved_model.PREDICT_METHOD_NAME
            )
        )
        if not tf.compat.v1.saved_model.signature_def_utils.is_valid_signature (prediction_signature):
            raise ValueError("Error: prediction signature not valid!")

        signature_def_map = {
              tf.saved_model.DEFAULT_SERVING_SIGNATURE_DEF_KEY: prediction_signature,
              signature_name: prediction_signature,
        }
        builder = tf.compat.v1.saved_model.builder.SavedModelBuilder(model_dir)
        builder.add_meta_graph_and_variables (
            sess,
            [tf.saved_model.SERVING],
            signature_def_map = signature_def_map,
            main_op = tf.compat.v1.tables_initializer(),
            strip_default_attrs=True
        )
        builder.save ()

    pathtool.mkdir (os.path.join (model_dir, 'assets'))
    if labels:
        with open (os.path.join (model_dir, 'assets', 'labels'), "wb") as f:
            pickle.dump ([(lb._origin, lb.name) for lb in labels], f)
    return inputs, outputs
convert = save


def deploy (model_dir, url, **data):
    with pathtool.flashfile ('model.zip') as zfile:
        pathtool.zipdir ('model.zip', model_dir)
        pathtool.uploadzip (url, 'model.zip', **data)
    resp = requests.get ('/'.join (url.split ("/")[:-2]))
    return resp.json ()


def load (model_dir, sess = None, graph = None):
    sess, graph = check_or_create (sess, graph)

    with graph.as_default ():
        meta = tf.compat.v1.saved_model.loader.load (
            sess,
            [tf.saved_model.SERVING],
            model_dir
        )

    input_map = {}
    outputs = {}
    activation = {}

    for signature_def_name, signature_def in meta.signature_def.items ():
        input_map [signature_def_name] = {}
        outputs [signature_def_name] = []
        activation [signature_def_name] = []

        for k, v in signature_def.inputs.items ():
            input_map [signature_def_name][k] = (v.name, sess.graph.get_tensor_by_name (v.name), v.dtype, [dim.size for dim in v.tensor_shape.dim])
        for k, v in signature_def.outputs.items ():
            outputs[signature_def_name].append ((k, v.name, sess.graph.get_tensor_by_name (v.name), v.dtype, [dim.size for dim in v.tensor_shape.dim]))
            activation [signature_def_name] .append (v.name)

    return Interpreter (model_dir, meta, input_map, outputs, activation, sess, graph)


class Interpreter:
    def __init__ (self, model_dir, meta, input_map, outputs, activation, sess, graph):
        self.model_dir = model_dir
        self.meta = meta
        self.input_map = input_map
        self.outputs = outputs
        self.activation = activation
        self.sess = sess
        self.graph = graph
        self.asset_dir = os.path.join (self.model_dir, 'assets')
        if not os.path.exists (self.asset_dir):
            self.asset_dir = self.model_dir
        self.norm_factor = self.load_norm_factor ()

    def load_norm_factor (self):
        norm_file = os.path.join (self.asset_dir, "normfactors")
        if os.path.isfile (norm_file):
            with open (norm_file, "rb") as f:
                return pickle.load (f)

    def normalize (self, x):
        if not self.norm_factor:
            return x
        return normalizer.normalize (x, *self.norm_factor)

    def run (self, x, **kargs):
        feed_dict = {}
        kargs ["x"] = x
        for k, v in kargs.items ():
            tensor_name, tensor, dtype, shape = self.input_map [tf.saved_model.DEFAULT_SERVING_SIGNATURE_DEF_KEY][k]
            if k == "x":
                v = self.normalize (v)
            feed_dict [tensor] =  v
        return self._run (feed_dict)

    def _run (self, feed_dict, signature_def_name = None):
        if signature_def_name is None:
            signature_def_name = tf.saved_model.signature_constants.DEFAULT_SERVING_SIGNATURE_DEF_KEY
        with self.graph.as_default (): # IMP: for thread-safe
            return self.sess.run (self.activation [signature_def_name], feed_dict = feed_dict)
