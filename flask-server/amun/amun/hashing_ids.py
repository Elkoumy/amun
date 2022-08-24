

import hashlib
import time
import numpy as np
import random
import pandas as pd


def hash_id(id):
    k = str(time.time()).encode('utf-8')
    padded=str(random.randint(0,100000))+str(k)+id+str(random.randint(0,100000))
    padded=padded.encode()
    hash_object = hashlib.sha256(padded)
    hex_dig = hash_object.hexdigest()
    return hex_dig

def vectorized_hashing(id):
    id=id.astype('str')
    unique_id = np.unique(id)
    vfunc = np.vectorize(hash_id)
    res=vfunc(unique_id)
    map=pd.DataFrame({'org':unique_id, 'new':res})
    id = pd.Series(id, name='org')
    id=id.reset_index()
    # t = id.join(map, on='org', lsuffix='l', rsuffix='r')
    id = pd.merge(id, map, on='org')
    id = id.set_index('index')
    return id['new']

# ar=np.array([1,2,2,3,4,5])
# ar=vectorized_hashing(ar)
# print(ar)