import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

def add(I,Is,Os,Af=None):
	W=tf.Variable(tf.random_normal([Is,Os]))
	b=tf.Variable(tf.zeros([1,Os])+0.01)
	WxPb=tf.matmul(I,W)+b
	if Af is None:
		return WxPb
	return Af(WxPb)

X=np.linspace(-2,2,100)[:,np.newaxis]
N=np.random.normal(0,0.2,X.shape)
Y=np.square(X)*2+7+N

Xs=tf.placeholder(tf.float32,[None,1])
Ys=tf.placeholder(tf.float32,[None,1])

l1=add(Xs,1,10,tf.nn.relu)
Pd=add(l1,10,1,None)

Los=tf.reduce_mean(tf.reduce_sum(tf.square(Ys-Pd),reduction_indices=[1]))
Ts=tf.train.GradientDescentOptimizer(0.05).minimize(Los)

Init=tf.initialize_all_variables()
Sess=tf.Session()
Sess.run(Init)

F=plt.figure()
plt.ion()
Ax=F.add_subplot(1,1,1)
plt.axis([-2,2,6,18])
Ax.scatter(X,Y)
plt.show()

for i in range(1000):
	try:
		Ax.lines.remove(Li[0])
	except Exception:
		pass
	Sess.run(Ts,feed_dict={Xs:X,Ys:Y})
	if i%3==0:
		PdV=Sess.run(Pd,feed_dict={Xs:X})
		Li=Ax.plot(X,PdV,'r',lw=2)
		plt.pause(0.01)
