# 虽然但是，这个代码好像有点错误
import numpy as np
import matplotlib.pyplot as plt

# 定义高斯分布的参数
mu = 100    # 均值
sigma = 10 # 标准差

# 生成数据
x = np.linspace(mu - 4*sigma, mu + 4*sigma, 100)
y = (1/(np.sqrt(2 * np.pi * sigma**2))) * np.exp(-(x - mu)**2 / (2 * sigma**2))

# 绘制高斯分布曲线
plt.figure(figsize=(8, 6))
plt.plot(x, y, label='Gaussian Distribution')
plt.title('Gaussian Distribution')
plt.xlabel('x')
plt.ylabel('Probability Density')
plt.legend()
plt.grid(True)
plt.show()