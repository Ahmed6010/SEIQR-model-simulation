# -*- coding: utf-8 -*-
import igraph
import random
import copy
import pylab as pl
import scipy
from scipy import random
import heapq
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.gridspec as gridspec
#→from matplotlib.animation import FuncAnimation
import numpy as np
import sys

GREY = (0.58, 0.58, 0.58) #(0.8, 0.8, 0.8, 1)   uninfected 
ORANGE = (1, 0.38, 0) #(1, 0.49, 0.31)    exposed
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
        self.ndAgentList = [] # nd -> Natural death
        self.ddAgentList = [] # dd -> disease death
 
        self.sList = []
        self.eList = []
        self.iList = []
        self.qList = []
        self.rList = []
        self.newIList = []
 
        self.latencyTimesHeap = []
        self.recoveryTimesHeap = []
        self.infectedTimesHeap = []
        self.agentCoordinates = {}
        self.record = []
        self.timeList = []
        self.eRecord = []
        self.iRecord = [0]
        self.rRecord = []
        
 
        allAgents = list(range(self.N))   #modification
        random.shuffle(allAgents)
        self.sAgentList = copy.copy(allAgents)
        
        for i in range(self.N):
            #self.agentCoordinates.update({self.sAgentList[i]: 'GREY'})
            self.agentCoordinates[self.sAgentList[i]] = GREY
        
        # infecter quelques agents à t = 0
        self.indexCases = []
        for i in range(E):
            indexCase = self.sAgentList[0]
            self.indexCases.append(indexCase)
            self.latentAgent(indexCase)
            self.eAgentList.append(indexCase)
                                                     #modification
        print('eAgentList1:', self.indexCases) # Doit contenir deux objets
        #print('latencyTimesHeap:', self.latencyTimesHeap) 
        #print('recoveryTimesHeap:', self.recoveryTimesHeap) 
        #print('time :', self.t) 
        
         # create plot
        self.fig = plt.figure(figsize=(12, 5))
        gs =  gridspec.GridSpec(ncols=2, nrows=1, figure=self.fig)
        self.axes = self.fig.add_subplot(gs[0, 1], projection="polar")
        self.axes.grid(False)
        self.axes.set_xticklabels([])
        self.axes.set_yticklabels([])
        self.axes.set_ylim(0, 1)
        
        #xy = np.zeros(0)
        self.axes2 = self.fig.add_subplot(gs[0, 0])
        #self.axes2.set_xlim(0)
        #self.axes2.set_ylim(0)
        
        
        indices = np.arange(0, self.N) + 0.5
        self.xCoordinates = np.pi * (1 + 5**0.5) * indices
        self.yCoordinates = np.sqrt(indices / self.N)
        self.scat = self.axes.scatter(self.xCoordinates, self.yCoordinates, s=5, facecolors=GREY, edgecolors=None)    
        
        self.day_text = self.axes.annotate("Day", xy=[np.pi / 2, 1], ha="center", va="bottom")
        #self.exposed_text = self.axes.annotate("Infected: 0", xy=[3 * np.pi / 2, 1], ha="center", va="top", color=ORANGE)
        self.infected_text = self.axes.annotate("\nInfected: 0", xy=[3 * np.pi / 2, 1], ha="center", va="top", color=RED)
        #self.quarantined_text = self.axes.annotate("\nDeaths: 0", xy=[3 * np.pi / 2, 1], ha="center", va="top", color=CYAN)
        self.recovered_text = self.axes.annotate("\n\nRecovered: 0", xy=[3 * np.pi / 2, 1], ha="center", va="top", color=GREEN)
        self.deaths_text = self.axes.annotate("\nDeaths: 0", xy=[3 * np.pi / 2, 1], ha="center", va="top", color=BLACK)
        # create annotations
        """self.day_text = self.axes.annotate("Day", xy=[np.pi / 2, 1], ha="center", va="bottom")
        self.exposed_text = self.axes.annotate("Exposed: 0", xy=[3 * np.pi / 2, 1], ha="center", va="top", color=ORANGE)
        self.infected_text = self.axes.annotate("\nInfected: 0", xy=[3 * np.pi / 2, 1], ha="center", va="top", color=RED)
        #self.quarantined_text = self.axes.annotate("\nDeaths: 0", xy=[3 * np.pi / 2, 1], ha="center", va="top", color=CYAN)
        self.recovered_text = self.axes.annotate("\nRecovered: 0", xy=[3 * np.pi / 2, 1], ha="center", va="top", color=GREEN)
        self.deaths_text = self.axes.annotate("\n\nDeaths: 0", xy=[3 * np.pi / 2, 1], ha="center", va="top", color=BLACK)
        #self.day_text.set_animated(True)"""
        #self.infected_text.set_animated(True)
       
        
    """def init(self):     
        indices = np.arange(0, self.N) + 0.5
        self.xCoordinates = np.pi * (1 + 5**0.5) * indices
        self.yCoordinates = np.sqrt(indices / self.N)
        self.scat = self.axes.scatter(self.xCoordinates, self.yCoordinates, s=5, color=GREY)    
        return self.scat,"""
          
    def updateScatterPlot(self, i):
        #print('fl') 
        #templist = list(self.agentCoordinates.values()) #♣ np.array
        if len(self.record) == 0:
            self.anim.event_source.stop()
            print('animation stop')
        else:    
            self.scat.set_facecolor(self.record.pop(0))
            #update_text
            self.day_text.set_text("Day {}".format(self.timeList.pop(0)))
            #self.exposed_text.set_text("Exposed: {}".format(self.eRecord.pop(0)))
            self.infected_text.set_text("Infected: {}".format(self.iRecord.pop(0)))
            self.recovered_text.set_text("\n\nRecovered: {}".format(self.rRecord.pop(0)))
            #print('1')
        return self.scat, self.day_text, self.infected_text, self.recovered_text,
        #templist = list(self.agentCoordinates.values()) #♣ np.array  networkResults
        #self.axes.scatter(self.xCoordinates, self.yCoordinates, s=5, color=np.array(templist))
        
        #self.scat.set_edgecolor(np.array(templist))
        #
        #for idx, val in enumerate(self.agentCoordinates):
            #colr = self.agentCoordinates[val]
            #self.axes.scatter(self.xCoordinates[idx], self.yCoordinates[idx], s=5, color= colr)
           
    
    """def init(self):
        self.pltLine.set_data([], [])
        return (self.pltLine,)
    
    def updateLinePlot(self, i):
        if len(self.sListRecord) == 0:
            self.anim2.event_source.stop()
            print('line stop')
        else:
            self.pltLine.set_data(self.ind.pop(0), self.sListRecord.pop(0))
            #print(len(self.ind[0]))
            #print(len(self.sListRecord[0]))
            print('2')
        return (self.pltLine,) """
    
    
    
    def latentAgent(self,agent):
        self.sAgentList.remove(agent)
        self.agentCoordinates.update({agent: ORANGE})
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
            recoveryTime = self.t + (1/self.omega)
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

    """def startAnim(self):
        self.anim.event_source.start()
    
    def stopAnim(self):
        self.anim.event_source.stop()"""
    
    def run(self):
        while (len(self.eAgentList) > 0 or len(self.iAgentList) > 0 or len(self.qAgentList) > 0):   #modification
            tempEAgentList = []
            infectList = []
            quarantinedList = []         #added
            recoverFromI = []
            recoverList = []
            #R_to_S = []
            newE = 0
            
            #if self.t == 1:
                #self.anim.event_source.start()
                #print('hoooooooooooooooo')
            
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
            
            cn = 0
            for infectAgent in infectList:
                self.eAgentList.remove(infectAgent)
                self.iAgentList.append(infectAgent)
                self.agentCoordinates.update({infectAgent: RED})
                cn += 1 
            
            self.iRecord.append(self.iRecord[-1] + cn)    
                
                
            """ind = self.agentCoordinates.index(infectAgent)
                lst = list(self.agentCoordinates)
                lst[ind] = (lst[ind][0],RED)
                self.agentCoordinates = tuple(lst)"""
                
                
                #print('---',self.agentCoordinates[ind])
                #print('+++',self.agentCoordinates[ind])
                
                
            for quarantinedAgent in quarantinedList:
                if quarantinedAgent in self.iAgentList:
                    self.iAgentList.remove(quarantinedAgent)
                    self.qAgentList.append(quarantinedAgent)
                    self.agentCoordinates.update({quarantinedAgent: CYAN})
                
            """for infectedAgent in recoverFromI:
                self.iAgentList.remove(infectedAgent)
                self.rAgentList.append(infectedAgent)  """
             
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
            
            #recordVar = recordVar + len(self.eAgentList)
            #self.eRecord.append(recordVar)
            #if self.iAgentList[-1]: 
            
            
            #♦recordVar3 = recordVar3 + len(self.rAgentList)
            self.rRecord.append(len(self.rAgentList))
            
            
            #print(recoverList , '\tR')
            self.eAgentList.extend(tempEAgentList)
            self.sList.append(len(self.sAgentList))
            self.eList.append(len(self.eAgentList))
            self.iList.append(len(self.iAgentList))
            self.qList.append(len(self.qAgentList))
            self.rList.append(len(self.rAgentList))
            self.newIList.append(newE)
 
            
            #upi = self.updatte() #init_func=self.init,   self.scat-> updatte
            #self.anim = FuncAnimation(fig=self.fig, func=self.updatte(), interval=1000, blit=True) #self.t, repeat=True
            #self.anim.event_source.start()
            #plt.show()
            #self.startAnim()    
               
           
            #templist = list(self.agentCoordinates.values()) #♣ np.array
            #self.scat.set_edgecolor(np.array(templist))
            self.record.append(list(self.agentCoordinates.values()))
            
            
            
            
            #♣print(list(self.agentCoordinates.values()))
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
           
            #print("/////////////////////////////////////////////////////////////////////") 
        print('ffffffff',self.iRecord)
        #print(self.rRecord)
        print(sys.getsizeof(self.record)) 
        self.timeList = list(range(0, self.t))
        return [self.sList, self.eList, self.iList, self.qList, self.rList, self.newIList]  #, self.latencyTimesHeap
    
    
    
    
    def scatterPlotAnimation(self):
        self.anim = animation.FuncAnimation(fig=self.fig, func=self.updateScatterPlot, interval=1000) # , blit=True
        #self.anim.save('/animation.gif', writer='imagemagick', fps=60)
        #self.anim.save('Animation.gif', writer='imagemagick', fps=30)
        Writer = animation.writers['ffmpeg']
        writer = Writer(fps=2, metadata={'artist': 'Me'}, bitrate=1800)

        #self.anim.save('Animation.mp4', writer)
    
    def linePlotAnimation(self):
        #self.anim2 = animation.FuncAnimation(fig=self.fig, func=self.updateLinePlot, init_func=self.init,  interval=200, blit=True) # frames=100,
        self.axes2.plot(list(range(0, self.t)), self.sList, label="S", c= GREY)
        self.axes2.plot(list(range(0, self.t)), self.eList, label="E", c= ORANGE)
        self.axes2.plot(list(range(0, self.t)), self.iList, label="I", c= RED)
        self.axes2.plot(list(range(0, self.t)), self.qList, label="Q", c= CYAN)
        self.axes2.plot(list(range(0, self.t)), self.rList, label="R", c= GREEN)
        self.axes2.legend()
    
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
    b = 0.2
    e = 1/5
    g = 1/15
    rho = 1/3  # I -> Q rate
    omega = 1/14  # I -> R rate
    v = 0.1
    #condition initiale  115  9 
    S = 100
    E = 10
    I = 0
    Q = 0
    R = 0
    #paramètres du réseau
    p = .6
    nei = 4
    myNetworkModel = simpleNetworkSEIQRModel(b, e, g, rho, omega, v, S, E, I ,Q , R , p, nei)
    
    networkResults = myNetworkModel.run()
    myNetworkModel.linePlotAnimation()
    myNetworkModel.scatterPlotAnimation()
    
    #myNetworkModel.startAnim()
    #myNetworkModel.stopAnim()
    myNetworkModel.graphPlot()
    
    plt.show()
    #length = len(networkResults[4])-1
    #numNetworkCases = networkResults[4][length]
    """pl.figure()
    #pl.plot(myNetworkModel)
    pl.xlabel('temps')
    pl.ylabel('Nbr Infectes')
    
    pl.plot(networkResults[0], label = 'S')
    pl.plot(networkResults[1], label = 'E')
    pl.plot(networkResults[2], label = 'I')
    pl.plot(networkResults[3], label = 'Q')
    pl.plot(networkResults[4], label = 'R')
    pl.legend(), loc=(0.9, 0.9)"""