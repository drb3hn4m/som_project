import numpy as np
import time

class SelfOrganizingMap:
    def __init__(self,NetworkShape,MaxIter,alpha=0.1):
        self.NetworkShape = tuple(NetworkShape)
        self.MaxIter = MaxIter
        self.alpha0 = alpha
        self.sigma0 = max(self.NetworkShape)/2
        if max(NetworkShape) == 2:
            raise Exception('value error for lambda \n increase the network shape')
        self.lamda = MaxIter/np.log(self.sigma0)

    def _update_params(self,t):
        sigma = self.sigma0*np.exp(-t/self.lamda)
        alpha = self.alpha0*np.exp(-t/self.lamda)
        return sigma,alpha
    
    def _update_weights(self,W,alpha,theta,Weight2DataPoint_dis):
        return W+alpha*np.expand_dims(theta,axis=2)*Weight2DataPoint_dis
    
    def _find_BMU(self,Weight2DataPoint_dis):
        BMUdis = np.linalg.norm(Weight2DataPoint_dis,ord=2,axis=-1)
        return np.argwhere(BMUdis == BMUdis.min())[0]

    def _calculate_influence(self,BMU_subscript,NetworkSubscripts,sigma):
        ElementWise_dif_subs = (np.expand_dims(BMU_subscript,axis=0)-NetworkSubscripts)
        EucDis = np.linalg.norm(ElementWise_dif_subs,ord=2,axis=-1)
        # print(EucDis[BMU_subscript[0],BMU_subscript[1]])
        return np.exp(-(EucDis**2)/(2*(sigma**2)))

    def _optimize(self,data,W,sigma,alpha,NetworkSubscripts):
        for i in range(data.shape[0]):
            Weight2DataPoint_dis = (np.expand_dims(data[i,:],axis=0)-W)
            BMU_subscript = self._find_BMU(Weight2DataPoint_dis)
            theta = self._calculate_influence(BMU_subscript,NetworkSubscripts,sigma)
            # print(theta[BMU_subscript[0],BMU_subscript[1]])
            W = self._update_weights(W,alpha,theta,Weight2DataPoint_dis)
        return W

    def train(self,InputData):
        print("SOM training in progress ... ")
        start = time.time()
        self.data = InputData
        self.NetworkWeightShape = self.NetworkShape + (self.data.shape[1],)
        self.W = np.random.random(self.NetworkWeightShape)
        _x = np.linspace(0, self.NetworkWeightShape[0]-1,self.NetworkWeightShape[0])
        _y = np.linspace(0, self.NetworkWeightShape[1]-1,self.NetworkWeightShape[1])
        _NetworkSubscripts = np.stack(np.meshgrid(_x,_y,indexing='ij'),axis=2)
        for t in range(self.MaxIter):
            _sigma,_alpha = self._update_params(t)
            self.W = self._optimize(self.data,self.W,_sigma,_alpha,_NetworkSubscripts)
        print(f"Elapsed time for SOM training: {time.time() - start:0.2f} seconds")
        return self.W