import numpy as np
import pandas as pd
import seaborn as sns
from sklearn import datasets
from sklearn.linear_model import LinearRegression
from matplotlib import pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
v_housing = datasets.load_boston()
x = v_housing.data[:, np.newaxis, 5]
y = v_housing.target
lm = LinearRegression()
lm.fit(x, y)
print('方程的确定性系数R的平方：', lm.score(x, y))
print('线性回归算法w值：', lm.coef_)
print('线性回归算法b值：', lm.intercept_)
plt.scatter(x, y, color='blue')
plt.plot(x, lm.predict(x), color='green', linewidth=6)
plt.xlabel('住宅平均房间数(RM)')
plt.ylabel(u'房屋价格')
plt.title('线性回归住宅平均房间数RM与房屋价格PRICE的关系')
plt.show()