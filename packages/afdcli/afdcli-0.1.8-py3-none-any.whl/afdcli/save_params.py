import pickle
from params import params

p = params()

with open("params.pickle", "wb") as file_: 
    pickle.dump(p, file_, -1)