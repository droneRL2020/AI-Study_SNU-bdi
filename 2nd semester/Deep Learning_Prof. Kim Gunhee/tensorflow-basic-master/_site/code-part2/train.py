import tensorflow as tf
import numpy as np
import models
from tensorflow.examples.tutorials.mnist import input_data
from IPython import embed
from tensorflow import flags
FLAGS = flags.FLAGS
flags.DEFINE_string("log_dir", "./logs/default", "default summary/checkpoint directory")
def main(_):
  mnist = input_data.read_data_sets("./data", one_hot=True)

  # defien model input: image and ground-truth label
  model_inputs = tf.placeholder(dtype=tf.float32, shape=[None, 784])
  labels = tf.placeholder(dtype=tf.float32, shape=[None, 10])

  model = getattr(models, "DNN", None)()
  predictions = model.create_model(model_inputs)

  # define cross entropy loss term
  loss = tf.losses.softmax_cross_entropy(
    onehot_labels=labels,
    logits=predictions)

  dense_predictions = tf.argmax(predictions, axis=1)
  dense_labels = tf.argmax(labels, axis=1)
  equals = tf.cast(tf.equal(dense_predictions, dense_labels), tf.float32)
  acc = tf.reduce_mean(equals)

  tf.summary.scalar("loss", loss)
  tf.summary.scalar("acc", acc)
  merge_op = tf.summary.merge_all()

  optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.01)
  train_op = optimizer.minimize(loss)
  with tf.Session() as sess:
    summary_writer_train = tf.summary.FileWriter(FLAGS.log_dir + "/train", sess.graph)
    summary_writer_val = tf.summary.FileWriter(FLAGS.log_dir + "/validation", sess.graph)

    sess.run(tf.global_variables_initializer())
    for step in range(10000):
      batch_images, batch_labels = mnist.train.next_batch(128)
      images_val, labels_val = mnist.validation.next_batch(128)
      feed = {model_inputs: batch_images, labels: batch_labels}
      _, loss_val = sess.run([train_op, loss], feed_dict=feed)
      print ("step {} | loss {}".format(step, loss_val))
      if step % 10 == 0:
        summary_train = sess.run(merge_op, feed_dict=feed)
        feed = {model_inputs: images_val, labels:labels_val}
        summary_val = sess.run(merge_op, feed_dict=feed)
        summary_writer_train.add_summary(summary_train, step)
        summary_writer_val.add_summary(summary_val, step)

if __name__ == "__main__":
  tf.app.run()




