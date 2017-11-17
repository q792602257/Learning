import numpy as np
import pandas as pd
import time

np.random.seed(2)

STATE = 9
ACTIONS = ["l","r"]
EPSILON = 0.9 #greedy police
ALPHA = 0.1 #Learning Rate
LAMBDA = 0.9 #Discount Factor
MAX_EPISODES=10 # count
FRESH = 0.001 #per every step

def buildQtable(n_s,act):
	table=pd.DataFrame(
		np.zeros((n_s,len(act))),
		columns=act,
	)
	return table
def choice(state,q_t):
	s_a = q_t.iloc[state,:]
	if (np.random.uniform() > EPSILON) or (s_a.all==0):
		a_n = np.random.choice(ACTIONS)
	else:
		a_n = s_a.argmax()
	return a_n
def getFeedback(S,A):
	if A=="r":
		if S==STATE - 2:
			S_="t"
			R =1
		else:
			S_ = S+1
			R=0
	else:
		R=0
		if S == 0:
			S_=S
		else:
			S_=S-1
	return S_,R
def buildEnv(S,E,step):
	envL=["_"]*(STATE-1)+["0"]
	if S=="t":
		print('\rE : %s\tStep : %s'%(E+1,step))
		time.sleep(3)
		print("\r\t\t\t\t\t")
	else:
		envL[S]="#"
		print("\r%s" % ("".join(envL)) , end="")
		time.sleep(FRESH)
def rl():
	q_t=buildQtable(STATE,ACTIONS)
	for ep in range(MAX_EPISODES):
		step=0
		S=0
		is_T = False
		buildEnv(S,ep,step)
		while not is_T:
			A=choice(S,q_t)
			S_,R=getFeedback(S,A)
			q_pred = q_t.ix[S,A]
			if S_ != "t":
				q_targ=R+LAMBDA*q_t.iloc[S_,:].max()
			else:
				q_targ=R
				is_T=True
			q_t.ix[S,A] = ALPHA*(q_targ-q_pred)
			S=S_
			buildEnv(S,ep,step+1)
			step+=1
	return q_t
q_t=rl()
print("Q_Table:")
print(q_t)
