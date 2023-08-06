import tensorflow as tf
from . import normalizer
import os
import pickle
import shutil

def check_or_create (sess, graph):
    from tensorflow.compat.v1.keras.backend import get_session
    if sess is None:
        sess = get_session ()
    if graph is None:
        graph = sess.graph
    return sess, graph

def save (model_dir, signature_name, inputs, outputs, sess = None, graph = None, labels = None, train_dir = None):
    from tensorflow.python.ops import lookup_ops
    from tensorflow.python.framework import dtypes

    sess, graph = check_or_create (sess, graph)
    with graph.as_default ():
        if labels:
            if not isinstance (labels, list):
                labels = [labels]
            if len (labels) == 1:
                class_names = labels [0].items ()
                NUM_CLASSES = len (class_names)

                y = None
                for k, v in outputs.items ():
                    y = v
                values, indices = tf.nn.top_k(y, min (NUM_CLASSES, 16))
                table = lookup_ops.index_to_string_table_from_tensor(
                    vocabulary_list=tf.constant(class_names),
                    default_value="UNK",
                    name=None
                    )
                prediction_classes = table.lookup(tf.cast(indices, dtype=dtypes.int64))
                outputs ['classes'] = prediction_classes
                outputs ['scores'] = values

        builder = tf.compat.v1.saved_model.builder.SavedModelBuilder(model_dir)
        inputs=dict ([(k, tf.compat.v1.saved_model.utils.build_tensor_info (v)) for k, v in inputs.items ()])
        outputs=dict ([(k, tf.compat.v1.saved_model.utils.build_tensor_info (v)) for k,v in outputs.items ()])
        prediction_signature = (
          tf.compat.v1.saved_model.signature_def_utils.build_signature_def (
              inputs=inputs,
              outputs=outputs,
              method_name=tf.saved_model.PREDICT_METHOD_NAME)
          )
        valid_signature = tf.compat.v1.saved_model.signature_def_utils.is_valid_signature (prediction_signature)
        if not valid_signature:
            raise ValueError("Error: prediction signature not valid!")
        builder.add_meta_graph_and_variables (
          sess,
          [tf.saved_model.SERVING],
          signature_def_map = {
              tf.saved_model.DEFAULT_SERVING_SIGNATURE_DEF_KEY: prediction_signature,
              signature_name: prediction_signature
          }
        )
        builder.save ()
    return inputs, outputs
convert = save

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
        self.norm_factor = self.load_norm_factor ()

    def load_norm_factor (self):
        norm_file = os.path.join (self.model_dir, "normfactors")
        if os.path.isfile (norm_file):
            with open (norm_file, "rb") as f:
                return pickle.load (f)

    def normalize (self, x):
        # SHOLUD BE SYMC with dnn,DNN.normalize ()
        if not self.norm_factor:
            return x
        return normalizer.normalize (x, *self.norm_factor)

    def  run (self, x, **kargs):
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
