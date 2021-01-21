import os
from inspect import getframeinfo, stack, currentframe


def debug_print(message=""):
	'''
	How to use:
	debug_print("price={}".format(price))
	debug_print("type(price)={}".format(type(price)))
	debug_print("self.prices.shape={}".format(self.prices.shape))
	'''
	caller = getframeinfo(stack()[1][0])
	if "self" in stack()[1][0].f_locals:
		class_name = stack()[1][0].f_locals["self"].__class__.__name__
	else:
		class_name = "NO_Class"

	method_name = stack()[1][0].f_code.co_name
	file_name   = os.path.basename(caller.filename)
	# this_func   = currentframe().f_code.co_name
	print("dbgp: +{} {} {}.{}() - {}".format(caller.lineno, file_name,
	  class_name, method_name, message))

	return

def debug_print2(message=""):
    '''
    This is dummy to switch off debug printing
    Replace debug_print with debug_print2 to stop printing.
    '''
    return