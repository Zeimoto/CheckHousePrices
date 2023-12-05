import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from api_tester import read_file



x = np.asanyarray()
y = np.asanyarray()


x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=10)

#df1 = pd.DataFrame(new_array, columns=['Size', 'Price'], index=['Item_'+str(i+1) for i in range(m)])