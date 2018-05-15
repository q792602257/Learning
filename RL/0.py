import numpy as np
import pandas as pd
import time
import os

LOGO ="Starting..."
STATE = 10
ACTIONS = ["l","r"]
EPSILON = 0.8 #greedy police(信任)
ALPHA = 0.5 #Learning Rate(效率)
LAMBDA = 0.9 #Discount Factor(衰减)
MAX_EPISODES=1000 # count
FRESH = 0.005 #per every step

def buildQtable(n_s,act):
	table=pd.DataFrame(
		np.zeros((n_s,len(act))),
		columns=act,
	)
	return table
def restoreQtable(fn="rl0.csv"):
	q_t = pd.read_csv(fn, header=0, index_col=0)
	return q_t
def saveQtable(q_t,fn="rl0.csv"):
	q_t.to_csv(fn)
	return True
def choice(state,q_t):
	s_a = q_t.iloc[state,:]
	if (np.random.uniform() > EPSILON) or (s_a.all()==0):
		a_n = np.random.choice(ACTIONS)
	else:
		a_n = s_a.argmax()
	return a_n
def getFeedback(S,A):
	if A=="r":
		if S==STATE - 1:
			S_="t"
			R =1
		else:
			S_ = S+1
			R=0
	else:
		if S == 0:
			S_= "d"
			R = -1
		else:
			S_=S-1
			R = 0
	return S_,R
def buildEnv(S,E,step):
	global LOGO
	envL=["_"]*(STATE)+["$"]
	if S=="t" or S=="d":
		LOGO = '\rEp : %s\tStep : %s'%(E+1,step)
		time.sleep(FRESH)
		print("\r\t\t\t\t\t")
	else:
		envL[S]="#"
		print("\r%s" % ("".join(envL)) , end="")
		time.sleep(FRESH)
def rl(q_t=buildQtable(STATE,ACTIONS)):
	for ep in range(MAX_EPISODES):
		step=0
		S=0
		is_T = False
		buildEnv(S,ep,step)
		while not is_T:
			A=choice(S,q_t)
			S_,R=getFeedback(S,A)
			q_pred = q_t.ix[S,A]
			if S_ != "t" and S_ != "d":
				q_targ=R+LAMBDA*q_t.iloc[S_,:].max()
			else:
				q_targ=R
				is_T=True
			q_t.ix[S,A] += ALPHA*(q_targ-q_pred)
			S=S_
			buildEnv(S,ep,step+1)
			step+=1
			os.system("cls")
			print (LOGO)
			print (q_t)
	return q_t
# q_t=restoreQtable()
# print (q_t)
q_t=rl()
saveQtable(q_t)
print("Q_Table:")
print(q_t)
