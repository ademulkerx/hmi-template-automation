import threading
import time


a = time.time()
b = time.time()
for i in range(10000000000):
    if i % 4 == 0 and time.time() - a < 1:
        print("a",i)
    elif time.time() - a > 2:
        a = time.time()
    elif i % 5 == 0 and time.time() - b < 1:
        print("b", i)
    elif time.time() - b > 3:
        b = time.time()
    