#!/usr/bin/env python3
import tensorflow as tf
import numpy as np

x_d=np.random.rand(1000).astype(np.float32)
y_d=x_d*2 + 0.5

###
W=tf.Variable(tf.random_uniform([1],-1.0,1.0))
B=tf.Variable(tf.zeros([1]))
y=W*x_d+B
L=tf.reduce_mean(tf.square(y-y_d))
O=tf.train.GradientDescentOptimizer(0.5)
T=O.minimize(L)
init = tf.global_variables_initializer()
###

sess=tf.Session()
sess.run(init)

for step in range(100):
	sess.run(T)
	print(step,sess.run(W),sess.run(B))
