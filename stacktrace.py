# This module is inspired (initially, outright borrowed) by a stackoverflow
# article :: http://stackoverflow.com/questions/132058/getting-stack-trace-from-a-running-python-application

# To use, just call the listen() function at some point when your program
# starts up (You could even stick it in site.py to have all python programs use
# it), and let it run. At any point, send the process a SIGUSR1 signal, using
# kill, or in python:
#
#    os.kill(pid, signal.SIGUSR1)
#
# This will cause the program to break to a python console at the point it is
# currently at, showing you the stack trace, and letting you manipulate the
# variables. Use control-d (EOF) to continue running (though note that you will
# probably interrupt any I/O etc at the point you signal, so it isn't fully
# non-intrusive.

import code, traceback, signal

def print_stack():
    """Easy place to put a simple stack printer"""
    traceback.print_stack()

    
def debug(sig, frame):
    """Interrupt running process, and provide a python prompt for
    interactive debugging."""
    d={'_frame':frame}         # Allow access to frame object.
    d.update(frame.f_globals)  # Unless shadowed by global
    d.update(frame.f_locals)

    i = code.InteractiveConsole(d)
    message  = "Signal recieved : entering python shell.\nTraceback:\n"
    message += ''.join(traceback.format_stack(frame))
    i.interact(message)

def listen():
    signal.signal(signal.SIGUSR1, debug)  # Register handler

    
