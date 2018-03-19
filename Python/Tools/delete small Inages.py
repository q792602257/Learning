import os,sys,Image,glob

  
s=glob.glob(os.path.join(os.path.abspath(''),'wallpaper*','*'))
for f in s:
    im=Image.open(f)
    if (im.size[0]<1000 or im.size[1]<700):
        os.remove(f)
        print f+'\t'+str(im.size)
