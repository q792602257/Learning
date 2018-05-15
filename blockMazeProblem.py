import numpy as np
from time import sleep
import os

def caculate_distance(s_x,s_y,e_x,e_y):#TODO:计算路程最好
    a_x = abs(s_x-e_x)
    a_y = abs(s_y-e_y)
    a_s = abs(a_x-a_y)
    a_c = int(abs(a_x+a_y-a_s)/2)
    return a_s*10+a_c*14

class maze:#TODO:代码乱
    def __init__(self,start=[4,2],end=[1,4],shape=[5,5], blocks=[[3,2],[2,3],[3,3],[3,4]]):
        self.shape=shape
        self.a=np.zeros(shape,int)
        for i,j in blocks:
            self.a[i][j]=1
        self.b=np.zeros(shape,int)
        self.c=np.zeros(shape,int)
        self.d=np.zeros(shape,int)
        for i in range(shape[0]):
            for j in range(shape[1]):
                self.b[i][j]=1000
                self.c[i][j]=1000
        self.start_x,self.start_y=start
        self.o_s_x=self.start_x
        self.o_s_y=self.start_y
        self.a[self.start_x][self.start_y]=2
        self.end_x,self.end_y=end
        self.a[self.end_x][self.end_y]=3
        self.a_o=self.a.copy()
        self.b_o=self.b.copy()
        self.c_o=self.c.copy()
        self.d_o=self.d.copy()
        self.step=0
    def run(self):
        if [self.start_x,self.start_y]==[self.end_x,self.end_y]:
            print("------Finished------")
            return True
        # print(self.a)
        for x in range(-1,2):
            for y in range(-1,2):
                if self.start_x+x >= self.shape[0] or self.start_y+y >= self.shape[1] or self.start_x+x < 0 or self.start_y+y < 0 :
                    continue
                if self.a_o[self.start_x+x][self.start_y+y]==1 or self.a_o[self.start_x+x][self.start_y+y]==7:
                    continue
                self.b[self.start_x+x][self.start_y+y]=caculate_distance(self.o_s_x,self.o_s_y,self.start_x+x,self.start_y+y)
                self.c[self.start_x+x][self.start_y+y]=caculate_distance(self.end_x,self.end_y,self.start_x+x,self.start_y+y)
                self.b_o[self.start_x+x][self.start_y+y]=self.b[self.start_x+x][self.start_y+y]
                self.c_o[self.start_x+x][self.start_y+y]=self.c[self.start_x+x][self.start_y+y]
        # print("行走距离:----")
        # print(self.b)
        # print("目标距离:----")
        # print(self.c)
        # print("综合判断:----")
        self.d_o=0.25*self.b_o+self.c_o
        self.d=0.25*self.b+self.c
        # print(self.d)
        self.a_o[self.start_x][self.start_y]=7
        self.b_o[self.start_x][self.start_y]=1000
        self.c_o[self.start_x][self.start_y]=1000
        self.d_o[self.start_x][self.start_y]=1000
        print("实时地图:----")
        print(self.a_o)
        self.start_x,self.start_y=np.unravel_index(self.d_o.argmin(),self.d_o.shape)
        self.step+=1
        print(" 第%2d步 :----"%(self.step))
        print([self.start_x,self.start_y],self.d_o[self.start_x][self.start_y])
        if [self.start_x,self.start_y]==[self.end_x,self.end_y]:
            print("------Finished------")
            return True
        else:
            print("--------------------")
            return False

a=maze(start=[19,0],end=[1,1],shape=[20,20],blocks=[
    [2,0],[2,1],[2,2],[2,3],
    [3,2],[3,3],[3,4],[3,5],[3,6],
    [4,6],[4,7],
    [5,7],[5,8],
    [6,8],[6,9],
    [7,9],[7,10],
    [8,10],[8,11],
    [9,10],
    [10,10],
    [11,10],
    [12,8],[12,11],[12,12],[12,9],[12,10],
    [13,12],[13,14],[13,5],[13,6],[13,10],
    [14,10],
    [15,10]
])
os.system("cls")
while not a.run():
    sleep(0.2)
    os.system("cls")
    continue
