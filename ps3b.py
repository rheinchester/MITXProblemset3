# Problem Set 3: Simulating the Spread of Disease and Virus Population Dynamics
# %%
import random
import pylab
import numpy as np
''' 
Begin helper code
'''


class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """


'''
End helper code
'''

#
# PROBLEM 1
#


class SimpleVirus(object):

    """
    Representation of a simple virus (does not model drug effects/resistance).
    """

    def __init__(self, maxBirthProb, clearProb):
        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.        
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).
        """
        self.maxBirthProb = self.isProb(maxBirthProb)
        self.clearProb = self.isProb(clearProb)

    def getMaxBirthProb(self):
        """
        Returns the max birth probability.
        """
        return self.maxBirthProb

    def getClearProb(self):
        """
        Returns the clear probability.
        """
        return self.clearProb

    def doesClear(self):
        """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step. 
        returns: True with probability self.getClearProb and otherwise returns
        False.
        """
        if random.random() <= self.getClearProb():
            return True
        else:
            return False

    def isProb(self, num):
        """ makes sure that a probabilistic figure is passed in """
        if num > 1 or num < 0:
            raise ValueError('Not a probability')
        return float(num)

    def reproduce(self, popDensity):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient and
        TreatedPatient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).         

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.         

        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.               
        """

        birthProb = self.maxBirthProb * (1 - popDensity)
        if birthProb == 0:
            raise NoChildException
        else:
            if random.random() <= birthProb:
                return SimpleVirus(self.getMaxBirthProb(), self.getClearProb())


class Patient(object):
    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the maximum virus population for this patient (an integer)
        """
        self.viruses = self.handleInstance(viruses)
        self.maxPop = int(maxPop)

    def handleInstance(self, obj):
        if isinstance(obj, list):
            return obj
        elif isinstance(obj, SimpleVirus):
            return [obj]

    def getViruses(self):
        """
        Returns the viruses in this Patient.
        """
        return self.viruses

    def getMaxPop(self):
        """
        Returns the max population.
        """
        return self.maxPop

    def getTotalPop(self):
        """
        Gets the size of the current total virus population. 
        returns: The total virus population (an integer)
        """
        return len(self.viruses)

    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:

        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.   

        - The current population density is calculated. This population density
          value is used until the next call to update() 

        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.                    

        returns: The total virus population at the end of the update (an
        integer)
        """
        popDensity = self.getTotalPop() / self.getMaxPop()
        for virus in self.getViruses()[:]:
            if virus.doesClear() == True:
                self.viruses.remove(virus)
            try:
                newVirus = virus.reproduce(popDensity)
                if newVirus != None and virus.doesClear() == False:
                    self.viruses.append(newVirus)
            except NoChildException:
                pass
        return len(self.getViruses())


#
# PROBLEM 2

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
        listsMean, i = [], 1
        while i <= 300:
            juliet.update()
            listsMean.append(float(juliet.getTotalPop()))
            i += 1
        return listsMean

    listOfMeans = np.array([buildMeanList() for i in range(numTrials)])
    sumPerTrial = np.sum(listOfMeans, axis=0, keepdims=True)
    overallMean = sumPerTrial/numTrials  # shape = (1, numTrials)
    toPlot = overallMean[0]

    pylab.plot(toPlot, label="SimpleVirus")
    pylab.title("SimpleVirus simulation")
    pylab.xlabel("Time Steps")
    pylab.ylabel("Average Virus Population")
    pylab.legend(loc="best")
    pylab.show()


# %%
# simulationWithoutDrug(1, 10, 1.0, 0.0, 100)

    #
# PROBLEM 3
class ResistantVirus(SimpleVirus):
    """
    Representation of a virus which can have drug resistance.
    """

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
        """
        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)       

        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'srinol':False}, means that this virus
        particle is resistant to neither guttagonol nor srinol.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.
        """
        super().__init__(maxBirthProb, clearProb)
        self.resistances = resistances
        self.mutProb = mutProb

    # def handleInstance(self, obj):
    #     if not isinstance(obj, dict):
    #         resistances = {obj: True}
    #         return resistances
    #     return obj

    def getResistances(self):
        """
        Returns the resistances for this virus.
        """
        return self.resistances

    def getMutProb(self):
        """
        Returns the mutation probability for this virus.
        """
        return self.mutProb

    def isResistantTo(self, drug):
        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in TreatedPatient to determine how many virus
        particles have resistance to a drug.       

        drug: The drug (a string)

        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """

        if drug in self.resistances and self.resistances[drug] == True:
            return True
        else:
            return False

    def willInheritResistance(self):
        """ switch resistance with probability """
        for drug in self.resistances.copy():
            resistant = self.resistances[drug]
            if random.random() <= self.mutProb:
                self.resistances[drug] = not resistant
        return self.resistances

    def reproduce(self, popDensity, activeDrugs=[]):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the TreatedPatient class.

        A virus particle will only reproduce if it is resistant to ALL the drugs
        in the activeDrugs list. For example, if there are 2 drugs in the
        activeDrugs list, and the virus particle is resistant to 1 or no drugs,
        then it will NOT reproduce.

        Hence, if the virus is resistant to all drugs
        in activeDrugs, then the virus reproduces with probability:      

        self.maxBirthProb * (1 - popDensity).                       

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent). The offspring virus
        will have the same maxBirthProb, clearProb, and mutProb as the parent.

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.       

        For example, if a virus particle is resistant to guttagonol but not
        srinol, and self.mutProb is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90%
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        srinol and a 90% chance that the offspring will not be resistant to
        srinol.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population       

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings).

        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.
        """
        for drug in activeDrugs:
            if self.isResistantTo(drug) == False:
                raise NoChildException

        birthProb = self.maxBirthProb * (1 - popDensity)
        if birthProb == 0:
            raise NoChildException
        else:
            self.resistances = self.willInheritResistance()
            if random.random() <= birthProb:
                return ResistantVirus(self.maxBirthProb, self.clearProb, self.resistances, self.mutProb)


class TreatedPatient(Patient):
    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).              

        viruses: The list representing the virus population (a list of
        virus instances)

        maxPop: The  maximum virus population for this patient (an integer)
        """
        super().__init__(viruses, maxPop)
        self.drugs = []

    def addPrescription(self, newDrug):
        """
        Administer a drug to this patient. After a prescription is added, the
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: The list of drugs being administered to a patient is updated
        """
        if newDrug in self.drugs:
            pass
        else:
            self.drugs.append(newDrug)

    def getPrescriptions(self):
        """
        Returns the drugs that are being administered to this patient.

        returns: The list of drug names (strings) being administered to this
        patient.
        """

        return self.drugs

    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in
        drugResist.       

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'srinol'])

        returns: The population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        lists = []
        for virus in self.viruses:
            if self.checkResistance(virus, drugResist) == True:
                lists.append(virus)
        return len(lists)

    def checkResistance(self, virus, lists):
        """ check if all virus is resistant to all drugs. if so, return true """
        if lists == []:
            return False
        for drug in lists:
            try:
                if virus.resistances[drug] == False:
                    return False
            except KeyError:
                return False
        return True

    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:

        - Determine whether each virus particle survives and update the list of
          virus particles accordingly

        - The current population density is calculated. This population density
          value is used until the next call to update().

        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.
          The list of drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces.

        returns: The total virus population at the end of the update (an
        integer)
        """
        popDensity = self.getTotalPop() / self.getMaxPop()
        for i, virus in enumerate(self.getViruses()[:]):
            if virus.doesClear() == True:
                self.viruses.remove(virus)
            try:
                newVirus = virus.reproduce(popDensity, self.drugs)
                if newVirus != None and virus.doesClear() == False:
                    self.viruses.insert(i+1,newVirus)
            except NoChildException:
                pass
        return len(self.getViruses())


#
# PROBLEM 4
#

def simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances,
                       mutProb, numTrials):
    """
    Runs simulations and plots graphs for problem 5.

    For each of numTrials trials, instantiates a patient, runs a simulation for
    150 timesteps, adds guttagonol, and runs the simulation for an additional
    150 timesteps.  At the end plots the average virus population size
    (for both the total virus population and the guttagonol-resistant virus
    population) as a function of time.

    numViruses: number of ResistantVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: maximum clearance probability (a float between 0-1)
    resistances: a dictionary of drugs that each ResistantVirus is resistant to
                 (e.g., {'guttagonol': False})
    mutProb: mutation probability for each ResistantVirus particle
             (a float between 0-1). 
    numTrials: number of simulation runs to execute (an integer)

    """
    def runSim(lists, resistList, patient):
        for i in range(150):
            patient.update()
            lists.append(float(patient.getTotalPop()))
            resistList.append(patient.getResistPop(['guttagonol']))
            i += 1
        return lists, resistList
    popList, resistList = [], []
    viruses = [ResistantVirus(maxBirthProb, clearProb, resistances, mutProb) for i in range(numViruses)]
    juliet = TreatedPatient(viruses, maxPop)
    runSim(popList, resistList, juliet)
    juliet.addPrescription('guttagonol')
    runSim(popList, resistList, juliet)
    
    pylab.plot(popList, label="TotalPop")
    pylab.plot(resistList, label="ResisitantPop")
    pylab.title("Resistant simulation")
    pylab.xlabel("Time Steps")
    pylab.ylabel("Average Virus Population")
    pylab.legend(loc="best")
    pylab.show()


# %%
virus1 = ResistantVirus(1.0, 0.0, {"drug1": True}, 0.0)
virus2 = ResistantVirus(1.0, 0.0, {"drug1": False}, 0.0)
patient = TreatedPatient([virus2, virus1], 10)
patient.addPrescription("drug1")
# i = 0
# lists = []
# while i < 15 :
#     patient.update()
#     lists.append(patient.getTotalPop())
#     i +=1
# print(patient.getResistPop(['drug1']), patient.getTotalPop())

numViruses = 10
maxPop = 1000
maxBirthProb = 0.1
clearProb = 0.05
resistances = {'guttagonol': False}
mutProb = 0.05
numTrials = 10
# %%
simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances, mutProb, numTrials)
# %%

# Total = [2.0, 3.8, 6.6, 11.4, 16.6, 20.6, 21.2, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6,
#          21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6, 21.6]
# Resistant = [1.0, 2.0, 3.2, 6.0, 8.2, 10.0, 10.4, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6,
#              10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6, 10.6]
# # simulationWithDrug(75, 100, .8, 0.1, {"guttagonol": True}, 0.8, 1)
# pylab.plot(Total, label="TotalPop")
# pylab.plot(Resistant, label="ResisitantPop")
# pylab.title("Resistant simulation")
# pylab.xlabel("Time Steps")
# pylab.ylabel("Average Virus Population")
# pylab.legend(loc="best")
# pylab.show()

# #%%
# MyTotal = [77.0, 95.0, 95.0, 99.0, 96.0, 94.0, 99.0, 94.0, 91.0, 95.0, 95.0, 92.0, 98.0, 97.0, 94.0, 95.0, 93.0, 94.0, 95.0, 91.0, 93.0, 95.0, 95.0, 94.0, 92.0, 91.0, 96.0, 100.0, 96.0, 99.0, 97.0, 93.0, 91.0, 91.0, 95.0, 97.0, 99.0, 94.0, 91.0, 90.0, 90.0, 93.0, 93.0, 91.0, 95.0, 97.0, 96.0, 91.0, 96.0, 96.0, 95.0, 95.0, 93.0, 93.0, 97.0, 99.0, 99.0, 100.0, 97.0, 96.0, 99.0, 94.0, 93.0, 99.0, 103.0, 94.0, 95.0, 99.0, 100.0, 97.0, 97.0, 96.0, 99.0, 99.0, 94.0, 92.0, 86.0, 91.0, 96.0, 101.0, 98.0, 95.0, 94.0, 93.0, 99.0, 94.0, 93.0, 93.0, 93.0, 90.0, 86.0, 92.0, 91.0, 95.0, 90.0, 86.0, 86.0, 91.0, 88.0, 93.0, 90.0, 92.0, 93.0, 96.0, 100.0, 95.0, 96.0, 97.0, 94.0, 96.0, 96.0, 100.0, 95.0, 95.0, 95.0, 105.0, 96.0, 97.0, 96.0, 97.0, 93.0, 91.0, 95.0, 96.0, 94.0, 102.0, 98.0, 99.0, 96.0, 96.0, 94.0, 92.0, 97.0, 92.0, 97.0, 92.0, 98.0, 96.0, 90.0, 95.0, 93.0, 102.0, 100.0, 98.0, 104.0, 98.0, 99.0, 89.0,
#            90.0, 96.0, 91.0, 88.0, 84.0, 80.0, 79.0, 78.0, 82.0, 84.0, 86.0, 90.0, 82.0, 86.0, 81.0, 74.0, 72.0, 67.0, 64.0, 61.0, 61.0, 62.0, 65.0, 68.0, 67.0, 71.0, 69.0, 65.0, 60.0, 63.0, 58.0, 60.0, 60.0, 52.0, 49.0, 49.0, 48.0, 44.0, 44.0, 43.0, 42.0, 37.0, 32.0, 31.0, 26.0, 24.0, 23.0, 24.0, 26.0, 23.0, 22.0, 22.0, 21.0, 21.0, 22.0, 21.0, 21.0, 17.0, 19.0, 14.0, 16.0, 15.0, 15.0, 15.0, 15.0, 16.0, 19.0, 19.0, 22.0, 24.0, 25.0, 24.0, 24.0, 23.0, 21.0, 21.0, 20.0, 20.0, 22.0, 25.0, 28.0, 31.0, 36.0, 40.0, 45.0, 50.0, 55.0, 60.0, 59.0, 59.0, 61.0, 59.0, 59.0, 59.0, 56.0, 50.0, 52.0, 49.0, 49.0, 50.0, 48.0, 48.0, 45.0, 41.0, 46.0, 47.0, 46.0, 45.0, 42.0, 39.0, 37.0, 43.0, 42.0, 42.0, 47.0, 51.0, 50.0, 42.0, 44.0, 42.0, 45.0, 46.0, 47.0, 47.0, 50.0, 52.0, 55.0, 50.0, 50.0, 50.0, 49.0, 42.0, 42.0, 42.0, 45.0, 39.0, 39.0, 38.0, 38.0, 39.0, 38.0, 39.0, 39.0, 40.0, 33.0, 34.0, 31.0, 30.0, 29.0, 28.0, 24.0, 25.0]

# MyResistance = [67, 69, 60, 59, 56, 53, 57, 56, 51, 53, 53, 48, 48, 47, 48, 49, 45, 46, 49, 46, 47, 51, 49, 48, 48, 47, 47, 52, 49, 48, 49, 47, 42, 48, 47, 45, 48, 42, 40, 41, 41, 39, 37, 40, 41, 39, 39, 37, 45, 48, 46, 45, 42, 47, 50, 50, 45, 44, 42, 43, 42, 43, 43, 41, 43, 41, 44, 48, 48, 47, 49, 48, 47, 46, 43, 41, 40, 42, 45, 47, 44, 42, 45, 46, 50, 46, 42, 44, 45, 44, 40, 43, 41, 47, 44, 40, 39, 42, 39, 40, 40, 42, 46, 47, 50, 46, 48, 51, 51, 47, 48, 47, 44, 46, 46, 51, 47, 48, 47, 47, 46, 39, 45, 45, 48, 52, 50, 50, 48, 49, 46, 42, 45, 45, 47, 44, 48,
#                 52, 52, 55, 54, 61, 58, 55, 57, 52, 54, 50, 50, 53, 49, 46, 42, 39, 39, 36, 35, 36, 37, 38, 33, 35, 31, 28, 28, 25, 26, 21, 19, 17, 17, 18, 16, 15, 15, 14, 13, 14, 13, 14, 15, 11, 10, 10, 9, 7, 6, 5, 4, 2, 2, 2, 2, 2, 2, 2, 3, 2, 2, 3, 3, 3, 3, 3, 4, 2, 3, 2, 2, 2, 2, 2, 3, 4, 4, 3, 4, 4, 3, 3, 4, 3, 3, 3, 4, 4, 5, 6, 7, 8, 13, 15, 18, 20, 18, 19, 19, 18, 16, 15, 11, 11, 9, 8, 9, 8, 7, 8, 7, 8, 7, 7, 8, 8, 7, 8, 7, 7, 7, 8, 9, 9, 10, 11, 10, 8, 8, 11, 11, 12, 11, 11, 12, 10, 12, 10, 11, 9, 11, 6, 6, 5, 6, 5, 7, 8, 6, 6, 7, 7, 8, 7, 4, 4, 4, 4, 3, 3, 2, 3]

# EdxTotal = [81.0, 93.0, 100.0, 99.0, 96.0, 95.0, 92.0, 91.0, 97.0, 90.0, 95.0, 100.0, 96.0, 88.0, 89.0, 93.0, 94.0, 98.0, 101.0, 97.0, 88.0, 87.0, 88.0, 100.0, 99.0, 96.0, 93.0, 100.0, 97.0, 96.0, 97.0, 98.0, 98.0, 93.0, 98.0, 96.0, 90.0, 103.0, 92.0, 95.0, 99.0, 98.0, 96.0, 99.0, 99.0, 95.0, 100.0, 102.0, 102.0, 98.0, 98.0, 99.0, 90.0, 91.0, 90.0, 92.0, 92.0, 97.0, 97.0, 97.0, 97.0, 95.0, 94.0, 95.0, 93.0, 99.0, 100.0, 93.0, 92.0, 98.0, 103.0, 97.0, 96.0, 98.0, 95.0, 95.0, 99.0, 91.0, 93.0, 95.0, 93.0, 88.0, 95.0, 97.0, 99.0, 99.0, 94.0, 98.0, 98.0, 104.0, 98.0, 95.0, 95.0, 98.0, 94.0, 95.0, 95.0, 98.0, 95.0, 99.0, 94.0, 95.0, 95.0, 100.0, 98.0, 98.0, 100.0, 93.0, 96.0, 100.0, 96.0, 93.0, 93.0, 95.0, 92.0, 88.0, 94.0, 94.0, 92.0, 95.0, 95.0, 94.0, 95.0, 91.0, 98.0, 96.0, 97.0, 100.0, 95.0, 92.0, 93.0, 94.0, 95.0, 91.0, 93.0, 96.0, 90.0, 93.0, 91.0, 92.0, 95.0, 97.0, 102.0, 94.0, 99.0, 96.0, 96.0, 97.0,
#             95.0, 96.0, 89.0, 89.0, 83.0, 77.0, 67.0, 69.0, 70.0, 70.0, 65.0, 61.0, 60.0, 54.0, 50.0, 48.0, 48.0, 46.0, 46.0, 43.0, 42.0, 39.0, 40.0, 43.0, 41.0, 39.0, 34.0, 31.0, 30.0, 27.0, 23.0, 25.0, 25.0, 25.0, 23.0, 22.0, 20.0, 18.0, 20.0, 21.0, 22.0, 22.0, 20.0, 22.0, 25.0, 26.0, 26.0, 27.0, 27.0, 25.0, 23.0, 24.0, 23.0, 24.0, 24.0, 26.0, 26.0, 29.0, 35.0, 36.0, 39.0, 41.0, 43.0, 48.0, 48.0, 53.0, 56.0, 58.0, 57.0, 53.0, 56.0, 58.0, 60.0, 60.0, 58.0, 58.0, 58.0, 54.0, 51.0, 49.0, 46.0, 44.0, 43.0, 42.0, 45.0, 43.0, 41.0, 43.0, 43.0, 43.0, 45.0, 46.0, 46.0, 45.0, 48.0, 49.0, 50.0, 47.0, 47.0, 50.0, 51.0, 51.0, 51.0, 51.0, 54.0, 51.0, 54.0, 55.0, 57.0, 57.0, 62.0, 64.0, 59.0, 59.0, 59.0, 59.0, 57.0, 54.0, 52.0, 51.0, 52.0, 51.0, 51.0, 49.0, 52.0, 49.0, 44.0, 40.0, 38.0, 37.0, 35.0, 36.0, 36.0, 38.0, 35.0, 37.0, 37.0, 34.0, 32.0, 33.0, 31.0, 33.0, 34.0, 33.0, 31.0, 32.0, 32.0, 33.0, 35.0, 37.0, 35.0, 34.0]
# EdxResistance = [73.0, 71.0, 70.0, 66.0, 60.0, 56.0, 53.0, 56.0, 59.0, 52.0, 55.0, 57.0, 53.0, 48.0, 47.0, 47.0, 46.0, 45.0, 45.0, 47.0, 42.0, 44.0, 47.0, 52.0, 54.0, 53.0, 46.0, 45.0, 39.0, 41.0, 42.0, 45.0, 44.0, 41.0, 42.0, 40.0, 35.0, 44.0, 39.0, 45.0, 49.0, 49.0, 48.0, 53.0, 53.0, 49.0, 51.0, 49.0, 49.0, 48.0, 48.0, 52.0, 46.0, 44.0, 44.0, 46.0, 47.0, 45.0, 44.0, 44.0, 43.0, 42.0, 43.0, 46.0, 45.0, 48.0, 48.0, 42.0, 43.0, 49.0, 53.0, 53.0, 50.0, 53.0, 49.0, 44.0, 48.0, 47.0, 48.0, 47.0, 47.0, 47.0, 51.0, 51.0, 54.0, 55.0, 52.0, 50.0, 49.0, 55.0, 55.0, 53.0, 54.0, 51.0, 49.0, 52.0, 55.0, 58.0, 56.0, 56.0, 50.0, 55.0, 53.0, 55.0, 51.0, 51.0, 56.0, 53.0, 53.0, 55.0, 53.0, 54.0, 51.0, 53.0, 52.0, 48.0, 50.0, 52.0, 50.0, 51.0, 47.0, 46.0, 47.0, 47.0, 50.0, 52.0, 55.0, 54.0, 49.0, 45.0, 44.0, 44.0, 43.0, 41.0, 43.0, 46.0, 46.0, 46.0, 44.0, 46.0, 48.0, 48.0,
#                  52.0, 47.0, 49.0, 44.0, 44.0, 46.0, 46.0, 45.0, 39.0, 37.0, 32.0, 27.0, 22.0, 22.0, 21.0, 20.0, 15.0, 14.0, 15.0, 12.0, 8.0, 7.0, 7.0, 7.0, 6.0, 5.0, 5.0, 3.0, 3.0, 3.0, 4.0, 4.0, 3.0, 3.0, 2.0, 1.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 3.0, 4.0, 4.0, 6.0, 7.0, 6.0, 7.0, 6.0, 6.0, 6.0, 6.0, 6.0, 6.0, 6.0, 7.0, 5.0, 7.0, 7.0, 9.0, 9.0, 10.0, 12.0, 14.0, 14.0, 14.0, 13.0, 15.0, 17.0, 18.0, 18.0, 21.0, 21.0, 18.0, 18.0, 15.0, 16.0, 17.0, 16.0, 17.0, 18.0, 16.0, 12.0, 11.0, 8.0, 9.0, 9.0, 9.0, 9.0, 8.0, 7.0, 9.0, 9.0, 11.0, 11.0, 12.0, 11.0, 13.0, 12.0, 11.0, 13.0, 12.0, 13.0, 15.0, 16.0, 14.0, 13.0, 13.0, 13.0, 13.0, 14.0, 16.0, 14.0, 14.0, 14.0, 15.0, 12.0, 13.0, 13.0, 14.0, 14.0, 14.0, 12.0, 10.0, 9.0, 10.0, 11.0, 11.0, 10.0, 7.0, 7.0, 7.0, 7.0, 6.0, 6.0, 6.0, 6.0, 6.0, 5.0, 6.0, 6.0, 6.0, 7.0, 6.0, 6.0, 7.0, 6.0, 6.0, 5.0, 5.0, 6.0, 6.0, 5.0, 6.0, 5.0, 5.0]
# simulationWithDrug(75, 100, .8, 0.1, {"guttagonol": True}, 0.8, 1)

# pylab.plot(MyTotal, label="TotalPop")
# pylab.plot(MyResistance, label="ResisitantPop")
# pylab.title("My Resistant simulation")
# pylab.xlabel("Time Steps")
# pylab.ylabel("Average Virus Population")
# pylab.legend(loc="best")
# pylab.show()

# pylab.plot(EdxTotal, label="TotalPop")
# pylab.plot(EdxResistance, label="ResisitantPop")
# pylab.title("Edx Resistant simulation")
# pylab.xlabel("Time Steps")
# pylab.ylabel("Average Virus Population")
# pylab.legend(loc="best")
# pylab.show()

#%%
import numpy as np
a0 = [1, 2, 3]
a1 = [1, 2, 3]
a2 = [1, 2, 3]
a3 = [1, 2, 3]
a4 = [1, 2, 3]
A = [ a0, a1, a2, a3, a4 ]
newList = []
for i in range(len(A)):
    x = 0
    for j in range(len(A)):
        x += A[i][0]
        newList.append
print (x)