# This code can be put in any Python module, it does not require IPython
# itself to be running already.  It only creates the magics subclass but
# doesn't instantiate it yet.
from __future__ import print_function
from IPython.core.magic import (Magics, magics_class, line_magic, cell_magic)
import pandas as pd

# The class MUST call this class decorator at creation time
@magics_class
class Blueprint(Magics):

    def __init__(self, shell):
        super(Blueprint, self).__init__(shell)
        self._input_datasets = {}
        self._output_datasets = {}

    @cell_magic
    def register_input(self, line, cell):
        "Register input datasets"
        for line in cell.strip().split('\n'):
            if line.strip().startswith('#'):
                continue
            key, val = line.split()
            self._input_datasets[key.strip()] = {"value" : val.strip(), "hitCount" : 0}

    @cell_magic
    def register_output(self, line, cell):
        "Register output datasets"
        for line in cell.strip().split('\n'):
            if line.strip().startswith('#'):
                continue
            key, val = line.split()
            self._output_datasets[key.strip()] = {"value" : val.strip(), "hitCount" : 0}

    @line_magic
    def show_input(self, line):
        "List input datasets"
        return pd.DataFrame(pd.Series(self._input_datasets, name = "input dataset"))

    @line_magic
    def show_output(self, line):
        "List output datasets"
        return pd.DataFrame(pd.Series(self._output_datasets, name = "output dataset"))

    @line_magic
    def get_input(self, name):
        "Get input by name"
        try:
            ds = self._input_datasets[name]
            ds['hitCount'] += 1 
            return ds['value']
        except KeyError:
            self.ipython_display.send_error(u'Could not find input dataset with name {}'.format(name))

    @line_magic
    def get_output(self, name):
        "Get output by name"
        try:
            ds = self._output_datasets[name]
            ds['hitCount'] += 1 
            return ds['value']
        except KeyError:
            self.ipython_display.send_error(u'Could not find output dataset with name {}'.format(name))

    @line_magic
    def input_exist(self, value):
        "Check if input value is registered"
        for ds in self._input_datasets.values():
            if ds['value'] == value:
                ds['hitCount'] += 1 
                return True
        return False

    @line_magic
    def output_exist(self, value):
        "Check if output value is registered"
        for ds in self._output_datasets.values():
            if ds['value'] == value:
                ds['hitCount'] += 1 
                return True
        return False

    @staticmethod
    def _get_input(name):
        return get_ipython().magic('get_input {}'.format(name))

    @staticmethod
    def _get_output(name):
        return get_ipython().magic('get_output {}'.format(name))

    @staticmethod
    def _input_exist(value):
        return get_ipython().magic('input_exist {}'.format(value))

    @staticmethod
    def _output_exist(value):
        return get_ipython().magic('output_exist {}'.format(value))

        
# In order to actually use these magics, you must register them with a
# running IPython.

def load_ipython_extension(ipython):
    """
    Any module file that define a function named `load_ipython_extension`
    can be loaded via `%load_ext module.path` or be configured to be
    autoloaded by IPython at startup time.
    """
    # You can register the class itself without instantiating it.  IPython will
    # call the default constructor on it.
    ipython.register_magics(Blueprint)

def unload_ipython_extension(ipython):
    pass
