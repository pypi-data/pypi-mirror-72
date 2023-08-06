import sys
import os
import linecache

def trace(f):
    def globaltrace(frame, why, arg):
        if why == "call":
            return localtrace
        return None

    def localtrace(frame, why, arg):
        if why == "line":
            # record the file name and line number of every trace
            filename = frame.f_code.co_filename
            funcname = frame.f_code.co_name
            lineno = frame.f_lineno

            if frame.f_code != f.__code__:
                return localtrace

            bname = os.path.basename(filename)
            print("{}({}) {}: {}".format( bname,
                                          lineno,
                                          funcname,
                                          linecache.getline(filename, lineno)), end='')
        return localtrace

    def _f(*args, **kwds):
        sys.settrace(globaltrace)
        result = f(*args, **kwds)
        sys.settrace(None)
        print()
        return result

    return _f
