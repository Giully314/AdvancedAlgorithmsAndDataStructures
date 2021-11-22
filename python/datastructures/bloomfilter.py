import bitarray
import random as rnd
import math

#I think that this datastructure is one of the small exception that has 0 sense to implement in a language like Python.
#However i use Python only to understand the dynamics of the datastructure and the concepts behind the operations without worry about
#implementation details that can be skipped at first. 


class BloomFilter:
    def __init__(self, max_size, max_tolerance=0.01, seed=None):
        rnd.seed(seed)
        self.size = 0
        self.max_size = max_size
        self.num_bits = -math.ceil(max_size * math.log2(max_tolerance) / math.log(2))
        self.num_hash_funcs = -math.ceil(math.log2(max_tolerance))
        self.bits_array = bitarray.bitarray(self.num_bits)
        self.bits_array[0:-1] = False



    def _init_hash_funcs(self):
        return 


b = BloomFilter(1000)