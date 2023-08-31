import numpy as np
import matplotlib.pyplot as plt

arr:np.ndarray=np.load("data.npy")
arr = arr[arr != 0]

std_deviation = np.std(arr)
# 设置标准差阈值
std_dev_threshold = 1
# 根据标准差筛选数据
arr = arr[np.abs(arr - np.mean(arr)) / std_deviation <= std_dev_threshold]

plt.hist(arr,range=(0,arr.max()),bins=20)
plt.show()