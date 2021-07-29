

import hashlib
import time
import numpy as np
import random


def hash_id(id):
    k = str(time.time()).encode('utf-8')
    padded=str(random.randint(0,100000))+str(k)+id+str(random.randint(0,100000))
    padded=padded.encode()
    hash_object = hashlib.sha256(padded)
    hex_dig = hash_object.hexdigest()
    return hex_dig

def vectorized_hashing(id):
    id = id.astype('str')
    vfunc = np.vectorize(hash_id)
    return vfunc(id)

# ar=np.array([1,2,3,4,5])
# ar=vectorized_hashing(ar)
# print(ar)