
#    for virus in self.viruses:
#         if virus.doesClear() == False:
#             popDensity = self.getTotalPop()/self.getMaxPop()
#             # if popDensity> 0:
#             newVirus = virus.reproduce(1-popDensity)
#             viruses.append(newVirus)
#             print(newVirus)
#     return len(self.viruses)
#     if self.viruses == []:
#     return ('Cleany neally!')
# else:
#     popDensity  = self.getTotalPop()/ self.getMaxPop()
#     newList = []
#     for virus in self.getViruses():
#         newList.append(virus)
#         newVirus = virus.reproduce(popDensity)
#         self.viruses = newList
# return len(self.getViruses())

# test area
# def toProb(num):
#     """ convert figure to probability between 0 and 1 """
#     if num == 1 :
#         num = float(1/(1+2.7**(-num)))
#     if num == 0:
#         num = float(1/(1+2.7**(num)))
#     return float(num)
# def isProb(num):
#     if num>1 or num< 0 :
#         raise ValueError('Not a probability')
#     return float(num)

#   try:
#         newVirus = virus.reproduce(popDensity)
#         print(newVirus)
#     except NoChildException:
#         newVirus = None
#         print(newVirus)
#     newList.append(newList)


#               newList = []
#             if virus.doesClear() == False:
#                 popDensity = self.getTotalPop()/ self.getMaxPop()
#                 newVirus = virus.reproduce(popDensity)
#                 print(newVirus)

# popDensity = self.getTotalPop() / self.getMaxPop()
# for virus in self.getViruses():
#     try:
#         updateList = []
#         newVirus = virus.reproduce(popDensity)
#         if newVirus != None and virus.doesClear() == False:
#             updateList.append(newVirus)
#     except NoChildException:
#         break
# if updateList != []:
#     self.viruses = self.getViruses() + updateList
# return len(self.getViruses())


popList = []
virusList = []
aveList = []
for i in range(numViruses):
    virus = SimpleVirus(maxBirthProb, clearProb)
    virusList.append(virus)
for j in range(numTrials):
    juliet = Patient(virusList, maxPop)
    num = 0
    totPop = 0
    # while num <= 300:
    print(juliet.update())
    print(totPop)
    num += 1


# ?????????????????????????? This might be the real mean list of 4.99 stuff

#   viruses = buildVirus(numViruses)
#     juliet = Patient(viruses, maxPop)
#     meanList = []
#     for i in range(numTrials):
#         i = 0
#         aveList = []
#         while i <= 300:
#             population = juliet.update()
#             i += 1
#         aveList.append(population)
#         # mean = sum(aveList)/numTrials
#         mean = sum(aveList)/numTrials
#         print(mean)
#         # print(mean)
#         meanList.append(mean)
#     print(meanList)


# ######################################### former stuff
    # def buildVirus(numViruses):
    #     virusList = []
    #     for i in range(numViruses):
    #         virus = SimpleVirus(maxBirthProb, clearProb)
    #         virusList.append(virus)
    #     return virusList

    # viruses = buildVirus(numViruses)
    # juliet = Patient(viruses, maxPop)
    # meanList = []
    # for i in range(numTrials):
    #     i = 0
    #     aveList = []
    #     while i <= 300:
    #         population = juliet.update()
    #         aveList.append(population)
    #         i += 1
    #     mean = sum(aveList)/300
    #     print(mean)
    #     meanList.append(mean)
    # print(meanList)

    virus = SimpleVirus(maxBirthProb, clearProb)
    viruses = np.array([virus for i in range(numViruses)])
    juliet = Patient(viruses, maxPop)
    i = 0
    aveList = []
    while i <= 300:
        population = juliet.update()
        aveList.append(population)
        i += 1
    meanList = np.array([sum(aveList)/300 for i in range(numTrials)])
    print(meanList)

# Third trial
    # for i in range(numTrials):
    #     i = 0
    #     aveList = []
    #     while i <= 300:
    #         population = juliet.update()
    #         aveList.append(population)
    #         meanPerTime = population/len(aveList)
    #         # print(meanPerTime)
    #         print(aveList)
    #         i += 1
    #     return
    #     mean = sum(aveList)/numTrials
    #     # print(mean)
    #     meanList.append(mean)

    # def buildVirus(numViruses):
    #     virusList = []
    #     for i in range(numViruses):
    #         virus = SimpleVirus(maxBirthProb, clearProb)
    #         virusList.append(virus)
    #     return virusList

    # overallMean = []
    # for j in range(numTrials):
    #     meanList = []
    #     viruses = buildVirus(numViruses)
    #     juliet = Patient(viruses, maxPop)
    #     i = 0
    #     aveList = []
    #     totMean = []
    #     while i <= 300:
    #         aveList.append(juliet.update())
    #         meanPerTimeStep = sum(aveList)/len(aveList)
    #         meanList.append(meanPerTimeStep)
    #         i += 1
    #     while j <= 1:
    #         pylab.plot(meanList, label="SimpleVirus")
    #         pylab.title("SimpleVirus simulation")
    #         pylab.xlabel("Time Steps")
    #         pylab.ylabel("Average Virus Population")
    #         pylab.legend(loc="best")
    #         pylab.show()
    #         return
    # meanPerTrial = sum(aveList)/numTrials
    # meanList.append(meanPerTrial)

    # overallMean = []
    # for j in range(numTrials):
    #     meanList = []
    #     viruses = buildVirus(numViruses)
    #     juliet = Patient(viruses, maxPop)
    #     i = 0
    #     aveList = []
    #     totList = []
    #     while i <= 300:
    #         aveList.append(juliet.update())
    #         meanPerTimeStep = sum(aveList)/len(aveList)
    #         meanList.append(meanPerTimeStep)
    #         i += 1
    #     # totList.append(meanList)
    #     # print(len(totList))
    #     # print(meanList)
    #     while j <= 1:
    #         pylab.plot(meanList, label="SimpleVirus")
    #         pylab.title("SimpleVirus simulation")
    #         pylab.xlabel("Time Steps")
    #         pylab.ylabel("Average Virus Population")
    #         pylab.legend(loc="best")
    #         pylab.show()
    #         return


    # def meanList(num):
    #     aveList, i = [], 0
    #     mean = []
    #     for i in range(num):
    #         print(sum(aveList))
    #         aveList.append(juliet.update())
    #         meanPerTimeStep = sum(aveList)/len(aveList)
    #         mean.append(meanPerTimeStep)
    #     return mean
    # print(meanList(300))


#
def simulationWithoutDrug(numViruses, maxPop, maxBirthProb, clearProb,
                          numTrials):
    """
    Run the simulation and plot the graph for problem 3 (no drugs are used,
    viruses do not have any drug resistance).    
    For each of numTrials trial, instantiates a patient, runs a simulation
    for 300 timesteps, and plots the average virus population size as a
    function of time.

    numViruses: number of SimpleVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: Maximum clearance probability (a float between 0-1)
    numTrials: number of simulation runs to execute (an integer)
    """
    def buildMeanList():
        viruses = [SimpleVirus(maxBirthProb, clearProb)
                   for i in range(numViruses)]
        juliet = Patient(viruses, maxPop)
        i = 1
        totMean = []
        listsMean = []
        while i <= 300:
            juliet.update()
            listsMean.append(float(juliet.getTotalPop()))
            i += 1
        return listsMean

    # print(buildMeanList())
    listOfMeans = np.array([buildMeanList() for i in range(numTrials)])
    sumPerTrial = np.sum(listOfMeans, axis=0, keepdims=True)
    totalMean = sumPerTrial/numTrials
    plotMean = totalMean[0]

    pylab.plot(plotMean, label="SimpleVirus")
    pylab.title("SimpleVirus simulation")
    pylab.xlabel("Time Steps")
    pylab.ylabel("Average Virus Population")
    pylab.legend(loc="best")
    pylab.show()

############################### Testing stuff##################
julius = SimpleVirus(1.0, 0.0)
# # viruses = [julius]
juliet = Patient(julius, 100)
# # julius.reproduce(8)
num = 0

# viruses = [
#     SimpleVirus(0.16, 0.85),
# ]
# P1 = Patient(viruses, 6)

# while num <= juliet.getMaxPop():
#     print(juliet.update())
#     num+=1
# numViruses = 100

maxPop = 1000
maxBirthProb = 0.99
clearProb = 0.1
numViruses = 100
numTrials = 10
# simulationWithoutDrug(numViruses, maxPop, maxBirthProb, clearProb, numTrials)
simulationWithoutDrug(1, 10, 1.0, 0.0, 1)

# lists = [87.0, 51.0, 28.0, 18.0, 11.0, 4.0, 3.0, 2.0, 3.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
#          0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
# pylab.plot(lists, label="SimpleVirus")
# pylab.title("SimpleVirus simulation")
# pylab.xlabel("Time Steps")
# pylab.ylabel("Average Virus Population")
# pylab.legend(loc="best")
# pylab.show()
