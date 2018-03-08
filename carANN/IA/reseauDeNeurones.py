import numpy as np
import theano
import theano.tensor as T
import lasagne
import math
from Commun.constantes import Constante

inputNet = np.array([[-60,-60,-60,-60,-60]])

#print(inputNet.shape)

def aNN():

    W_init = np.random.uniform(-0.1, 0.1, (5, 10))
    #b_init = np.random.uniform(-1, 1, (10,))
    #print(W_init)
    #print(b_init)
    
    W_output = np.random.uniform(-0.1, 0.1, (10, 1))
    #b_output = np.random.uniform(-1, 1, (1,))
    
    
    x = T.matrix('x')
    
    l_in = lasagne.layers.InputLayer(((1,5)), name="input_layer", nonlinearity=lasagne.nonlinearities.ScaledTanh(scale_in = math.pi, scale_out = math.pi), input_var=x)
    l_hidden = lasagne.layers.DenseLayer(l_in, 10, name="hidden_layer", nonlinearity=lasagne.nonlinearities.ScaledTanh(scale_in = math.pi, scale_out = math.pi), W=W_init)
    l_out = lasagne.layers.DenseLayer(l_hidden, 1, name="output_layer", nonlinearity=lasagne.nonlinearities.ScaledTanh(scale_in = math.pi, scale_out = math.pi), W=W_output)
    y = lasagne.layers.get_output(l_out)

    f = theano.function([x], y)
    
    return f

#for i in range(100):
#    print(aNN()(inputNet))
    