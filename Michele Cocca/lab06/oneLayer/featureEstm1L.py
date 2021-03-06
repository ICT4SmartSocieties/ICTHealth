import tensorflow as tf
import numpy as np
import scipy.io as scio
import matplotlib.pyplot as plt

#import matrix
mat_file=scio.loadmat('updrs.mat')
data=mat_file.get('updrs')
dimensions=[]
dimensions = np.asmatrix(data).shape #shape of the matrix

data = np.asmatrix(data)
#elimnate coluumn 1 and 4
dimensions=[]
dimensions = np.asmatrix(data).shape #shape of the matrix

#normalize the matrix
means = data.mean(axis=0)
variances = data.var(axis=0)
o = np.ones((dimensions[0],1))
mmeans = o*means
mvars  = o*variances
normData = (data - mmeans)/np.sqrt(mvars)

f05 = normData[:,4]
f07 = normData[:,6]
normData05 = normData07= normData
normData05 = np.delete(normData05, [0,3,4,5], 1)
normData07 = np.delete(normData07, [0,3,4,5,6],1)
dimensions05=[]
dimensions05 = np.asmatrix(normData05).shape #shape of the matrix
dimensions07=[]
dimensions07 = np.asmatrix(normData07).shape #shape of the matrix

def execuction(normData,dimensions, features, name):
    #initial settings
    tf.set_random_seed(1234)
    x=tf.placeholder(tf.float32,[dimensions[0],dimensions[1]])#inputs
    t=tf.placeholder(tf.float32,[dimensions[0],1])#desired outputs
    
    b=tf.Variable(tf.random_normal(shape=[1,1], mean=0.0, stddev=1.0, dtype=tf.float32, name="biases"))
    w=tf.Variable(tf.random_normal(shape=[dimensions[1],1], mean=0.0, stddev=1.0, dtype=tf.float32, name="weights"))
    y=tf.matmul(x,w) + b
    
    cost=tf.reduce_sum(tf.squared_difference(y, t, name="objective_function"))#objective function
    optim=tf.train.GradientDescentOptimizer(2e-5,name="GradientDescent")# use gradient descent in the trainig phase
    optim_op = optim.minimize(cost, var_list=[w,b])# minimize the objective function changing w1,b1,w2,b2
    
    init=tf.initialize_all_variables()
    #--- run the learning machine
    sess = tf.Session()
    sess.run(init)
    for i in range(100000):
        # generate the data
        xval = normData #senza 5
        tval = features
        # train
        train_data={x: xval, t: tval}
        sess.run(optim_op, feed_dict=train_data)

    #print(sess.run(w),sess.run(b))
    
    #predicted vs oringinal
    yval=y.eval(feed_dict=train_data,session=sess)
    plt.plot(features,'r', label='regressand')
    plt.plot(yval,'b', label='regression')
    plt.xlabel('case number')
    plt.grid(which='major', axis='both')
    plt.legend()
    plt.savefig(str(name)+'_predVsOrig.pdf',format='pdf')
    plt.show()
    
    #histogramma errore
    plt.hist(yval-features, label ='differences')
    plt.xlabel('case number')
    plt.ylabel('number of elemenets per case number')
    plt.savefig(str(name)+'_errHist.pdf',format='pdf')
    plt.show()
    
    #differences diagram
    yval=y.eval(feed_dict=train_data,session=sess)
    plt.plot(features-yval ,'r', label='differences')
    plt.grid(which='major', axis='both')
    plt.legend()
    plt.savefig(str(name)+'_diffGraph.pdf',format='pdf')
    plt.show()
    return

execuction(normData05,dimensions05,f05,"f05")
execuction(normData07,dimensions07,f07,"f07")




