#!/usr/bin/python
# http://stackoverflow.com/questions/9619199/best-way-to-preserve-numpy-arrays-on-disk
import numpy as np;
import time; 
from tempfile import TemporaryFile
import os

n = 20000000; #20 mil

a = np.arange(n)
b = np.arange(n) * 10
c = np.arange(n) * -0.5

t = time.time()
f = file("tmp.bin","wb")
np.save(f,a);
np.save(f,b);
np.save(f,c);
f.close()
print "save time = ", time.time() - t

t = time.time()
f = file("tmp.bin","rb")
aa = np.load(f);
bb = np.load(f);
cc = np.load(f);
f.close()
print "load time = ", time.time() - t

t = time.time()
filez = TemporaryFile()
np.savez(filez,a = a, b = b, c = c);
print "saveZ time = ", time.time() - t

filez.seek(0)
t = time.time()
z = np.load(filez)
print "loadZ time = ", time.time() - t

t = time.time()
aa = z['a']
bb = z['b']
cc = z['c']
print "assigning time = ", time.time() - t;

os.remove("tmp.bin")