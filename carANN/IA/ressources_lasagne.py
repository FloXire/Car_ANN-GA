'''
Created on 5 mars 2018

@author: flo-1
'''


<<<<<<< HEAD
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


>>> x = T.dmatrix('x')
>>> s = 1 / (1 + T.exp(-x))
>>> logistic = theano.function([x], s)
>>> logistic([[0, 1], [-1, -2]])
array([[ 0.5       ,  0.73105858],
       [ 0.26894142,  0.11920292]])


>>> a, b = T.dmatrices('a', 'b')
>>> diff = a - b
>>> abs_diff = abs(diff)
>>> diff_squared = diff**2
>>> f = theano.function([a, b], [diff, abs_diff, diff_squared])

When we use the function f, it returns the three variables (the printing was reformatted for readability):

>>> f([[1, 1], [1, 1]], [[0, 1], [2, 3]])
[array([[ 1.,  0.],
       [-1., -2.]]), array([[ 1.,  0.],
       [ 1.,  2.]]), array([[ 1.,  0.],
       [ 1.,  4.]])]

"""""
variables partagées :
"""""
>>> from theano import shared
>>> state = shared(0)
>>> inc = T.iscalar('inc')
>>> accumulator = function([inc], state, updates=[(state, state+inc)])
This code introduces a few new concepts. The shared function constructs so-called shared variables. 
These are hybrid symbolic and non-symbolic variables whose value may be shared between multiple functions. 
Shared variables can be used in symbolic expressions just like the objects returned by dmatrices(...) 
but they also have an internal value that defines the value taken by this symbolic variable in all the functions that use it. 
It is called a shared variable because its value is shared between many functions. 
The value can be accessed and modified by the .get_value() and .set_value() methods. 
We will come back to this soon.

The other new thing in this code is the updates parameter of function. 
updates must be supplied with a list of pairs of the form (shared-variable, new expression). 
It can also be a dictionary whose keys are shared-variables and values are the new expressions. 
Either way, it means “whenever this function runs, it will replace the .value of each shared variable with the result of the corresponding expression”. 
Above, our accumulator replaces the state‘s value with the sum of the state and the increment amount.

Let’s try it out!

>>> print(state.get_value())
0
>>> accumulator(1)
array(0)
>>> print(state.get_value())
1
>>> accumulator(300)
array(1)
>>> print(state.get_value())
301
It is possible to reset the state. Just use the .set_value() method:

>>> state.set_value(-1)
>>> accumulator(3)
array(-1)
>>> print(state.get_value())
2

As we mentioned above, you can define more than one function to use the same shared variable. These functions can all update the value.

>>> decrementor = function([inc], state, updates=[(state, state-inc)])
>>> decrementor(2)
array(2)
>>> print(state.get_value())
0


lasagne : 

>>> import theano.tensor as T
>>> l_in = lasagne.layers.InputLayer((100, 50))
>>> l_hidden = lasagne.layers.DenseLayer(l_in, num_units=200)
>>> l_out = lasagne.layers.DenseLayer(l_hidden, num_units=10,
...                                   nonlinearity=T.nnet.softmax)

The first layer of the network is an InputLayer, which represents the input. When creating an input layer, you should specify the shape of the input data. 
In this example, the input is a matrix with shape (100, 50), representing a batch of 100 data points, where each data point is a vector of length 50. 
The first dimension of a tensor is usually the batch dimension, following the established Theano and scikit-learn conventions.

The hidden layer of the network is a dense layer with 200 units, taking its input from the input layer. Note that we did not specify the nonlinearity of the hidden layer. 
A layer with rectified linear units will be created by default.

The output layer of the network is a dense layer with 10 units and a softmax nonlinearity, allowing for 10-way classification of the input vectors.

Note also that we did not create any object representing the entire network. Instead, the output layer instance l_out is also used to refer to the entire network in Lasagne.


Pour les poids : différents façn d initialiser voir https://lasagne.readthedocs.io/en/latest/user/layers.html#creating-a-layer

Propagating data through layers
To compute an expression for the output of a single layer given its input, the get_output_for() method can be used. 
To compute the output of a network, you should instead call lasagne.layers.get_output() on it. This will traverse the network graph.

You can call this function with the layer you want to compute the output expression for:

>>> y = lasagne.layers.get_output(l_out)

>>> l = lasagne.layers.DenseLayer(l_in, num_units=100,
...                               W=lasagne.init.Normal(0.01))

Parameter sharing between multiple layers can be achieved by using the same Theano shared variable instance for their parameters. For example:

>>> l1 = lasagne.layers.DenseLayer(l_in, num_units=100)
>>> l2 = lasagne.layers.DenseLayer(l_in, num_units=100, W=l1.W)
These two layers will now share weights (but have separate biases).

Any keyword arguments passed to get_output() are propagated to all layers. This makes it possible to control the behavior of the entire network. 
The main use case for this is the deterministic keyword argument, which disables stochastic behaviour such as dropout when set to True. 
This is useful because """"a deterministic output is desirable at evaluation time."""

>>> y = lasagne.layers.get_output(l_out, deterministic=True) #a quoi ca sert ?

"""The behaviour of the layer depends on the deterministic keyword argument passed to lasagne.layers.get_output(). 
If True, the layer behaves deterministically, and passes on the input unchanged. If False or not specified, dropout (and possibly scaling) is enabled. 
Usually, you would use deterministic=False at train time and deterministic=True at test time."""

In Lasagne, parameters are represented by Theano shared variables. 

Why """Dropout""": Dropout helps prevent weights from converging to identical positions. It does this by randomly turning nodes off when forward propagating. 
It then back-propagates with all the nodes turned on.

Hinton advocates tuning dropout in conjunction with tuning the size of your hidden layer. 
Increase your hidden layer size(s) with dropout turned off until you perfectly fit your data. 
Then, using the same hidden layer size, train with dropout turned on. This should be a nearly optimal configuration. 
Turn off dropout as soon as you re done training and voila! You have a working neural network!


Some layers can have multiple behaviors. For example, a layer implementing dropout should be able to be switched on or off. 
During training, we want it to apply dropout noise to its input and scale up the remaining values, but during evaluation we don’t want it to do anything.
=======
f = theano.function([x], y)

print(f(inputNet))
>>>>>>> branch 'master' of https://github.com/FloXire/TIPE_ANN.git
