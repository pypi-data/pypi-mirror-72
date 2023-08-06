import numpy as np
import os.path
import os
import itertools
import copy

######################
# INTERNAL FUNCTIONS #
######################
def _insert_blank_spaces(string, nblanks):
    ns = string
    l = 0
    for c in string:
        if c=='\n':
            ns = ns[:l+1] + (' '*nblanks) + ns[l+1:] 
            l += nblanks
        l += 1
    return ns


def _get_str_from_array1d(prefix, arr):
    s = "%s[ "%prefix
    for i in range(min(len(arr), 3)):
        if i < len(arr)-1:
            s += "%s, "%arr[i]
        else:
            s += "%s "%arr[i]
    if len(arr) > 3:
        s += "... "
    s += "]\n"
    return s


def _get_str_from_multiarray(prefix, marr, ndim):
    s = "%s[ "%prefix
    for d in range(ndim):
        if d>0: s += " "*(len(prefix)+2)
        s += _get_str_from_array1d("", marr[d])+"\n"
    s += " "*len(prefix) + "]\n"
    return s


def _get_str_from_array(prefix, arr, ndim):
    if arr is np.nan:
        return prefix+"NaN\n"
    elif ndim==1:
        return _get_str_from_array1d(prefix, arr)
    else:
        return _get_str_from_multiarray(prefix, arr, ndim)


#def _compare_arrays(a,b):
#    if a is None:
#        if b is None:
#            return True
#        else:
#            return False
#    elif b is None:
#        return False
#    elif len(a)!=len(b):
#        return False
#    else:
#        for i in range(len(a)):
#            if a[i] != b[i]:
#                return False
#        return True
