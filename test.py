import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


x = [0,1,2,3,4]
y = [0,2,4,6,8]

plt.plot(x,y, label='temp', color='red', linewidth=2, marker='.')

plt.title('graph')
plt.xlabel('x')
plt.ylabel('y')

plt.xticks([1,2,3,4])
plt.yticks([0,2,4,6,8])

plt.legend()

plt.show()