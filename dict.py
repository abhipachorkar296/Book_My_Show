import numpy as ny
x = ny.array([{"A1":0 , "A2":0 , "A3":0},{"B1":0 , "B2":0 , "B3":0}])
for i in range(20):
	ny.save("seats_%s" % i,x)