import sys
import math
import random as rnd
import queue as q
import matplotlib.pyplot as plt

class Cities(object):
    
    def __init__(self):
        self.names = {}
        self.coord = list()
        
    def getCity(self, idx):
        return self.names[idx]
    
    def getCityCoord(self, idx):
        return self.coord[idx]
    
    def addCity(self, cityName, x, y):
        self.coord.append((x, y))
        self.names[len(self.coord)-1] = cityName
        
    def getCoordinates(self):
        return self.coord
    
    def getRandomSolution(self):
        """
        Generates a random solution to TSP, solution contains the indices of the cities.
        """
        rnd.seed(37)
        solution = list()
        noOfCities = len(self.coord)
        start = rnd.randrange(0, noOfCities)
        solution.append(start)
        while len(solution) != len(self.coord):
            idx = rnd.randrange(0, noOfCities)
            if idx not in solution:
                solution.append(idx)
        solution.append(start)
        return solution
        
    def toString(self):
        """
        Print the cities with their coordinates.
        """
        s = ""
        for idx in range(0, len(self.coord)):
            s += self.getCity(idx) + ", x = " + str(self.coord[idx][0]) + ", y = " + str(self.coord[idx][1]) + "\n"
        print(s)

        
class TSP(object):
    
    def __init__(self,cities):
        self.cities = cities
        self.marked = []
        self.noOfCities = len(cities.getCoordinates())
        for idx in range(0, self.noOfCities):
            self.marked.append(False)
        
#    def areAllCitiesVisited(self):
#        visited = True
#        for idx in range(0, self.noOfCities):
#            if not self.marked[idx]:
#                visited = False
#                break
#        return visited
        
    def greedySolution(self):
        rnd.seed(29)
        startidx = rnd.randint(0, (len(self.cities.getCoordinates())-1))
        self.marked[startidx] = True
        minpq = q.PriorityQueue()
        currentCity = startidx
        solution = []
        solution.append(currentCity)
        totalDistance = 0.0
        while len(solution) != self.noOfCities:
            for idx in range(0, self.noOfCities):
                if not self.marked[idx]:
                    dist = self.getDistance(self.cities.getCityCoord(currentCity), self.cities.getCityCoord(idx))
                    minpq.put((dist, idx))
            item = minpq.get()
            totalDistance += item[0]
            currentCity = item[1]
            solution.append(currentCity)
            self.marked[item[1]] = True
            minpq = q.PriorityQueue()
        solution.append(startidx)
        return totalDistance, solution
    
    def improveSol(self, solution, limit):
        pass
    
    def randomHillClimbingLS(self, limit):
        pass
        
    def getDistance(self, cityA, cityB):
        return (((cityA[0] - cityB[0])**2 + (cityA[1] - cityB[1])**2)**0.5) * 56.9
    
    def showGreedySolution(self):
        totalDistance, solution = self.greedySolution()
        print("Best found distance: %.2f miles\n" % totalDistance)
        s = self.cities.getCity(solution[0])
        for idx in solution[1:]:
            s += " - " + self.cities.getCity(idx)
        print(s)
        self.plotTSP(solution)
        
    def plotTSP(self, solution):
        rndsol = self.cities.getRandomSolution()
        #print(rndsol)
        rndx = [ ]
        rndy = [ ]
        for idx in rndsol:
            city = self.cities.getCityCoord(idx)
            rndx.append(city[0])
            rndy.append(city[1])
        plt.plot(rndx, rndy, "k.-")
        rndx.clear()
        rndy.clear()
        for idx in solution:
            city = self.cities.getCityCoord(idx)
            rndx.append(city[0])
            rndy.append(city[1])
        plt.plot(rndx, rndy, "b.-")
        plt.title("Plot of TSP")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.show()
        

if __name__ == "__main__":
    fname = sys.argv[1]
    cities = Cities()
    fl = open(fname)
    for line in fl:
        alist = line.split(';') 
        for i in range(0,len(alist)):
            alist[i] = alist[i].rstrip('\n')
            alist[i] = alist[i].rstrip(',')
        cities.addCity(alist[0], float(alist[1]), float(alist[2]))
    fl.close()
    #cities.toString()
    tsp = TSP(cities)
    tsp.showGreedySolution()
            







    
