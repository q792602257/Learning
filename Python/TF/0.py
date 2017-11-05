#!/usr/bin/env python3
# coding:utf8
import tensorflow as tf
import numpy as np

x_d=np.random.rand(1000).astype(np.float32)
y_d=np.random.rand(1000).astype(np.float32)
z_d=4*x_d*y_d + 0.5

###
W=tf.Variable(tf.random_uniform([1],-1.0,1.0))
B=tf.Variable(tf.zeros([1]))
z=W*x_d*y_d+B
L=tf.reduce_mean(tf.square(z-z_d))
O=tf.train.GradientDescentOptimizer(0.5)
T=O.minimize(L)
init = tf.global_variables_initializer()
###

sess=tf.Session()
sess.run(init)

for step in range(100):
	sess.run(T)
	print(step,sess.run(W),sess.run(B))
