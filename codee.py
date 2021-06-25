# -*- coding: utf-8 -*-

import random
import copy
import math
import heapq
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.gridspec as gridspec
import networkx as nx
import numpy as np
from moviepy.editor import VideoClip
import sys
import os

GREY = (0.58, 0.58, 0.58) #(0.8, 0.8, 0.8, 1)   uninfected 
YELLOW = (1, 1, 0) #(1, 0.49, 0.31)    exposed
RED = (0.96, 0.15, 0.15) #(1, 0, 0, 1)    infected
CYAN = (0, 0.84, 0.84)#(0.48, 0.4, 0.93)  quarantined 
GREEN = (0, 0.86, 0.03) #(0, 0.5, 0.5, 1)   recovered
BLACK = (0, 0, 0)          # dead


class simpleNetworkSEIQRModel():
    def __init__(self, beta, epsilon, tau, rho, omega, kappa, sigma, S , E , I , Q , R ):       
        # parameters of the model
        self.beta = beta
        self.epsilon = epsilon
        self.tau = tau
        self.rho = rho
        self.omega = omega
        self.kappa = kappa
        self.sigma = sigma
        self.t = 0
        self.N = S + E + I + Q + R
        self.graph = nx.barabasi_albert_graph(self.N, 5)
        self.adjacencyList = []
        for i in self.graph.nodes:
            self.adjacencyList.append(list(self.graph.neighbors(i)))
            
        ## saving the list of neighbors in the output1.csv file
        with open("output1.csv", "wb") as file:      
             #self.graph.write_edgelist(f)
             nx.write_edgelist(self.graph, file)
        with open('output1.csv', 'r') as file :     
             filedata = file.read()
             filedata = filedata.replace(' ', ',')
             filedata = filedata.replace(',{}', '')
        with open('output1.csv', 'w') as file:
            file.write("A,B\n")
            file.write(filedata)
        
        ## initializing the lists    
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
        self.dList = []
 
        self.latencyTimesHeap = []
        self.recoveryTimesHeap = []
        self.infectedTimesHeap = []
        self.deathTimesHeap = []

        self.agentCoordinates = {}
        self.record = []
        self.timeList = []
        self.iRecord = [0]
        self.rRecord = []
        self.dRecord = []
        self.recordList = []
        
        ## creating list of agents
        allAgents = list(range(self.N))   
        random.shuffle(allAgents)
        self.sAgentList = copy.copy(allAgents)
        
        ## setting the color for all agents to grey
        for i in range(self.N):
            self.agentCoordinates[self.sAgentList[i]] = GREY
        
        ## infect some agents at t = 0
        self.indexCases = []
        for i in range(E):
            indexCase = self.sAgentList[0]
            self.indexCases.append(indexCase)
            self.latentAgent(indexCase)
            self.eAgentList.append(indexCase)

        
    ## function for updating the animation      
    def updateScatterPlot(self, i):
        if len(self.record) == 0:
            self.anim.event_source.stop()
        else:    
            ## update animation
            self.scat.set_facecolor(self.record.pop(0))

            ## update texts
            self.day_text.set_text("Day {}".format(self.timeList.pop(0)))
            self.infected_text.set_text("Infected: {}".format(self.iRecord.pop(0)))
            self.recovered_text.set_text("\n\nRecovered: {}".format(self.rRecord.pop(0)))
            self.deaths_text.set_text("\nDeaths: {}".format(self.dRecord.pop(0)))
        return self.scat, self.day_text, self.infected_text, self.recovered_text,
    
     
    ## function to represent the latent period
    def latentAgent(self,agent):
        self.sAgentList.remove(agent)
        self.agentCoordinates.update({agent: YELLOW})
        latencyTime = self.t + self.epsilon # random.choice(self.epsilon)
        heapq.heappush(self.latencyTimesHeap, (latencyTime, agent))
        return 1
    

    ## function to indicate the ending of the latent period
    def endLatent(self):
        latentList = []
        if len(self.latencyTimesHeap) > 0:
            while self.latencyTimesHeap[0][0] <= self.t:
                latentTuple = heapq.heappop(self.latencyTimesHeap)
                latentList.append(latentTuple[1])
                if len(self.latencyTimesHeap) == 0:
                    break 
        return latentList
    
    ## function to handle the posibilities of the infected agent    
    def infectAgent(self, agent, num):
        if num == 1:                            
            infectionTime = self.t + self.rho 
            heapq.heappush(self.infectedTimesHeap, (infectionTime, agent))
        if num == 2:
            recoveryTime = self.t + self.omega  
            heapq.heappush(self.recoveryTimesHeap, (recoveryTime, agent))
        if num == 3:  
            deathTime = self.t + self.kappa
            heapq.heappush(self.deathTimesHeap, (deathTime, agent))

    
    ## function to represent the quarantine period     
    def movingToQ(self):
        infectedList = []
        if len(self.infectedTimesHeap) > 0:
            while self.infectedTimesHeap[0][0] <= self.t:
                infectTuple = heapq.heappop(self.infectedTimesHeap)
                infectedList.append(infectTuple[1])
                if len(self.infectedTimesHeap) == 0:
                    break 
        return infectedList           
    

    ## function to indicate the ending of the quarantine period   
    def quarantinedAgent(self, agent, num):
        if num == 1:
            quarantineTime = self.t + self.tau
            heapq.heappush(self.recoveryTimesHeap, (quarantineTime, agent))
        else:
            deathTime = self.t + self.sigma
            heapq.heappush(self.deathTimesHeap, (deathTime, agent))
       

    ## function for recover state     
    def recoverAgents(self):
        recoverList = []
        if len(self.recoveryTimesHeap) > 0:
            while self.recoveryTimesHeap[0][0] <= self.t:
                recoveryTuple = heapq.heappop(self.recoveryTimesHeap)
                recoverList.append(recoveryTuple[1])
                if len(self.recoveryTimesHeap) == 0:
                    break
        return recoverList
    

    ## function for death state 
    def deadAgents(self):
        deathList = []
        if len(self.deathTimesHeap) > 0:
            while self.deathTimesHeap[0][0] <= self.t:
                deathTuple = heapq.heappop(self.deathTimesHeap)
                deathList.append(deathTuple[1])
                if len(self.deathTimesHeap) == 0:
                    break
        return deathList

    
    ## function for running one simulation
    def run(self):
        while (len(self.eAgentList) > 0 or len(self.iAgentList) > 0 or len(self.qAgentList) > 0):   #modification
            tempEAgentList = []
            infectList = []
            quarantinedList = []         
            recoverFromI = []
            recoverList = []
            deathList = []
            newE = 0

                
            infectList = self.endLatent()
            
            cn = 0
            for infectAgent in infectList:
                self.eAgentList.remove(infectAgent)
                self.iAgentList.append(infectAgent)
                self.agentCoordinates.update({infectAgent: RED})
                cn += 1   
            self.iRecord.append(self.iRecord[-1] + cn)    
        
            
            for iAgent in self.iAgentList:
                for agent in self.adjacencyList[iAgent]:
                    if agent in self.sAgentList:
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
        
            for quarantinedAgent in quarantinedList:
                if quarantinedAgent in self.iAgentList:
                    self.iAgentList.remove(quarantinedAgent)
                    self.qAgentList.append(quarantinedAgent)
                    #cnt3 = cnt3+1  {quarantinedAgent: CYAN}
                    self.agentCoordinates.update({quarantinedAgent: RED})
             
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

            listCoordinates = list(self.agentCoordinates.values())
            self.record.append(listCoordinates)
            
            self.t += 1


            # print('t', self.t, 'numS', len(self.sAgentList),'numE', len(self.eAgentList), 'numI', len(self.iAgentList), 'numQ', len(self.qAgentList), 'numR', len(self.rAgentList), 'numD', len(self.dAgentList))
            line = str(self.t) + '\t' + str(len(self.sAgentList)) + '\t\t' + str(len(self.eAgentList)) + '\t\t' + str(len(self.iAgentList)) + '\t\t' + str(len(self.qAgentList))+ '\t\t' + str(len(self.rAgentList))+ '\t\t' + str(len(self.dAgentList)) + '\n'



            if self.t == 1:
                with open("output2.csv", "w") as f:
                    f.write("t\tnumS\tnumE\tnumI\tnumQ\tnumR\tnumD\n")
                    f.write(line)
            else:
                with open("output2.csv", "a") as f:
                    f.write(line)
                    
            
            maximum = max(len(self.sAgentList), len(self.eAgentList), len(self.iAgentList), len(self.qAgentList), len(self.rAgentList), len(self.dAgentList))
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



            random.shuffle(self.eAgentList)
           
        self.timeList = list(range(1, self.t+1))
        return [self.sList, self.eList, self.iList, self.qList, self.rList, self.dList, self.iRecord]  #, self.latencyTimesHeap


    ## function for saving the simulated data
    def OutputData(self, record):     
        for x in range(len(record[0])):
            line = 't '+ str(x+1)+ '  numS '+ str(record[0][x])+ '  numE '+ str(record[1][x])+ '  numI '+ str(record[2][x])+ '  numQ '+ str(record[3][x])+ '  numR '+ str(record[4][x])+ '  numD '+ str(record[5][x])+ '\n'        
            line2 = str(record[6][x])+ '\n'
            if x == 0:
                with open("output4.csv", "w") as f:
                    f.write(line)
                with open("output5.csv", "w") as f2:
                    f2.write(line2)   
            else:
                with open("output4.csv", "a") as f:
                    f.write(line)
                with open("output5.csv", "a") as f2:
                    f2.write(line2) 

    
    ## function to keep tracking the progress of the animation        
    def progress(self):
        self.done = self.done+1

    ## function for the animation    
    def scatterPlotAnimation(self, record, t):
        self.done = 0
        self.anim = animation.FuncAnimation(fig=self.fig, func=self.updateScatterPlot, interval=1000, save_count=t) # , blit=True
        # # self.anim.save('Animation.gif', writer='imagemagick', fps=30)
        Writer = animation.writers['ffmpeg']
        writer = Writer(fps=2, metadata={'artist': 'Me'}, bitrate=1800)
        self.anim.save('Animation.mp4', writer, progress_callback =lambda i, n: self.progress())  # sys.stdout.write(f'Saving frame {i} of {n}')
        return self.done


    ## function to display the graphs   
    def linePlot(self, record):
        # create plot
        self.fig = plt.figure(figsize=(9, 5.1))
        self.axes = self.fig.add_subplot(projection="polar")
        self.axes.grid(False)
        self.axes.set_xticklabels([])
        self.axes.set_yticklabels([])
        self.axes.set_ylim(0, 1)
        self.figAll = plt.figure(figsize=(6, 3.7))
        self.axes2 = self.figAll.add_subplot()
        plt.xlabel('Time (day)',loc='right' , fontsize=8)
        plt.ylabel('Number of individual',loc='top' , fontsize=8)
        plt.grid(True, which='major', axis='y')
        
        indices = np.arange(0, self.N) + 0.5
        self.xCoordinates = np.pi * (1 + 5**0.5) * indices
        self.yCoordinates = np.sqrt(indices / self.N)
        self.scat = self.axes.scatter(self.xCoordinates, self.yCoordinates, s=5, facecolors=GREY, edgecolors=None)    
        
        # create annotations
        self.day_text = self.axes.annotate("Day", xy=[np.pi / 2, 1], ha="center", va="bottom", color=BLACK)
        self.infected_text = self.axes.annotate("\nInfected: 0", xy=[3 * np.pi / 2, 1], ha="center", va="top", color=RED)
        self.recovered_text = self.axes.annotate("\n\nRecovered: 0", xy=[3 * np.pi / 2, 1], ha="center", va="top", color=GREEN)
        self.deaths_text = self.axes.annotate("\nDeaths: 0", xy=[3 * np.pi / 2, 1], ha="center", va="top", color=BLACK)
        
        t = len(record[0])
        self.axes2.plot(list(range(0, t)), record[0], label="S", c= GREY)
        self.axes2.plot(list(range(0, t)), record[1], label="E", c= YELLOW)
        self.axes2.plot(list(range(0, t)), record[2], label="I", c= RED)
        self.axes2.plot(list(range(0, t)), record[3], label="Q", c= CYAN)
        self.axes2.plot(list(range(0, t)), record[4], label="R", c= GREEN)
        self.axes2.plot(list(range(0, t)), record[5], label="D", c= BLACK)
        self.axes2.legend()
        self.axes2.spines['bottom'].set_color('black')
        self.axes2.spines['left'].set_color('black')
        self.axes2.spines['right'].set_alpha(0)
        self.axes2.spines['top'].set_alpha(0)
        self.axes2.xaxis.label.set_color('black')
        self.axes2.yaxis.label.set_color('black')
        self.axes2.tick_params(axis='x', colors='black')
        self.axes2.tick_params(axis='y', colors='black')
        self.figAll.savefig('All_classes_plot.png', dpi=150, transparent=True)
    
        
    ## function to display the comparison graph 
    def comparisonPlot(self, Data, rcrd):
        self.fig2 = plt.figure(figsize=(6, 3.7))
        self.axes3 = self.fig2.add_subplot()
        plt.xlabel('Time (day)',loc='right' , fontsize=8)
        plt.ylabel('Number of infected',loc='top' , fontsize=8) 
        plt.grid(True, which='major', axis='y')

        self.axes3.plot(rcrd[:45], label="Simulated", c='lightcoral')    
        self.axes3.plot(Data[:45], label="Real data", c='cornflowerblue')
        self.axes3.legend()
        self.axes3.spines['bottom'].set_color('black')
        self.axes3.spines['left'].set_color('black')
        self.axes3.spines['right'].set_alpha(0)
        self.axes3.spines['top'].set_alpha(0)
        self.axes3.xaxis.label.set_color('black')
        self.axes3.yaxis.label.set_color('black')
        self.axes3.tick_params(axis='x', colors='black')
        self.axes3.tick_params(axis='y', colors='black')
        self.fig2.savefig('Two_plot.png', dpi=150, transparent=True)

    

    ## function for running multiple simulation    
    def mainn(self, beta, epsilon, rho, omega, kappa, tau, sigma, S, E, I , Q, R, nSimul):
        emptyRecord = 0
        returnedList = []
        
        nSimulation = nSimul
        print('---------------')
        for i in range(nSimulation):
            print('Simulation : ', i+1)
            myNetworkModel = simpleNetworkSEIQRModel(beta, epsilon, tau, rho, omega, kappa, sigma, S, E, I , Q, R)  #, p, nei
            if i == 0:
                recordList = myNetworkModel.run()
            else:
                networkResults = myNetworkModel.run()
                if len(networkResults[0]) < 30:
                    emptyRecord += 1
                    continue
                for j in range(len(recordList)):
                    if len(recordList[j]) < len(networkResults[j]):
                        dif = len(networkResults[j]) - len(recordList[j])
                        recordList[j].extend([recordList[j][-1]]*dif)
                    else:
                        dif = len(recordList[j]) - len(networkResults[j])
                        networkResults[j].extend([networkResults[j][-1]]*dif)
                    recordList[j] = [recordList[j][y] + networkResults[j][y] for y in range(len(recordList[j]))]      
        print('---------------')
        for j in range(len(recordList)):
            recordList[j][:] = [math.ceil(x / (nSimulation-emptyRecord)) for x in recordList[j]]   
            
        
        myNetworkModel.OutputData(recordList)
        myNetworkModel.linePlot(recordList)
        returnedList = recordList[-1].copy()
        dn = 0
        dn = myNetworkModel.scatterPlotAnimation(recordList,len(returnedList)-1)

        return dn, returnedList, len(returnedList)-1
    
    
    # ♠ • ○ ` § ♪ ☻ → Ø