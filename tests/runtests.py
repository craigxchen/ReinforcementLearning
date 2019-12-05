import sys, os
# access to files one directory up
sys.path.append(os.path.abspath(os.path.join("..")))

from VFA_Net import NeuralNetwork
import matplotlib.pyplot as plt
import numpy as np

nn_arq = [
    {"input_dim": 1, "output_dim": 64, "activation": "relu"},
    {"input_dim": 64, "output_dim": 1, "activation": "none"},
]

ALPHA = 1
GAMMA = 1
NUM_TRIALS = 500000
TMAX = 20000
#slope and offset of function to be learnied
AA = 0.7
BB = 0.3

def f_star(x):
    return AA * x + BB

def loss(target, prediction, alpha=1):
    return float((1/(alpha**2))*np.square(target-alpha*prediction))

model = NeuralNetwork(nn_arq, bias=True, double=True, initVar=1, initVarLast=1)


# %%



def sample_train(nsample):
    xtrain = np.random.randn(nsample)
    return xtrain, f_star(xtrain) #xtrain, ytrain


def plot_loss(y):
    fig, ax = plt.subplots()
    label_fontsize = 18

    t = np.arange(0,len(y))
    ax.plot(t[::int(TMAX/50)],y[::int(TMAX/50)])

    ax.set_yscale('log')
    ax.set_xlabel('Trials',fontsize=label_fontsize)
    ax.set_ylabel('Loss',fontsize=label_fontsize)

    plt.grid(True)
    plt.show()
    return

def plot_test(xtest):# xtest is a np.array
    fig, ax = plt.subplots()
    label_fontsize = 18

    #t = np.arange(0,len(y))
    ax.plot(list(xtest),[model.net_forward([x]) for x in xtest])
    ax.plot(list(xtest),list(f_star(xtest)))
    #ax.set_yscale('log')
    ax.set_xlabel('x',fontsize=label_fontsize)
    ax.set_ylabel('yhat',fontsize=label_fontsize)

    plt.grid(True)
    plt.show()
    return

# %% training

def train(xtrain, **kwargs):
    loss_history = []

    for j in range(TMAX):
        grad_values = {}
        losstemp = 0
        for i in range(xtrain.shape[0]):
            if (i+1)%(xtrain.shape[0]/10) == 0:
                print('training samples {}/{}'.format(i+1,xtrain.shape[0]))

            y_hat = model.net_forward(np.array([[xtrain[i]]]))
            y = np.array([[f_star(xtrain[i])]])

            lr = 0.001

            losstemp += loss(y, y_hat, ALPHA)
            #model.net_backward(y, y_hat, ALPHA)

            grad_values[i] = model.net_backward(y, y_hat[0], ALPHA)
            
        model.batch_update_wb(lr,grad_values)
        loss_history.append(losstemp/xtrain.shape[0])

    return loss_history

#model.reset_params()
xtrain,ytrain = sample_train(500)
loss_history = train(xtrain)
plot_loss(loss_history)
plot_test(np.random.randn(50))