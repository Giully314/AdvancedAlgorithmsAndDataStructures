import unittest
import cProfile
import pstats

import random

from datastructures.dheap import DHeap

#Some of the functions are taken from: 
# https://github.com/mlarocca/AlgorithmsAndDataStructuresInAction/blob/master/Python/mlarocca/tests/heap_profile.py

#This is my first time writing a test case using python with unittest and cProfile so i use as reference the link above.



class ProfileHeap(unittest.TestCase):
    BranchingFactors = range(2, 21)
    Runs = 5000
    OutputFileName = "data/stats_heap.csv"
    OutputFileNameHeapify = "data/stats_heapify.csv"


    @staticmethod
    def write_header(f) -> None:
        """Write the header of the output csv file for stats"""
        f.write('test_case,branching_factor,method_name,total_time,cumulative_time,per_call_time\n')
    

    @staticmethod
    def write_row(f, test_case: str, branching_factor: int, method_name: str, total_time: float,
                  cumulative_time: float, per_call_time: float) -> None:
        """Add a row of data to the stats csv file"""
        f.write(f'{test_case},{branching_factor},{method_name},{total_time},{cumulative_time},{per_call_time}\n')


    @staticmethod
    def get_running_times(st: pstats.Stats, method_name: str) -> list[tuple[str, float]]:
        ps = st.strip_dirs().stats

        # Takes methods frequency_table_to_heap, heap_to_tree, and _heapify
        def is_heap_method(k):
            return method_name in k[2]

        keys = list(filter(is_heap_method, ps.keys()))
        # cc, nc, tt, ct, callers = ps[key]
        #  ps[key][2] -> tt -> total time
        #  ps[key][3] -> ct -> cumulative time
        return [(key[2], ps[key][2], ps[key][3], ps[key][3] / ps[key][1]) for key in keys]


    def test_insert_and_top(self) -> None:
        with open(ProfileHeap.OutputFileName, "w") as f:
            ProfileHeap.write_header(f)

            for b in ProfileHeap.BranchingFactors:
                heap = DHeap(b)
                
                for _ in range(ProfileHeap.Runs):
                    profiler = cProfile.Profile()
                    profiler.runcall(heap.insert, random.random(), random.randint(0, 2000))
                    st = pstats.Stats(profiler)

                    for method_name, total_time, cumulative_time, per_call_time in ProfileHeap.get_running_times(st, "insert"):
                        ProfileHeap.write_row(f, "heap", b, method_name, total_time, cumulative_time, per_call_time)
                    
                     
                while not heap.empty():
                    profiler = cProfile.Profile()
                    profiler.runcall(heap.top)
                    st = pstats.Stats(profiler)

                    for method_name, total_time, cumulative_time, per_call_time in ProfileHeap.get_running_times(st, "top"):
                        ProfileHeap.write_row(f, "heap", b, method_name, total_time, cumulative_time, per_call_time)

                    


    def test_heapify(self) -> None:
        with open(ProfileHeap.OutputFileNameHeapify, "w") as f:
            ProfileHeap.write_header(f)
            
            for b in ProfileHeap.BranchingFactors:
                for _ in range(ProfileHeap.Runs):
                    n = 1000 + random.randint(0, 1000)
                    elements = [random.random() for i in range(n)]
                    priorities = [random.randint(0, 2000) for i in range(n)]
                    
                    profiler = cProfile.Profile()
                    profiler.runcall(DHeap, b, "max", elements, priorities)

                    st = pstats.Stats(profiler)
                    
                    for method_name, total_time, cumulative_time, per_call_time in ProfileHeap.get_running_times(st, "_heapify"):
                        ProfileHeap.write_row(f, "heap", b, method_name, total_time, cumulative_time, per_call_time)


if __name__ == "__main__":
    unittest.main()