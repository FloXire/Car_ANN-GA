import numpy as np
import theano
import theano.tensor as T
import lasagne

inputNet = np.array([[60,60,60,60,60]])

print(inputNet.shape)

W_init = np.random.normal(0, 1, (5, 10))
b_init = np.random.normal(0, 1, (10,))
print(W_init)
print(b_init)

W_output = np.random.normal(0, 1, (10, 1))
b_output = np.random.normal(0, 1, (1,))


x = T.matrix('x')

l_in = lasagne.layers.InputLayer(((1,5)), name="input_layer", input_var=x)
l_hidden = lasagne.layers.DenseLayer(l_in, 10, name="hidden_layer", nonlinearity=lasagne.nonlinearities.tanh, W=W_init, b=b_init)
l_out = lasagne.layers.DenseLayer(l_hidden, 1, name="output_layer", W=W_output, b=b_output)
y = lasagne.layers.get_output(l_out)

f = theano.function([x], y)

print(f(inputNet))