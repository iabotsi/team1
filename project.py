import sys
import math
import random as rnd
import queue as q
import matplotlib.pyplot as plt
        

class Cities(object):
    '''
    To store city information, location and name
    '''
    
    def __init__(self):
        self.names = []
        self.coord = []
        
    def getCity(self, idx):
        return self.names[idx]
    
    def getCityCoord(self, idx):
        return self.coord[idx]
    
    def addCity(self, cityName, x, y):
        self.coord.append((x, y))
        self.names.append(cityName)
        
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
        self.distance = []          #to store the distances between two cities
        for idx in range(0, self.noOfCities):   #to see if the city has been visited
            self.marked.append(False)
        self.setDistance()

    def getDistance(self, cityA, cityB):
        return (((cityA[0] - cityB[0])**2 + (cityA[1] - cityB[1])**2)**0.5) * 56.9

    def setDistance(self):
        '''
        set distance matrix
        '''
        rowList = []
        for i in range(self.noOfCities):
            for j in range(self.noOfCities):
                rowList.append(self.getDistance(self.cities.getCityCoord(i),self.cities.getCityCoord(j)))
            self.distance.append(rowList)
            rowList = []
        #print(self.distance)
        
    def evaluate(self, solution):
        '''
        get totalDistance of different solution(solution not include the distance back to 1st city)
        '''
        dist = 0
        for i in range(1,len(solution)):
            dist += self.distance[solution[i-1]][solution[i]]
        dist += self.distance[solution[-1]][solution[0]]
        #back to first city
        return dist

    def greedySolution(self):
        rnd.seed(29)
        startidx = rnd.randint(0, (len(self.cities.getCoordinates())-1))
        self.marked[startidx] = True
        minpq = q.PriorityQueue()   #to get the minimum distance
        currentCity = startidx
        solution = []
        solution.append(currentCity)
        
        while len(solution) != self.noOfCities:
            for idx in range(0, self.noOfCities):
                if not self.marked[idx]:
                    dist = self.distance[currentCity][idx]
                    minpq.put((dist, idx))
            item = minpq.get()
            currentCity = item[1]
            solution.append(currentCity)
            self.marked[item[1]] = True
            minpq = q.PriorityQueue()
        solution.append(startidx)
        totalDistance = self.evaluate(solution[:-1])

        return totalDistance, solution
    
    def randomHillClimbingLS(self, limit):
        totalDistance, solution = self.greedySolution()
        #print("greedy:",totalDistance)
        dist_best = totalDistance
        rnd.seed(39)
        s_best = solution[:-1]
        step = 0    #to record it cost how many times to get best solution
        
        for i in range(limit):
            temp = s_best[:]
            ran1 = rnd.randint(1, len(solution)-2)
            ran2 = rnd.randint(1, len(solution)-2)
            while ran1==ran2:
                ran2 = rnd.randint(1, len(solution)-2)

            #change 2 city position in s_best
            temp[ran1], temp[ran2] = temp[ran2], temp[ran1]
            temp_dist = self.evaluate(temp)

            #judge if the temp solution is better than s_best
            if dist_best>temp_dist:
                dist_best = temp_dist
                s_best = temp[:]
                #dist_best, s_best = self.removeCross(temp)
                step = i
        
        #print("best step:", step)
        s_best.append(s_best[0])
        return dist_best, s_best
    
    def removeCross(self, temp):
        '''
        To eliminate the cross line, not finish
        '''
        k = len(temp)
        for i in range(0, k-2):
            for j in range(i+2,k-1):
                i_i1 = self.distance[temp[i]][temp[i+1]]
                j_j1 = self.distance[temp[j]][temp[j+1]]
                i_j1 = self.distance[temp[i]][temp[j+1]]
                j_i1 = self.distance[temp[j]][temp[i+1]]
                if i_i1+j_j1>i_j1+j_i1:
                    temp[i+1],temp[j+1] = temp[j+1],temp[i+1]
        dist = self.evaluate(temp)
        return dist, temp

    def showSolution(self):
        limit = 10000    #iteration times
        totalDistance, solution = self.randomHillClimbingLS(limit)
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

    fname = "tour48pro.csv"
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
    tsp.showSolution()
            







    
