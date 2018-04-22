"""module qui sert pour des tests"""

import numpy as np
import theano
import theano.tensor as T
import lasagne
import math
from Commun.constantes import Constante

inputNet = np.array([[-60,-60,-60,-60,-60]])

#regler le pb du type qui va en arrière

"""
#print(4000+(500//(4000**0.1)))
#print(4000+(50//((4000**2)**0.01))-(3990+(50//((3990**2)**0.01))))


score1 = 3500
score2 = 3000

csteBonus = score1*1.5

print(score1+(csteBonus**15/score1**15)*(csteBonus/(1.5*4500)))
print(score2+(csteBonus**15/score2**15)*(csteBonus/(1.5*4500)))

print(score1+(10*score1)/100-((10**2)*score1))
print(score2+(10*score2)/100)

#self.score = self.score+(10*self.score)/100+(constanteBonusScore/self.score)**15

#print(2200+(7000**9/(2200**9)))
#print(2190+(7000**9/(2190**9)))

#(500000//(self.score**0.1))
"""

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
    