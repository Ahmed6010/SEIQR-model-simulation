# -*- coding: utf-8 -*-
import igraph
import random
import copy
#import pylab as pl
#import scipy
#from scipy import random
import heapq
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.gridspec as gridspec
import networkx as nx
#→from matplotlib.animation import FuncAnimation
import numpy as np
import pandas as pd
import sys

GREY = (0.58, 0.58, 0.58) #(0.8, 0.8, 0.8, 1)   uninfected 
YELLOW = (1, 1, 0) #(1, 0.49, 0.31)    exposed
RED = (0.96, 0.15, 0.15) #(1, 0, 0, 1)    infected
CYAN = (0, 0.84, 0.84)#(0.48, 0.4, 0.93)  quarantined 
GREEN = (0, 0.86, 0.03) #(0, 0.5, 0.5, 1)   recovered
BLACK = (0, 0, 0)          # dead

"""GREY = (0.78, 0.78, 0.78)  # uninfected
ORANGE = (1, 0.49, 0.31)   # exposed
RED = (0.96, 0.15, 0.15)   # infected
PURPLE = (0.48, 0.4, 0.93) # quarantined 
GREEN = (0.23, 0.7, 0.44)  # recovered
BLACK = (0, 0, 0)          # dead"""
 
#model constructor
class simpleNetworkSEIQRModel():
<<<<<<< HEAD
    def __init__(self, b, e, tau, rho, omega, kappa, sigma, v, S , E , I , Q , R , p , nei):        
        # parameters
=======
    def __init__(self, b  , e ,  g ,rho, omega, kappa, sigma, v, S , E , I , Q , R , p , nei):        
        #parameters
>>>>>>> 3b7b81f0b3c11b3994a54a6be63c526139a04e76
        self.b = b
        self.e = e
        self.tau = tau
        self.rho = rho
        self.omega = omega
        self.kappa = kappa
        self.sigma = sigma
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
        self.dAgentList = [] 
 
        self.sList = []
        self.eList = []
        self.iList = []
        self.qList = []
        self.rList = []
        self.newIList = []
        self.dList = []
 
        self.latencyTimesHeap = []
        self.recoveryTimesHeap = []
        self.infectedTimesHeap = []
        self.deathTimesHeap = []
<<<<<<< HEAD
        self.immunityDifference = [1,2,3,4,5]
        
=======
>>>>>>> 3b7b81f0b3c11b3994a54a6be63c526139a04e76
        self.agentCoordinates = {}
        self.record = []
        self.timeList = []
        self.iRecord = [0]
        self.rRecord = []
        self.dRecord = []
        
        # creating list of agents
        allAgents = list(range(self.N))   
        random.shuffle(allAgents)
        self.sAgentList = copy.copy(allAgents)
        
        # setting the color for all agents to grey
        for i in range(self.N):
            self.agentCoordinates[self.sAgentList[i]] = GREY
        
        # infect some agents at t = 0
        self.indexCases = []
        for i in range(E):
            indexCase = self.sAgentList[0]
            self.indexCases.append(indexCase)
            self.latentAgent(indexCase)
            self.eAgentList.append(indexCase)
        
        # create plot
        self.fig = plt.figure(figsize=(12, 5))
        gs =  gridspec.GridSpec(ncols=2, nrows=1, figure=self.fig)
        self.axes = self.fig.add_subplot(gs[0, 1], projection="polar")
        self.axes.grid(False)
        self.axes.set_xticklabels([])
        self.axes.set_yticklabels([])
        self.axes.set_ylim(0, 1)
        
        self.axes2 = self.fig.add_subplot(gs[0, 0])
        
        indices = np.arange(0, self.N) + 0.5
        self.xCoordinates = np.pi * (1 + 5**0.5) * indices
        self.yCoordinates = np.sqrt(indices / self.N)
        self.scat = self.axes.scatter(self.xCoordinates, self.yCoordinates, s=5, facecolors=GREY, edgecolors=None)    
        
        # create annotations
        self.day_text = self.axes.annotate("Day", xy=[np.pi / 2, 1], ha="center", va="bottom")
        #self.exposed_text = self.axes.annotate("Infected: 0", xy=[3 * np.pi / 2, 1], ha="center", va="top", color=ORANGE)
        self.infected_text = self.axes.annotate("\nInfected: 0", xy=[3 * np.pi / 2, 1], ha="center", va="top", color=RED)
        #self.quarantined_text = self.axes.annotate("\nDeaths: 0", xy=[3 * np.pi / 2, 1], ha="center", va="top", color=CYAN)
        self.recovered_text = self.axes.annotate("\n\nRecovered: 0", xy=[3 * np.pi / 2, 1], ha="center", va="top", color=GREEN)
        self.deaths_text = self.axes.annotate("\nDeaths: 0", xy=[3 * np.pi / 2, 1], ha="center", va="top", color=BLACK)

          
    def updateScatterPlot(self, i):
        if len(self.record) == 0:
            self.anim.event_source.stop()
            print('animation stop')
        else:    
            # update colors
            self.scat.set_facecolor(self.record.pop(0))
            # update text
            self.day_text.set_text("Day {}".format(self.timeList.pop(0)))
            #self.exposed_text.set_text("Exposed: {}".format(self.eRecord.pop(0)))
            self.infected_text.set_text("Infected: {}".format(self.iRecord.pop(0)))
            self.recovered_text.set_text("\n\nRecovered: {}".format(self.rRecord.pop(0)))
            self.deaths_text.set_text("\nDeaths: {}".format(self.dRecord.pop(0)))
<<<<<<< HEAD
            
=======
            #print('1')
>>>>>>> 3b7b81f0b3c11b3994a54a6be63c526139a04e76
        return self.scat, self.day_text, self.infected_text, self.recovered_text,
    
     
   
    def latentAgent(self,agent):
        self.sAgentList.remove(agent)
        self.agentCoordinates.update({agent: YELLOW})
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
        return latentList
    
    def infectAgent(self, agent, num):
        if num == 1:
            infectionTime = self.t + (1/self.rho)
            heapq.heappush(self.infectedTimesHeap, (infectionTime, agent))
        if num == 2:
            recoveryTime = self.t + (1/self.omega)
            heapq.heappush(self.recoveryTimesHeap, (recoveryTime, agent))
        if num == 3:  
            deathTime = self.t + (1/self.kappa)
            heapq.heappush(self.deathTimesHeap, (deathTime, agent))

        
    def movingToQ(self):
        infectedList = []
        if len(self.infectedTimesHeap) > 0:
            while self.infectedTimesHeap[0][0] <= self.t:
                infectTuple = heapq.heappop(self.infectedTimesHeap)
                infectedList.append(infectTuple[1])
                if len(self.infectedTimesHeap) == 0:
                    break 
        return infectedList           
       
    def quarantinedAgent(self, agent, num):
        if num == 1:
<<<<<<< HEAD
            quarantineTime = self.t + (1/self.tau)
=======
            quarantineTime = self.t + (1/self.g)
>>>>>>> 3b7b81f0b3c11b3994a54a6be63c526139a04e76
            heapq.heappush(self.recoveryTimesHeap, (quarantineTime, agent))
        else:
            deathTime = self.t + (1/self.sigma)
            heapq.heappush(self.deathTimesHeap, (deathTime, agent))
<<<<<<< HEAD
=======
        #print(self.recoveryTimesHeap)
        
>>>>>>> 3b7b81f0b3c11b3994a54a6be63c526139a04e76
        
    def recoverAgents(self):
        recoverList = []
        if len(self.recoveryTimesHeap) > 0:
            while self.recoveryTimesHeap[0][0] <= self.t:
                recoveryTuple = heapq.heappop(self.recoveryTimesHeap)
                recoverList.append(recoveryTuple[1])
                if len(self.recoveryTimesHeap) == 0:
                    break
        return recoverList
<<<<<<< HEAD
=======
    
    def deadAgents(self):
        deathList = []
        if len(self.deathTimesHeap) > 0:
            while self.deathTimesHeap[0][0] <= self.t:
                deathTuple = heapq.heappop(self.deathTimesHeap)
                deathList.append(deathTuple[1])
                if len(self.deathTimesHeap) == 0:
                    break
        return deathList
        
    """def startAnim(self):
        self.anim.event_source.start()
>>>>>>> 3b7b81f0b3c11b3994a54a6be63c526139a04e76
    
    def deadAgents(self):
        deathList = []
        if len(self.deathTimesHeap) > 0:
            while self.deathTimesHeap[0][0] <= self.t:
                deathTuple = heapq.heappop(self.deathTimesHeap)
                deathList.append(deathTuple[1])
                if len(self.deathTimesHeap) == 0:
                    break
        return deathList

    
    def run(self):
        while (len(self.eAgentList) > 0 or len(self.iAgentList) > 0 or len(self.qAgentList) > 0):   #modification
            tempEAgentList = []
            infectList = []
            quarantinedList = []         
            recoverFromI = []
            recoverList = []
            deathList = []
<<<<<<< HEAD
=======
            #R_to_S = []
>>>>>>> 3b7b81f0b3c11b3994a54a6be63c526139a04e76
            newE = 0
            
                
            infectList = self.endLatent()
                
            for eAgent in infectList:

                for agent in self.adjacencyList[eAgent]:
                    
                    if agent in self.sAgentList:
                        if (random.random() < self.b):                            
                            newE += self.latentAgent(agent)
                            tempEAgentList.append(agent)
                            
            
            
            for iAgent in self.iAgentList:
                rnd = random.random()
<<<<<<< HEAD
                if rnd < 0.75:        
                    self.infectAgent(iAgent, 1)
=======
                if rnd < 0.75:               
                    #quarantinedList.append(iAgent)
                    self.infectAgent(iAgent, 1)
                    #self.quarantinedAgent(iAgent)
>>>>>>> 3b7b81f0b3c11b3994a54a6be63c526139a04e76
                elif rnd < 0.99:
                    recoverFromI.append(iAgent)
                    self.infectAgent(iAgent, 2)
                else:    
                    self.infectAgent(iAgent, 3)
<<<<<<< HEAD
=======
                    print('rnd 1', rnd)
>>>>>>> 3b7b81f0b3c11b3994a54a6be63c526139a04e76
            
            quarantinedList = self.movingToQ()
            
            for qAgent in self.qAgentList:
                rnd = random.random()
                if rnd < 0.99:
                    self.quarantinedAgent(qAgent, 1)
                else:
                    self.quarantinedAgent(qAgent, 2)
<<<<<<< HEAD
           
=======
                    print('rnd 2', rnd)
            """print(self.t)
            print(tempEAgentList , '\tE')
            print(infectList , '\tI')
            print(quarantinedList , '\tI->Q')
            print(recoverFromI , '\tI->R')"""
>>>>>>> 3b7b81f0b3c11b3994a54a6be63c526139a04e76
            
            cn = 0
            for infectAgent in infectList:
                self.eAgentList.remove(infectAgent)
                self.iAgentList.append(infectAgent)
                self.agentCoordinates.update({infectAgent: RED})
                cn += 1 
            
<<<<<<< HEAD
            self.iRecord.append(self.iRecord[-1] + cn)
            
=======
            self.iRecord.append(self.iRecord[-1] + cn)    
                
            deathList = self.deadAgents()
            
            for deadAgent in deathList:
                if deadAgent in self.iAgentList:    
                    self.iAgentList.remove(deadAgent)
                    self.ddAgentList.append(deadAgent)
                    self.agentCoordinates.update({deadAgent: BLACK})
                if deadAgent in self.qAgentList:
                    self.qAgentList.remove(deadAgent)
                    self.ddAgentList.append(deadAgent)
                    self.agentCoordinates.update({deadAgent: BLACK})
            """ind = self.agentCoordinates.index(infectAgent)
                lst = list(self.agentCoordinates)
                lst[ind] = (lst[ind][0],RED)
                self.agentCoordinates = tuple(lst)"""
                
                
                #print('---',self.agentCoordinates[ind])
                #print('+++',self.agentCoordinates[ind])
                
>>>>>>> 3b7b81f0b3c11b3994a54a6be63c526139a04e76
                
            deathList = self.deadAgents()
            
            for deadAgent in deathList:
                if deadAgent in self.iAgentList:    
                    self.iAgentList.remove(deadAgent)
                    self.dAgentList.append(deadAgent)
                    self.agentCoordinates.update({deadAgent: BLACK})
                if deadAgent in self.qAgentList:
                    self.qAgentList.remove(deadAgent)
                    self.dAgentList.append(deadAgent)
                    self.agentCoordinates.update({deadAgent: BLACK})
            #if self.t == 0:
                #cnt3 = len(self.qAgentList)         
            for quarantinedAgent in quarantinedList:
                if quarantinedAgent in self.iAgentList:
                    self.iAgentList.remove(quarantinedAgent)
                    self.qAgentList.append(quarantinedAgent)
                    #cnt3 = cnt3+1
                    #self.agentCoordinates.update({quarantinedAgent: CYAN})
             
            recoverList = self.recoverAgents()
            
            for recoverAgent in recoverList:
                if recoverAgent in self.qAgentList:   
                    self.qAgentList.remove(recoverAgent)
                    self.rAgentList.append(recoverAgent)
                    self.agentCoordinates.update({recoverAgent: GREEN})
                if recoverAgent in recoverFromI:
                    if recoverAgent in self.iAgentList:
                        self.iAgentList.remove(recoverAgent)
                        self.rAgentList.append(recoverAgent) 
                        self.agentCoordinates.update({recoverAgent: GREEN})
            
<<<<<<< HEAD
=======
            
            
                    
            #recordVar = recordVar + len(self.eAgentList)
            #self.eRecord.append(recordVar)
            #if self.iAgentList[-1]: 
>>>>>>> 3b7b81f0b3c11b3994a54a6be63c526139a04e76
            
            
            self.rRecord.append(len(self.rAgentList))
<<<<<<< HEAD
            self.dRecord.append(len(self.dAgentList))
            
            
=======
            self.dRecord.append(len(self.ddAgentList))
>>>>>>> 3b7b81f0b3c11b3994a54a6be63c526139a04e76
            
            self.eAgentList.extend(tempEAgentList)
            self.sList.append(len(self.sAgentList))
            self.eList.append(len(self.eAgentList))
            self.iList.append(len(self.iAgentList))
            self.qList.append(len(self.qAgentList))
            self.rList.append(len(self.rAgentList))
<<<<<<< HEAD
            self.dList.append(len(self.dAgentList))
=======
            self.dList.append(len(self.ddAgentList))
>>>>>>> 3b7b81f0b3c11b3994a54a6be63c526139a04e76
            self.newIList.append(newE)
 
            
            self.record.append(list(self.agentCoordinates.values()))
            
            #cnt3 = 0
            self.t += 1


<<<<<<< HEAD
            print('t', self.t, 'numS', len(self.sAgentList),'numE', len(self.eAgentList), 'numI', len(self.iAgentList), 'numQ', len(self.qAgentList), 'numR', len(self.rAgentList), 'numD', len(self.dAgentList))
            line = str(self.t) + '\t' + str(len(self.sAgentList)) + '\t\t' + str(len(self.eAgentList)) + '\t\t' + str(len(self.iAgentList)) + '\t\t' + str(len(self.qAgentList))+ '\t\t' + str(len(self.rAgentList))+ '\t\t' + str(len(self.dAgentList)) + '\n'
=======
            print('t', self.t, 'numS', len(self.sAgentList),'numE', len(self.eAgentList), 'numI', len(self.iAgentList), 'numQ', len(self.qAgentList), 'numR', len(self.rAgentList), 'numD', len(self.ddAgentList))
            line = str(self.t) + '\t' + str(len(self.sAgentList)) + '\t\t' + str(len(self.eAgentList)) + '\t\t' + str(len(self.iAgentList)) + '\t\t' + str(len(self.qAgentList))+ '\t\t' + str(len(self.rAgentList))+ '\t\t' + str(len(self.ddAgentList)) + '\n'
>>>>>>> 3b7b81f0b3c11b3994a54a6be63c526139a04e76


            if self.t == 1:
                with open("output2.csv", "w") as f:
                    f.write("t\tnumS\tnumE\tnumI\tnumQ\tnumR\tnumD\n")
                    f.write(line)
            else:
                with open("output2.csv", "a") as f:
                    f.write(line)
                    
            
            maximum = max(len(self.sAgentList), len(self.eAgentList), len(self.iAgentList), len(self.qAgentList), len(self.rAgentList))
            if self.t == 1:
                with open("output3.csv", "w") as f:
                    f.write("t\tnumS\tnumE\tnumI\tnumQ\tnumR\tnumD\n")
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
<<<<<<< HEAD
                    if j >= len(self.dAgentList):  
                        f.write("-\n")
                    else:
                        f.write(str(self.dAgentList[j]) + "\n")
=======
                    if j >= len(self.ddAgentList):  
                        f.write("-\n")
                    else:
                        f.write(str(self.ddAgentList[j]) + "\n")
>>>>>>> 3b7b81f0b3c11b3994a54a6be63c526139a04e76

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
           
            #print("/////////////////////////////////////////////////////////////////////") 
<<<<<<< HEAD
        
=======
        #print('ffffffff',self.iRecord)
        #print(self.rRecord)
>>>>>>> 3b7b81f0b3c11b3994a54a6be63c526139a04e76
        print(sys.getsizeof(self.record)) 
        self.timeList = list(range(0, self.t))
        return [self.sList, self.eList, self.iList, self.qList, self.rList, self.newIList]  #, self.latencyTimesHeap
    
    
    def scatterPlotAnimation(self):
        self.anim = animation.FuncAnimation(fig=self.fig, func=self.updateScatterPlot, interval=1000) # , blit=True
        #self.anim.save('/animation.gif', writer='imagemagick', fps=60)
        #self.anim.save('Animation.gif', writer='imagemagick', fps=30)
        Writer = animation.writers['ffmpeg']
        writer = Writer(fps=2, metadata={'artist': 'Me'}, bitrate=1800)
<<<<<<< HEAD
        #self.anim.save('Animation.mp4', writer)
    
    def linePlot(self):
        self.axes2.plot(self.iRecord, label="Simulated", c= RED)
        exlFile = pd.read_excel('Covid19Data.xlsx',sheet_name='Alger') #, index_col=1
        exlFile = exlFile.dropna()
        exlFile = exlFile.sort_index(ascending=False)
        realData = exlFile['Confirmed'].tolist()
        #print(realData)
        self.axes2.plot(realData[:self.t], label="Real data", c= GREEN)
        #self.axes2.plot(list(range(0, self.t)), self.sList, label="S", c= GREY)
        #self.axes2.plot(list(range(0, self.t)), self.eList, label="E", c= ORANGE)
        #self.axes2.plot(list(range(0, self.t)), self.iList, label="I", c= RED)
        #self.axes2.plot(list(range(0, self.t)), self.qList, label="Q", c= CYAN)
        #self.axes2.plot(list(range(0, self.t)), self.rList, label="R", c= GREEN)
        #self.axes2.plot(list(range(0, self.t)), self.dList, label="D", c= BLACK)
=======

        self.anim.save('Animation.mp4', writer)
    
    def linePlotAnimation(self):
        #self.anim2 = animation.FuncAnimation(fig=self.fig, func=self.updateLinePlot, init_func=self.init,  interval=200, blit=True) # frames=100,
        self.axes2.plot(list(range(0, self.t)), self.sList, label="S", c= GREY)
        self.axes2.plot(list(range(0, self.t)), self.eList, label="E", c= YELLOW)
        self.axes2.plot(list(range(0, self.t)), self.iList, label="I", c= RED)
        self.axes2.plot(list(range(0, self.t)), self.qList, label="Q", c= CYAN)
        self.axes2.plot(list(range(0, self.t)), self.rList, label="R", c= GREEN)
        self.axes2.plot(list(range(0, self.t)), self.dList, label="D", c= BLACK)
>>>>>>> 3b7b81f0b3c11b3994a54a6be63c526139a04e76
        self.axes2.legend()
            
    #def nSimulation(self):    

if __name__=='__main__':
    #paramètres
    b = 0.2
<<<<<<< HEAD
    e = 1/4       # the latent period
    rho = 1/3     # I -> Q rate
    omega = 1/14  # I -> R rate
    kappa = 1/8   # I -> D rate
    tau = 1/15    # Q -> R rate
    sigma = 1/4   # Q -> D rate  
    v = 0.1
    #IFR = 0.2  # infection fatality rate ( the number of deaths from a disease divided by the total number of cases. )
    #condition initiale   
    S = 100
    E = 1
=======
    e = 1/5
    g = 1/15
    rho = 1/3     # I -> Q rate
    omega = 1/14  # I -> R rate
    kappa = 1/8   # I -> D rate 
    sigma = 1/4
    v = 0.1
    #IFR = 0.2  # infection fatality rate ( the number of deaths from a disease divided by the total number of cases. )
    #condition initiale   
    S = 500
    E = 10
>>>>>>> 3b7b81f0b3c11b3994a54a6be63c526139a04e76
    I = 0
    Q = 0
    R = 0
    # network settings
    p = .6
    nei = 4
<<<<<<< HEAD
    myNetworkModel = simpleNetworkSEIQRModel(b, e, tau, rho, omega, kappa, sigma, v, S, E, I ,Q , R , p, nei)
=======
    myNetworkModel = simpleNetworkSEIQRModel(b, e, g, rho, omega, kappa, sigma, v, S, E, I ,Q , R , p, nei)
>>>>>>> 3b7b81f0b3c11b3994a54a6be63c526139a04e76
    
    networkResults = myNetworkModel.run()
    myNetworkModel.linePlot()
    myNetworkModel.scatterPlotAnimation()
    plt.show()
    
    """
    pl.xlabel('temps')
    pl.ylabel('Nbr Infectes')
    
    pl.legend(), loc=(0.9, 0.9)"""