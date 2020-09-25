#### sklearn学习

---

1. sklearn是机器学习中的常用第三方模块，对常用的机器学习方法进行了封装，包括回归、降维、分类、聚类等方法

2. 引入需要训练的数据

   + Sklearn datasets  Sklearn 自带部分数据集，例如使用```datasets.load_boston()```可以加载波士顿房价数据![img](https://upload-images.jianshu.io/upload_images/77550-feb8b5370cedb701.jpg?imageMogr2/auto-orient/strip|imageView2/2/w/720/format/webp)

   + 自己构造数据用以学习

     ```python
     from sklearn import datasets#引入数据集
     #构造的各种参数可以根据自己需要调整
     X,y=datasets.make_regression(n_samples=100,n_features=1,n_targets=1,noise=1)
     ```

     绘制自己构造的数据图

     ![image-20200925225231752](C:\Users\hp\AppData\Roaming\Typora\typora-user-images\image-20200925225231752.png)

   

3. 线性回归模型

   ```python
   from sklearn.linear_model import LinearRegression#引入线性回归模型
   ###训练数据###
   model=LinearRegression()
   model.fit(data_X,data_y)
   model.predict(data_X[:4,:])#预测前4个数据
   ```

   

   

