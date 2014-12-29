__author__ = 'rened'

import inspect, importlib as implib
import subprocess

unitlist = []

if __name__ == "__main__":
    mod = implib.import_module( "read_labview_rev2" )
    for i in inspect.getmembers(mod, inspect.ismodule ):
        unitlist.append(( i[1].__name__).split('.')[0])

tell_list = list(set(unitlist))

for item in tell_list:
    cmd = "/home/rened/anaconda/bin/pip freeze | grep "+item
    ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    output = ps.communicate()[0]
    print output.split('\n')[0]


