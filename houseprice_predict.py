import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression


w = 1
b = 0
y_hat = int()
m = 9
f = np.array([])


#size in squaremeters
x1 = np.array([
    60/180,
    175/180,
    82/180,
    4/180,
    180/180,
    105/180,
    60/180,
    40/180,
    102/180
])
print(x1)
x1.reshape((-1, 1))
print(x1)
#typology
x2 = np.array([
    0,
    3,
    1,
    1,
    4,
    3,
    1,
    1,
    2
])

#age
x3 = np.array([
    29,
    10,
    35,
    1,
    2,
    20,
    72,
    72,
    2
])

#floor
x4 = np.array([
    0,
    3,
    0,
    2,
    0,
    3,
    0,
    1,
    2
])

#energy class
x5 = np.array([
    3,
    5,
    1,
    5,
    6,
    1,
    0,
    3,
    4
])

#price in thousands €
y = np.array([
    350/1695,
    1695/1695,
    189/1695,
    275/1695,
    735/1695,
    245/1695,
    230/1695,
    99/1695,
    760/1695
])

x_vector = np.array([x1,x2,x3,x4,x5])

#df1 = pd.DataFrame(new_array, columns=['Size', 'Price'], index=['Item_'+str(i+1) for i in range(m)])


plt.scatter(x1,y)
model = LinearRegression().fit(x1.reshape(1,-1),y)
plt.show()
print(model)
r_sq=model.score(x1,y)

y_pred = model.predict(x1)


#linear regression model - f w,b(x) = wx + b
#b = 400
#


def apply_gradientdescent():
    derivate = 0