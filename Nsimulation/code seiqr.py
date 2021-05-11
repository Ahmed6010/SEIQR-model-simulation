# -*- coding: utf-8 -*-
import igraph
import random
import copy
import pylab as pl
import scipy
from scipy import random
import heapq
 
#model constructor

    

class simpleNetworkSIRModel():
    def __init__(self, b  , e ,  g ,rho, omega, v, S , E , I , Q , R , p , nei):        
        #parameters
        self.b = b
        self.e = e
        self.g = g
        self.rho = rho
        self.omega = omega
        self.v = v
        self.t = 0
        self.p = p
        self.N = S + E + I + Q + R
        self.graph = igraph.Graph.Watts_Strogatz(1, self.N, nei=nei, p = p)
        self.graph.simplify()
        self.adjacencyList = []
        for i in range(self.N):
            self.adjacencyList.append([])
 
        for edge in self.graph.es: 
            self.adjacencyList[edge.source].append(edge.target) 
            self.adjacencyList[edge.target].append(edge.source) 
        #self.adjacencyList = self.graph.get_adjlist()
        with open("output1.csv", "w") as f:
             self.graph.write_edgelist(f)
        with open('output1.csv', 'r') as file :     
             filedata = file.read()
             filedata = filedata.replace(' ', ',')
        with open('output1.csv', 'w') as file:
            file.write("A,B\n")
            file.write(filedata)
            
        self.sAgentList = []
        self.eAgentList = []
        self.iAgentList = []
        self.qAgentList = []
        self.rAgentList = []
 
    
        self.sList = []
        self.eList = []
        self.iList = []
        self.qList = []
        self.rList = []
        self.newIList = []
       
 
        self.latencyTimesHeap = []
        self.recoveryTimesHeap = []
        self.infectedTimesHeap = []
 
        allAgents = list(range(self.N))   #modification
        random.shuffle(allAgents)
        self.sAgentList = copy.copy(allAgents)
 
        # infecter quelques agents à t = 0
        self.indexCases = []
        for i in range(E):           #modification
            indexCase = self.sAgentList[0]
            self.indexCases.append(indexCase)
            self.latentAgent(indexCase)
            self.eAgentList.append(indexCase)
                                                     #modification
        print('eAgentList1:', self.indexCases) # Doit contenir deux objets
        #print('latencyTimesHeap:', self.latencyTimesHeap) 
        #print('recoveryTimesHeap:', self.recoveryTimesHeap) 
        #print('time :', self.t) 
        
    def latentAgent(self,agent):
        self.sAgentList.remove(agent)
        latencyTime = self.t + (1/self.e)
        heapq.heappush(self.latencyTimesHeap, (latencyTime, agent))
        return 1
    
    def endLatent(self):
        latentList = []
        if len(self.latencyTimesHeap) > 0:
            while self.latencyTimesHeap[0][0] <= self.t:
                latentTuple = heapq.heappop(self.latencyTimesHeap)
                latentList.append(latentTuple[1])
                if len(self.latencyTimesHeap) == 0:
                    break 
        #print(self.latencyTimesHeap)
        return latentList
    
    def infectAgent(self, agent, num):
        if(num == 1):
            infectionTime = self.t + (1/self.rho)
            heapq.heappush(self.infectedTimesHeap, (infectionTime, agent))
        if(num == 2):
            recoveryTime = self.t  + (1/self.omega) #scipy.random.exponential
            heapq.heappush(self.recoveryTimesHeap, (recoveryTime, agent))
        
    def movingToQ(self):
        infectedList = []
        if len(self.infectedTimesHeap) > 0:
            while self.infectedTimesHeap[0][0] <= self.t:
                infectTuple = heapq.heappop(self.infectedTimesHeap)
                infectedList.append(infectTuple[1])
                if len(self.infectedTimesHeap) == 0:
                    break 
        #print(self.infectedTimesHeap)
        return infectedList           
       
    def quarantinedAgent(self, agent):
        quarantineTime = self.t + (1/self.g)
        heapq.heappush(self.recoveryTimesHeap, (quarantineTime, agent))
        #print(self.recoveryTimesHeap)
        
        
    def recoverAgents(self):
        recoverList = []
        #maxHeap = max(len(self.recoveryTimesHeap), len(self.quarantinedTimesHeap))
        if len(self.recoveryTimesHeap) > 0:
            while self.recoveryTimesHeap[0][0] <= self.t:
                #print(self.recoveryTimesHeap[0][0], ' <= ',self.t, '---------++')
                recoveryTuple = heapq.heappop(self.recoveryTimesHeap)
                recoverList.append(recoveryTuple[1])
                if len(self.recoveryTimesHeap) == 0:
                    break
        return recoverList
 
   
    def run(self):
           
        while (len(self.eAgentList) > 0 or len(self.iAgentList) > 0 or len(self.qAgentList) > 0):
            #modification
            
            tempEAgentList = []
            infectList = []
            quarantinedList = []         #added
            recoverFromI = []
            recoverList = []
            R_to_S = []
            newE = 0
            """for eAgent in self.eAgentList:

                for agent in self.adjacencyList[eAgent]:
                    
                    if agent in self.sAgentList:
                        if (random.random() < self.b):                            
                            newE += self.latentAgent(agent)
                            tempEAgentList.append(agent)"""
                
            infectList = self.endLatent()
                
            for eAgent in infectList:

                for agent in self.adjacencyList[eAgent]:
                    
                    if agent in self.sAgentList:
                        if (random.random() < self.b):                            
                            newE += self.latentAgent(agent)
                            tempEAgentList.append(agent)
                            #print("hhhhhhhhhh", agent)
            
            
            for iAgent in self.iAgentList:
                if(random.random() < 0.75):
                    #quarantinedList.append(iAgent)
                    self.infectAgent(iAgent, 1)
                    #self.quarantinedAgent(iAgent)
                else:
                    recoverFromI.append(iAgent)
                    self.infectAgent(iAgent, 2)
            
            quarantinedList = self.movingToQ()
            
            for qAgent in self.qAgentList:
                self.quarantinedAgent(qAgent)
        
            """print(self.t)
            print(tempEAgentList , '\tE')
            print(infectList , '\tI')
            print(quarantinedList , '\tI->Q')
            print(recoverFromI , '\tI->R')"""
            

            for infectAgent in infectList:
                self.eAgentList.remove(infectAgent)
                self.iAgentList.append(infectAgent)
                
            for quarantinedAgent in quarantinedList:
                if quarantinedAgent in self.iAgentList:
                    self.iAgentList.remove(quarantinedAgent)
                    self.qAgentList.append(quarantinedAgent)
                
            """for infectedAgent in recoverFromI:
                self.iAgentList.remove(infectedAgent)
                self.rAgentList.append(infectedAgent)  """
             
            recoverList = self.recoverAgents()
            
            for recoverAgent in recoverList:
                if recoverAgent in self.qAgentList:   
                    self.qAgentList.remove(recoverAgent)
                    self.rAgentList.append(recoverAgent)
                if recoverAgent in recoverFromI:
                    if recoverAgent in self.iAgentList:
                        self.iAgentList.remove(recoverAgent)
                        self.rAgentList.append(recoverAgent) 
            
            
            #print(recoverList , '\tR')
            self.eAgentList.extend(tempEAgentList)
            self.sList.append(len(self.sAgentList))
            self.eList.append(len(self.eAgentList))
            self.iList.append(len(self.iAgentList))
            self.qList.append(len(self.qAgentList))
            self.rList.append(len(self.rAgentList))
            self.newIList.append(newE)
 
            self.t += 1

            """print(self.t)
            print(self.eAgentList , '\tE')
            print(self.iAgentList , '\tI')
            print(self.qAgentList , '\tI->Q')
            print(self.rAgentList , '\tI->R')"""

           #print('t', self.t, 'numS', len(self.sAgentList),'numE', len(self.eAgentList), 'numI', len(self.iAgentList), 'numQ', len(self.qAgentList), 'numR', len(self.rAgentList))
            line = str(self.t) + '\t' + str(len(self.sAgentList)) + '\t\t' + str(len(self.eAgentList)) + '\t\t' + str(len(self.iAgentList)) + '\t\t' + str(len(self.qAgentList))+ '\t\t' + str(len(self.rAgentList)) + '\n'


            if self.t == 1:
                with open("output2.csv", "w") as f:
                    f.write("t\tnumS\tnumE\tnumI\tnumQ\tnumR\n")
                    f.write(line)
            else:
                with open("output2.csv", "a") as f:
                    f.write(line)
                    
            
            maximum = max(len(self.sAgentList), len(self.eAgentList), len(self.iAgentList), len(self.qAgentList), len(self.rAgentList))
            if self.t == 1:
                with open("output3.csv", "w") as f:
                    f.write("t\tnumS\tnumE\tnumI\tnumQ\tnumR\n")
            with open("output3.csv", "a") as f:                     #modification
                for j in range(maximum):
                    f.write(str(self.t) + "\t")
                    if j >= len(self.sAgentList):
                        f.write("-\t\t")
                    else:
                        f.write(str(self.sAgentList[j]) + "\t\t")
                    if j >= len(self.eAgentList):
                        f.write("-\t\t")
                    else:
                        f.write(str(self.eAgentList[j]) + "\t\t")
                    if j >= len(self.iAgentList):
                        f.write("-\t\t")
                    else:
                        f.write(str(self.iAgentList[j]) + "\t\t")
                    if j >= len(self.qAgentList):
                        f.write("-\t\t")
                    else:
                        f.write(str(self.qAgentList[j]) + "\t\t")    
                    if j >= len(self.rAgentList):
                        f.write("-\n")
                    else:
                        f.write(str(self.rAgentList[j]) + "\n")

            """if(len(self.eAgentList) != 0 or len(self.iAgentList) != 0):
                random.shuffle(self.rAgentList)
                for i in range(len(self.rAgentList)):
                    if (random.random() < self.v): 
                        self.sAgentList.append(self.rAgentList[0])   
                        R_to_S.append(self.rAgentList[0])
                        self.rAgentList.pop(0)"""       
                #print(self.rAgentList , '\tR --> S')

            random.shuffle(self.eAgentList)
            #self.allAgents = range(self.N)        modification
            

            
        return [self.sList, self.eList, self.iList, self.qList, self.rList, self.newIList]  #, self.latencyTimesHeap
        print("hi")
        
    
    def graphPlot(self):
        for v in self.graph.vs():
            v['label_size'] = 0


            v['color'] = 'blue'
            if v.index in self.rAgentList or v.index in self.iAgentList:
                v['color'] = 'red'
            if v.index in self.indexCases:
                v['color'] = 'green'



        if self.p <= .05:
            l = self.graph.layout_circle()

        elif len(self.graph.vs) < 500:

            l = self.graph.layout_kamada_kawai()

        else:

            l = self.graph.layout_grid_fruchterman_reingold()
        #igraph.drawing.plot(self.graph, layout = l)      #modification
     
if __name__=='__main__':
    #paramètres
    b = 0.3
    e = 1/5
    g = 1/15
    rho = 1/3  # I -> Q rate
    omega = 1/14  # I -> R rate
    v = 0.2
    #condition initiale  115  9 
    S = 100 # suspect
    E = 5 # exposed
    I = 0 # infected
    Q = 0 # quarantined 
    R = 0 # recovered
    #paramètres du réseau
    p = 0.6
    nei = 3
    kk = 0 # kk for the while 
    d=0 # int get input 
    
    ntimeS=0 # number of times simulated
    incr=0
    networkResultssimu=[],[],[],[],[],[] #declarit list multidemo kda mana malhih 
    q =[],[],[],[],[],[] # to plot 
    d=input('Enter how many time its gonna simulate for you:')
    nyimeS = int(d)         
    while kk < nyimeS : # loop N time // nyimeS time
        myNetworkModel = simpleNetworkSIRModel(b, e, g, rho, omega, v, S, E, I ,Q , R , p, nei)
        networkResults = myNetworkModel.run()
        """if not networkResultssimu[0] : # if this array/tuple first index is empty we add 0 to it
            for x in range (0, len(networkResults)):
                for m in range (0, len(networkResults[x])):
                    networkResultssimu[x].append(0)"""
        
        # i choose just index 0 cause all index have the same size i tested it 
        ####################################################################
        for x in range (0, len (networkResults)):    #size of this array is 6  
            for m in range (0, len (networkResults[x])): # length of this lengff is this size inside the first index and its
                if not networkResultssimu[x] : #
                        networkResultssimu[x].append(networkResults[x][m])    
                if ( len(networkResultssimu[x])>m)==False :
                    #if (networkResultssimu[x][m-1]<networkResults[x][m]):
                        networkResultssimu[x].append(networkResults[x][m]) 
                else:
                    if(kk==0)==False:
                        networkResultssimu[x][m]=( networkResultssimu[x][m] + networkResults[x][m])
        print(networkResultssimu[4])
            
        print("m",kk)
        
        kk+=1
    for x in range(len(networkResultssimu)):
        for m in range(len(networkResultssimu[x])):
             q[x].append(networkResultssimu[x][m] / nyimeS)
    myNetworkModel.graphPlot()
   # length = len(networkResults[4])-1
    #numNetworkCases = networkResults[4][length]
    pl.figure()
    # pour 10000 S / 5 E time is around 100 and 105
    
    #pl.plot(myNetworkModel)
    pl.xlabel('temps')
    pl.ylabel('Nbr Infectes')
    pl.plot(q[0], label = 'S')
    pl.plot(q[1], label = 'E')
    pl.plot(q[2], label = 'I')
    pl.plot(q[3], label = 'Q')
    pl.plot(q[4], label = 'R')
    pl.legend()