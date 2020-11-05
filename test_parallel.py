import multiprocessing as mp
from itertools import repeat
import time
def multiply(item):
    return item **2



if __name__ == "__main__":
    start_time = time.time()
    print("before pool")
    p = mp.Pool(mp.cpu_count())
    l=[1,2,3,4,4]
    l=list(range(0,10000000))
    print("before map")
    result = p.map(multiply, l)

    p.close()
    print("before join")
    p.join()
    end_time = time.time()
    print("time = " + str(end_time - start_time))
    # print(result)