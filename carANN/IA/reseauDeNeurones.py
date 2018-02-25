'''
Created on 23 fevr. 2018

@author: flo-1
'''

# Ensure python 3 forward compatibility
from __future__ import print_function

import numpy as np
import matplotlib.pyplot as plt
import theano
# By convention, the tensor submodule is loaded as T
import theano.tensor as T

# The theano.tensor submodule has various primitive symbolic variable types.
# Here, we're defining a scalar (0-d) variable.
# The argument gives the variable its name.
foo = T.scalar('foo')
# Now, we can define another variable bar which is just foo squared.
bar = foo**2
# It will also be a theano variable.
#print(type(bar))
#print(bar.type)
# Using theano's pp (pretty print) function, we see that 
# bar is defined symbolically as the square of foo
#print(theano.pp(bar))

# We can't compute anything with foo and bar yet.
# We need to define a theano function first.
# The first argument of theano.function defines the inputs to the function.
# Note that bar relies on foo, so foo is an input to this function.
# theano.function will compile code for computing values of bar given values of foo
f = theano.function([foo], bar)
#print(f(3))

# Alternatively, in some cases you can use a symbolic variable's eval method.
# This can be more convenient than defining a function.
# The eval method takes a dictionary where the keys are theano variables and the values are values for those variables.
#print(bar.eval({foo: 3}))


# We can also use Python functions to construct Theano variables.
# It seems pedantic here, but can make syntax cleaner for more complicated examples.
def square(x):
    return x**2
bar = square(foo)
print(bar.eval({foo: 3}))


A = T.matrix('A')
x = T.vector('x')
b = T.vector('b')
y = T.dot(A, x) + b
# Note that squaring a matrix is element-wise
z = T.sum(A**2)
# theano.function can compute multiple things at a time
# You can also set default parameter values
# We'll cover theano.config.floatX later
b_default = np.array([0, 0], dtype=theano.config.floatX)
linear_mix = theano.function([A, x, theano.In(b, value=b_default)], [y, z]) #definit un produit matriciel + une somme de matrice et le
# Supplying values for A, x, and b
print(linear_mix(np.array([[1, 2, 3],
                           [4, 5, 6]], dtype=theano.config.floatX), #A
                 np.array([1, 2, 3], dtype=theano.config.floatX), #x
                 np.array([4, 5], dtype=theano.config.floatX))) #b
# Using the default value for b
print(linear_mix(np.array([[1, 2, 3],
                           [4, 5, 6]], dtype=theano.config.floatX), #A
                 np.array([1, 2, 3], dtype=theano.config.floatX))) #x
