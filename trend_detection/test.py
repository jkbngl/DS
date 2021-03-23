import numpy as np
import pymannkendall as mk

# Data generation for analysis
data = [1,2,3,4,5,8]

result = mk.original_test(data)
print(result)
