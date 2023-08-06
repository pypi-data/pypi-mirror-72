from time import sleep
import numpy as np
from deepdiff import DeepDiff, DeepHash

# t1 = np.array([[1, 2], [3, 4]])
# t2 = np.array([[2, 2], [3, 3]])

# diff = DeepDiff(t1, t2, view='tree')

# import ipdb; ipdb.set_trace()

# print('hello')

t1 = np.array([[1, 2, 3, 4], [4, 2, 2, 1]], np.int8)
t1_hash = DeepHash(t1)
msg = None
# try:
#     t1_hash[t1[0]]
# except KeyError as e:
#     msg = str(e).strip("'")
print(id(t1[0]))
print(t1[0])
print(id(t1[1]))
print(t1[1])
print(id(t1[0]) == id(t1[1]))
print(t1[0] is t1[1])
# print(id(t1[0]))
# print(id(t1[0]))
# print(id(t1[0]))
# print(id(t1[0]))
# print(id(t1[0]))
# for i in range(1000):
#     sleep(0.01 * i)
#     print(eval('id(t1[0])'))
# # print(t1_hash[t1[0]])
# # print(msg)
