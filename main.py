import csv
from datetime import timedelta

class ChainingHashTable:
    def __init__(self, initial_capacity=16):
        self.table = []
        #self.num = 5
        for i in range(initial_capacity):
            self.table.append([])

    def insert(self, key, item):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for n in bucket_list:
            if n[0] == key:
                n[1] = item
                return True

        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    def search(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for n in bucket_list:
            if n[0] == key:
                return n[1]
        return None


    def remove(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for n in bucket_list:
            if n[0] == key:
                bucket_list.remove([n[0], n[1]])

class Package:
    def __init__(self, ID, addr, city, zipcode, deadline,  weight, status):
        self.ID = ID
        self.addr = addr
        self.city = city
        self.zipcode = zipcode
        self.deadline = deadline
        self.weight = weight
        self.status = status

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s" % (self.ID, self.addr, self.city, self.zipcode,self.deadline, self.weight, self.status)

class truck:
    def __init__(self, num, packageList, location, startingLocation, time, startingTime, mileage):
        self.num = num
        self.packageList = packageList
        self.location = location
        self.startingLocation = startingLocation
        self.time = time
        self.startingTime = startingTime
        self.mileage = mileage

def loadPackageCSV(filename):
    with open(filename) as PackageCSV:
        packageData = csv.reader(PackageCSV, delimiter=',')
        next(packageData)
        for package in packageData:
            pID = int(package[0])
            pAddr = package[1]
            pCity = package[2]
            pZipCode = package[4]
            pDeadLine = package[5]
            pWeight = package[6]
            pStatus = ["At Hub", "08:00:00"]

            package = Package(pID, pAddr, pCity,  pZipCode, pDeadLine, pWeight,  pStatus)

            myHash.insert(pID, package)

city_arr2 = []
weight_arr2 = []

def loadDistanceTableCSV(filename):
    with open(filename) as DistanceTableCSV:
        distanceTableData = csv.reader(DistanceTableCSV, delimiter=',')
        next(distanceTableData)
        for distance in distanceTableData:
            #print(distance[1])
            city_arr2.append(distance[1])
            weight_arr2.append(distance[2:len(distance)])

def packageLookUp(ID):
    return myHash.search(ID)

myHash = ChainingHashTable()

loadPackageCSV("PackageCSV.csv")

myHash.search(25).addr = "5383 S 900 East #104"
myHash.search(26).addr = "5383 S 900 East #104"

#print(myHash.search(25).addr)
#print(myHash.search(26).addr)

loadDistanceTableCSV("DistanceTableCSV.csv")

def getDistanceBetween2Cities(start, end):
    if(start <= end):
        return weight_arr2[end][start]
    else:
        return 'ERROR::make sure start is less than or equal to end'

def getShrotestDistance(pX, pY):
    print("This method will return the shortest distance between two addresses")


def getTimeBetweenPXandPY(time_string, distanceFromPXtoPy):
    # print(time_string)
    h, m, s = time_string.split(':')
    current_time = timedelta(hours=int(h), minutes=int(m))
    # print(current_time)
    travel_time = timedelta(hours=distanceFromPXtoPy / 18)
    # print(travel_time, (current_time + travel_time))

    calc_time = current_time + travel_time

    formatted_timedelta_current_time = f"{calc_time.seconds // 3600:02}:{(calc_time.seconds // 60) % 60:02}:{calc_time.seconds % 60:02}"
    #formatted_timedelta_travel_time = f"{current_time.seconds // 3600:02}:{(current_time.seconds // 60) % 60:02}:{current_time.seconds % 60:02}"

    #print(formatted_timedelta_current_time)

    #print(formatted_timedelta_current_time + travel_time)

    return formatted_timedelta_current_time

#trk1 = getTruckRoute(truck(1, [16, 34, 15, 37, 14, 20, 40, 19, 31, 13, 29, 39, 5, 26], "At Hub", "At Hub", "08:00:00", "08:00:00", 0))
#trk2 = getTruckRoute(truck(2, [38, 3, 30, 1, 25,6, 36, 18, 28, 32, 33, 35], "At Hub", "At Hub", "09:05:00", "09:05:00", 0))
#trk1_2 = getTruckRoute(truck(1, [9, 2, 4, 7, 8, 10, 11, 12, 17, 21, 22, 23, 24, 27], "At Hub", "At Hub", trk1.time, trk1.time, 0))