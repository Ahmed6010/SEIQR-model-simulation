# -*- coding: utf-8 -*-
#import igraph
import random
import copy
import math
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
from moviepy.editor import VideoClip
import sys
import os

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
    def __init__(self, beta, epsilon, tau, rho, omega, kappa, sigma, S , E , I , Q , R ):    #, p , nei    
        # parameters
        self.beta = beta
        self.epsilon = epsilon
        self.tau = tau
        self.rho = rho
        self.omega = omega
        self.kappa = kappa
        self.sigma = sigma
        self.t = 0
        #self.p = p
        self.N = S + E + I + Q + R
        #self.graph = igraph.Graph.Watts_Strogatz(1, self.N, nei=nei, p = p)
        self.graph = nx.barabasi_albert_graph(self.N, 5)
        #self.graph.simplify()
        self.adjacencyList = []
        for i in self.graph.nodes:
            self.adjacencyList.append(list(self.graph.neighbors(i)))
        """for i in range(self.N):
            self.adjacencyList.append([])
 
        for edge in self.graph.es: 
            self.adjacencyList[edge.source].append(edge.target) 
            self.adjacencyList[edge.target].append(edge.source) """
            
            
        #self.adjacencyList = self.graph.get_adjlist()
        with open("output1.csv", "wb") as file:           # w -> wb
             #self.graph.write_edgelist(f)
             nx.write_edgelist(self.graph, file)
        with open('output1.csv', 'r') as file :     
             filedata = file.read()
             filedata = filedata.replace(' ', ',')
             filedata = filedata.replace(',{}', '')
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
        #self.newIList = []
        self.dList = []
 
        self.latencyTimesHeap = []
        self.recoveryTimesHeap = []
        self.infectedTimesHeap = []
        self.deathTimesHeap = []
        self.immunityDifference = [1,2,3,4,5]   ###
        

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
        
       
        #print(self.eAgentList)
        
          
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
        return self.scat, self.day_text, self.infected_text, self.recovered_text,
    
     
   
    def latentAgent(self,agent):
        self.sAgentList.remove(agent)
        self.agentCoordinates.update({agent: YELLOW})
        latencyTime = self.t + self.epsilon # random.choice(self.epsilon)
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
            infectionTime = self.t + self.rho #random.choice(self.rho)
            heapq.heappush(self.infectedTimesHeap, (infectionTime, agent))
        if num == 2:
            recoveryTime = self.t + self.omega  # random.choice(self.omega)
            heapq.heappush(self.recoveryTimesHeap, (recoveryTime, agent))
        if num == 3:  
            deathTime = self.t + self.kappa
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
            quarantineTime = self.t + self.tau
            heapq.heappush(self.recoveryTimesHeap, (quarantineTime, agent))
        else:
            deathTime = self.t + self.sigma
            heapq.heappush(self.deathTimesHeap, (deathTime, agent))
        
    def recoverAgents(self):
        recoverList = []
        if len(self.recoveryTimesHeap) > 0:
            while self.recoveryTimesHeap[0][0] <= self.t:
                recoveryTuple = heapq.heappop(self.recoveryTimesHeap)
                recoverList.append(recoveryTuple[1])
                if len(self.recoveryTimesHeap) == 0:
                    break
        return recoverList
    
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
            newE = 0
            #if self.t==90:
            #    self.beta= 0.16
                
            infectList = self.endLatent()
                
            """for eAgent in infectList:

                for agent in self.adjacencyList[eAgent]:
                    
                    if agent in self.sAgentList:
                        #if random.choice([0,1,2,3]):
                        if (random.random() < self.beta):                            
                            newE += self.latentAgent(agent)
                            tempEAgentList.append(agent)
                        """"""else:
                            print('break')
                            continue"""
            
            cn = 0
            for infectAgent in infectList:
                self.eAgentList.remove(infectAgent)
                self.iAgentList.append(infectAgent)
                self.agentCoordinates.update({infectAgent: RED})
                cn += 1 
            # if len(self.iAgentList) != 0 and len(self.eAgentList) != 0:   
            #     self.iRecord.append(self.iRecord[-1] + cn)
            #if cn != 0:   
            self.iRecord.append(self.iRecord[-1] + cn)    
            
            
            for iAgent in self.iAgentList:
                for agent in self.adjacencyList[iAgent]:
                    if agent in self.sAgentList:
                        #if random.choice([0,1,2]):
                        if (round(random.random(), 3) < self.beta):                            
                            newE += self.latentAgent(agent)
                            tempEAgentList.append(agent)          
                            
                rnd = round(random.random(), 2)
                if rnd < 0.75:        
                    self.infectAgent(iAgent, 1)
                elif rnd < 0.99:
                    recoverFromI.append(iAgent)
                    self.infectAgent(iAgent, 2)
                else:    
                    self.infectAgent(iAgent, 3)
            
            tempEAgentList = list( dict.fromkeys(tempEAgentList) )        
            
            quarantinedList = self.movingToQ()
            
            for qAgent in self.qAgentList:
                rnd = round(random.random(), 2)
                if rnd < 0.99:
                    self.quarantinedAgent(qAgent, 1)
                else:
                    self.quarantinedAgent(qAgent, 2)
            
            
                
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

            
            
            self.rRecord.append(len(self.rAgentList))
            self.dRecord.append(len(self.dAgentList))

            
            self.eAgentList.extend(tempEAgentList)
            self.sList.append(len(self.sAgentList))
            self.eList.append(len(self.eAgentList))
            self.iList.append(len(self.iAgentList))
            self.qList.append(len(self.qAgentList))
            self.rList.append(len(self.rAgentList))
            self.dList.append(len(self.dAgentList))

            #self.newIList.append(newE)
 
            
            self.record.append(list(self.agentCoordinates.values()))
            
            #cnt3 = 0
            self.t += 1


            print('t', self.t, 'numS', len(self.sAgentList),'numE', len(self.eAgentList), 'numI', len(self.iAgentList), 'numQ', len(self.qAgentList), 'numR', len(self.rAgentList), 'numD', len(self.dAgentList))
            line = str(self.t) + '\t' + str(len(self.sAgentList)) + '\t\t' + str(len(self.eAgentList)) + '\t\t' + str(len(self.iAgentList)) + '\t\t' + str(len(self.qAgentList))+ '\t\t' + str(len(self.rAgentList))+ '\t\t' + str(len(self.dAgentList)) + '\n'



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
                    if j >= len(self.dAgentList):  
                        f.write("-\n")
                    else:
                        f.write(str(self.dAgentList[j]) + "\n")


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
        #print(self.iRecord)    
        
        self.timeList = list(range(0, self.t))
        print('len ( timeList ) ', len(self.timeList))
        return [self.sList, self.eList, self.iList, self.qList, self.rList, self.dList, self.iRecord]  #, self.latencyTimesHeap
        #return self.iRecord
        
    def progress(self):
        # done = 0
        # if i==n:
        # print('hii ',self.done) 
        self.done = self.done+1

    def scatterPlotAnimation(self):
        # qq = os.remove("Animation.mp4")
        # print('qq',qq)
        # os.chmod("Animation.mp4" , 0o777)
        self.done = 0
        self.anim = animation.FuncAnimation(fig=self.fig, func=self.updateScatterPlot, interval=1000) # , blit=True
        # self.anim.save('Animation.gif', writer='imagemagick', fps=30)
        Writer = animation.writers['ffmpeg']
        writer = Writer(fps=2, metadata={'artist': 'Me'}, bitrate=1800)
        self.anim.save('Animation.mp4', writer, progress_callback =lambda i, n: self.progress())  # sys.stdout.write(f'Saving frame {i} of {n}')
        # print('done', self.done)
        return self.done

    def linePlot(self, record):
        # create plot
        self.fig = plt.figure(figsize=(7, 4))
        #`gs =  gridspec.GridSpec(ncols=2, nrows=1, figure=self.fig)
        #self.axes = self.fig.add_subplot(gs[0, 1], projection="polar")
        self.axes = self.fig.add_subplot(projection="polar")
        self.axes.grid(False)
        self.axes.set_xticklabels([])
        self.axes.set_yticklabels([])
        self.axes.set_ylim(0, 1)
        self.figAll = plt.figure(figsize=(9, 6))
        # self.axes2 = self.fig.add_subplot(gs[0, 0])
        self.axes2 = self.figAll.add_subplot()
        
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
        self.fig2 = plt.figure(figsize=(10, 6))
        self.axes3 = self.fig2.add_subplot()
        plt.xlabel('Time (day)')
        plt.ylabel('Number of infected')
        
        plt.grid(True, which='major', axis='y')
        self.axes3.plot(record[6], label="Simulated", c='lightcoral')
        exlFile = pd.read_excel('Covid19Data.xlsx',sheet_name='Blida') #, index_col=1  
        exlFile = exlFile.dropna()
        exlFile = exlFile.sort_index(ascending=False)
        realData = exlFile['Confirmed'].tolist()
        
        # exlFile2 = pd.read_excel('Covid19Data.xlsx',sheet_name=['Blida', 'Alger', 'Oran']) #, index_col=1  
        # realData2=[]
        # # exlFile2['Blida'] = exlFile2['Blida'].dropna()
        # exlFile2['Alger'] = exlFile2['Alger'].dropna()
        # exlFile2['Oran'] = exlFile2['Oran'].dropna()
        # exlFile2['Blida'] = exlFile2['Blida'].sort_index(ascending=False)
        # exlFile2['Alger'] = exlFile2['Alger'].sort_index(ascending=False)
        # exlFile2['Oran'] = exlFile2['Oran'].sort_index(ascending=False)
        # realData2.append(exlFile2['Blida']['Confirmed'].tolist())
        # realData2.append(exlFile2['Alger']['Confirmed'].tolist())
        # realData2.append(exlFile2['Oran']['Confirmed'].tolist())  #+
        # self.fig3 = plt.figure(figsize=(10, 6))
        # self.axes4 = self.fig3.add_subplot()
        # plt.xlabel('Time (day)')
        # plt.ylabel('Number of infected')
        # plt.grid(True, which='major', axis='y')
        # self.axes4.plot(realData2[0][:75], label="Real data (Blida)", c='cornflowerblue')
        # self.axes4.plot(record[6][:75], label="Simulated", c='lightcoral')
        # self.axes4.legend()
        
        # self.fig4 = plt.figure(figsize=(10, 6))  #+
        # self.axes5 = self.fig4.add_subplot()     #+
        # plt.xlabel('Time (day)')
        # plt.ylabel('Number of infected')
        # plt.grid(True, which='major', axis='y')
        # self.axes5.plot(realData2[1][:75], label="Real data (Alger)", c='cornflowerblue')  #realData2[1][:220]
        # self.axes5.plot(record[6][:75], label="Simulated", c='lightcoral')
        # self.axes5.legend()
        
        # self.fig5 = plt.figure(figsize=(10, 6))  #+
        # self.axes6 = self.fig5.add_subplot()
        # plt.xlabel('Time (day)')
        # plt.ylabel('Number of infected')
        # plt.grid(True, which='major', axis='y')
        # self.axes6.plot(realData2[2][:75], label="Real data (Oran)", c='cornflowerblue')
        # self.axes6.plot(record[6][:75], label="Simulated", c='lightcoral')
        # self.axes6.legend()
        
        
        # tomato  blueviolet  springgreen
        
        #print('real data', realData[:len(record[6])])
        #print('simu', self.iRecord)
        t = len(record[0])
        self.axes3.plot(realData[:len(record[6])], label="Real data (Blida)", c='cornflowerblue')
        self.axes2.plot(list(range(0, t)), record[0], label="S", c= GREY)
        self.axes2.plot(list(range(0, t)), record[1], label="E", c= YELLOW)
        self.axes2.plot(list(range(0, t)), record[2], label="I", c= RED)
        self.axes2.plot(list(range(0, t)), record[3], label="Q", c= CYAN)
        self.axes2.plot(list(range(0, t)), record[4], label="R", c= GREEN)
        self.axes2.plot(list(range(0, t)), record[5], label="D", c= BLACK)
        self.axes2.legend()
        self.axes3.legend()
            
    
    def mainn(self, beta, epsilon, rho, omega, kappa, tau, sigma, S, E, I , Q, R, nSimul):
        #paramètres  0.025, 7, 3, 14, 8, 15, 4, 1000, 5, 
        # beta = 0.025   # transmission rate
        # epsilon = [7] # the latent period    6, 7, 8, 9, 10
        # rho = [3]     # I -> Q rate          1/....
        # omega = [14]   # I -> R rate, 16, 18, 20, 10, 12, 14
        # kappa = 8   # I -> D rate  1/8
        # tau = 15    # Q -> R rate  1/15
        # sigma = 4  # Q -> D rate   1/4
        
        # #IFR = 0.2  # infection fatality rate ( the number of deaths from a disease divided by the total number of cases. )
        # #condition initiale   
        # S = 5000
        #E = 10
        # I = 0
        # Q = 0
        # R = 0
        # network settings
        #p = .6
        #nei = 4
        emptyRecord = 0
        #record = []
        nSimulation = nSimul
        
        for i in range(nSimulation):
            print('Simulation : ', i)
            myNetworkModel = simpleNetworkSEIQRModel(beta, epsilon, tau, rho, omega, kappa, sigma, S, E, I , Q, R)  #, p, nei
            if i == 0:
                record = myNetworkModel.run()
                #print(record)
            else:
                networkResults = myNetworkModel.run()
                if len(networkResults[0]) < 30:
                    emptyRecord += 1
                    continue
                for j in range(len(record)):
                    if len(record[j]) < len(networkResults[j]):
                        dif = len(networkResults[j]) - len(record[j])
                        record[j].extend([record[j][-1]]*dif)
                    else:
                        dif = len(record[j]) - len(networkResults[j])
                        networkResults[j].extend([networkResults[j][-1]]*dif)
                    record[j] = [record[j][y] + networkResults[j][y] for y in range(len(record[j]))]
        #print(record[-1])        
        
        for j in range(len(record)):
            record[j][:] = [math.ceil(x / (nSimulation-emptyRecord)) for x in record[j]]   
            
        #·print(record[-1]) 
        
        #myNetworkModel = simpleNetworkSEIQRModel(beta, epsilon, tau, rho, omega, kappa, sigma, S, E, I ,Q , R )
        #networkResults = myNetworkModel.run()
        myNetworkModel.linePlot(record)
        dn = 0
        dn = myNetworkModel.scatterPlotAnimation()
        # plt.show()
        print('doe', dn)
        return dn
    
# if __name__=='__main__':
    
#     obj = simpleNetworkSEIQRModel(0.025, 7, 3, 14, 8, 15, 4, 2500, 5,0,0,0)
#     obj.mainn(0.025, 7, 3, 14, 8, 15, 4, 2000, 5,0,0,0,2)
    """
    pl.xlabel('temps')
    pl.ylabel('Nbr Infectes')
    
    pl.legend(), loc=(0.9, 0.9)"""
    
    
    # ♠ • ○ `