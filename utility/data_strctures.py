from collections import OrderedDict
#from abc import ABC, abstractmethod


class CSVSlicer():
    
    def __init__(self, fn : str) -> None:
        self.fn = fn
        
    def get_list_slice(self, fields):
        d = OrderedDict()