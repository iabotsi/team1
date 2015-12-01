import sys
import math
import random as rnd
import queue as q
import matplotlib.pyplot as plt



class Tsp:
    def __init__(self,filename):
        self.Mylist=[]
        self.Mylist= self.myList(filename)  # The function myList(self) reads the file and put the names of cities and x,y cordinates in two diffrent list eg[[cities],[(x,y)]] 
        self.cities=self.Mylist[0]                  # This is a list containing cities only ie. [cities]
        self.cordinate=self.Mylist[1]           # This list contains cordinates point only 
        self.distance=self.distance()           # This is a list of distance for the entire data. this list contains 50 sublist [[list1],[list2]...........[list50]]



    def myList(self,filename):
        f = open(filename)
        cities=[]
 
        cordxy=[]
        for line in f:
            alist = line.split(';') 
            for i in range(0,len(alist)):
                alist[i] = alist[i].rstrip('\n')
                alist[i]=alist[i].rstrip(',')
            cities.append(alist[0])
            x=int(alist[1])
            y=int(alist[2])
            cordxy.append( (x,y) )
        self.Mylist.extend([cities,cordxy])
        f.close()
        return(self.Mylist)

    def distance(self):
        dis=[]
        size=len(self.cordinate)
        for cd in range(0,size):
            deem=[]
            for uu in range(0,size):
                me=(self.cordinate[cd][0]-self.cordinate[uu][0])**2+(self.cordinate[cd][1]-self.cordinate[uu][1])**2
                me=(me)**0.5
                deem.append(me*56.9)
            dis.append(deem)
        return(dis)

    def getcityanddistance(self,n):                     # This methods returns the name of the city and its distance from each city
        return(self.cities[n],self.distance[n])
        
 

    
            
t = Tsp('tour48pro.csv')   # To test the function
print(t.Mylist)
print()
print(t.cordinate)
print()
print(t.cities)
print()
print(t.getcityanddistance(2))
print()






    



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
            







    
