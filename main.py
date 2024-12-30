'''
NAME: Christopher Burzo
STUDENT ID: 011825393
'''

import csv
from datetime import timedelta

'''
HASH TABLE CLASS
---------------
This class serves as my main database to hold all package data
'''
class ChainingHashTable:
    def __init__(self, initial_capacity=16):
        self.table = []
        #self.num = 5
        for i in range(initial_capacity):
            self.table.append([])
    '''
    Method to add a package to the hash table
    '''
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

    '''
    Method to search for an existing package and return None
    if it does not exist
    '''
    def search(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for n in bucket_list:
            if n[0] == key:
                return n[1]
        return None

    '''
    Method to remove a package to the hash table
    '''
    def remove(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for n in bucket_list:
            if n[0] == key:
                bucket_list.remove([n[0], n[1]])

'''
PACKAGE CLASS
---------------
This class instantiates packages
'''
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

'''
TRUCK CLASS
---------------
This class instantiates trucks
'''
class truck:
    def __init__(self, num, packageList, location, startingLocation, time, startingTime, mileage):
        self.num = num
        self.packageList = packageList
        self.location = location
        self.startingLocation = startingLocation
        self.time = time
        self.startingTime = startingTime
        self.mileage = mileage

'''
PACKAGE LOADING METHOD
-----------------------
This method loads all data from the existing PackageCSV.csv file
'''
def loadPackageCSV(filename):
    with open(filename) as PackageCSV:
        packageData = csv.reader(PackageCSV, delimiter=',')
        next(packageData)
        '''
        loop through all the packages from the csv file and load contents into variables
        '''
        for package in packageData:
            pID = int(package[0])
            pAddr = package[1]
            pCity = package[2]
            pZipCode = package[4]
            pDeadLine = package[5]
            pWeight = package[6]
            pStatus = ["At Hub", "08:00:00"]

            '''
            create a new instance object from the package class and store that in a variable 
            '''
            package = Package(pID, pAddr, pCity,  pZipCode, pDeadLine, pWeight,  pStatus)

            '''
            insert the package with its ID into the hash table
            '''
            myHash.insert(pID, package)

'''
DISTANCE TABLE LOADING METHOD
-----------------------------
This method loads all data from the existing DistanceTableCSV.csv file
'''
def loadDistanceTableCSV(filename):
    with open(filename) as DistanceTableCSV:
        distanceTableData = csv.reader(DistanceTableCSV, delimiter=',')
        next(distanceTableData)
        '''
        loop through all the data in the distance file and store them in two arrays
        '''
        for distance in distanceTableData:
            '''
            1d array to hold only the address names from the distance table
            '''
            city_arr2.append(distance[1])
            '''
            2d array to hold only the distance data from the distance table
            '''
            weight_arr2.append(distance[2:len(distance)])

'''
PACKAGE LOOKUP METHOD
---------------------
This method simply returns the corresponding package data when an id is input
'''
def packageLookUp(ID):
    return myHash.search(ID)

'''
This method returns the distance between any 2 address inputs
'''
def getDistanceBetweenAddr(PX, PY):
    if city_arr2.index(PX) >= city_arr2.index(PY):
        return weight_arr2[city_arr2.index(PX)][city_arr2.index(PY)]
    else:
        return weight_arr2[city_arr2.index(PY)][city_arr2.index(PX)]

'''
This method finds accepts the input of an address and an array of package IDs.
It will loop through every element in the array to find the smallest distance 
between the given address and the the element
'''
def minDistanceFrom(fromAddr, trkPkgs):
    min = 25.0
    addrOfMin = ''
    idx = 0
    for i in range(0, len(trkPkgs)):
        if float(getDistanceBetweenAddr(fromAddr, " "+packageLookUp(trkPkgs[i]).addr+"\n("+packageLookUp(trkPkgs[i]).zipcode+")")) < min:
            min = float(getDistanceBetweenAddr(fromAddr, " "+packageLookUp(trkPkgs[i]).addr+"\n("+packageLookUp(trkPkgs[i]).zipcode+")"))
            addrOfMin = " "+packageLookUp(trkPkgs[i]).addr+"\n("+packageLookUp(trkPkgs[i]).zipcode+")"
            idx = i

    '''
    After the smallest distance is found, the method returns the address of the smallest distance,
    the index in the array corresponding to the smallest distance and the minimum distance value itself
    '''
    return [addrOfMin, idx, min]

'''
This method accepts the inputs: a string represent time in the format 00:00:00 and the raw
distance from one address to another.

The time taken between those distances is calculated and then formatted back to 00:00:00
'''
def getTimeBetweenPXandPY(time_string, distanceFromPXtoPy):
    h, m, s = time_string.split(':')
    current_time = timedelta(hours=int(h), minutes=int(m))
    travel_time = timedelta(hours=distanceFromPXtoPy / 18)
    calc_time = current_time + travel_time

    formatted_timedelta_current_time = f"{calc_time.seconds // 3600:02}:{(calc_time.seconds // 60) % 60:02}:{calc_time.seconds % 60:02}"

    '''
    The calculated time between the distances is returned
    '''
    return formatted_timedelta_current_time

'''
This method accepts an instance object of truck. It is the main method for delivering
every package in the trucks package list.

Before the loop starts, the first distance is called and loaded into nextAddr variable. 
Then the time between those distances is taken and stored in time variable. The truck and 
package data, in there respective data structures, are then updated.
'''
def deliverPackages(trk):
    nextAddr = minDistanceFrom(" HUB", trk.packageList)
    time = getTimeBetweenPXandPY(trk.startingTime, nextAddr[2])
    trk.time = time
    packageLookUp(trk.packageList[nextAddr[1]]).status[0] = "Delivered"
    packageLookUp(trk.packageList[nextAddr[1]]).status[1] = str(time)
    '''
    After updating the the truck's package list, the address stored in nextAddr is "visited", therefore it
    is then sliced out of the package list to reduce the array to the packages that have not yet been 
    visited.
    '''
    trk.packageList = trk.packageList[0:nextAddr[1]] + trk.packageList[nextAddr[1] + 1:len(trk.packageList)]
    '''
    Keeps a running total of the mileage for the trucks
    '''
    tot = nextAddr[2]

    '''
    What was introduced in the first part of the method will now repeat in the form of a loop. The loop runs
    until the trucks package list is empty and all packages are essentially delivered and no longer on the truck
    '''
    while len(trk.packageList) != 0:
        nextAddr = minDistanceFrom(nextAddr[0], trk.packageList)
        time = getTimeBetweenPXandPY(time, nextAddr[2])
        trk.time = time
        packageLookUp(trk.packageList[nextAddr[1]]).status[0] = "Delivered"
        packageLookUp(trk.packageList[nextAddr[1]]).status[1] = str(time)
        trk.packageList = trk.packageList[0:nextAddr[1]] + trk.packageList[nextAddr[1] + 1:len(trk.packageList)]
        tot += nextAddr[2]

    '''
    The time to hub is kept track of for each truck and returned to be used later in a seperate calculation
    to add the time to the hub to the truck's total time
    '''
    timeToHub = getTimeBetweenPXandPY(time, float(getDistanceBetweenAddr(nextAddr[0], " HUB")))
    '''
    The total mileage is kept track of for each truck and the mileage from the final address that the truck visits
    to the hub is added
    '''
    trk.mileage = tot + float(getDistanceBetweenAddr(nextAddr[0], " HUB"))
    return timeToHub

'''
This function "pretty" prints the status for all packages at any given time input
'''
def printPackageStatusForAllPackages(myInputTime, printFlag):
    print("Package Status at", myInputTime)
    if printFlag == 1:
        print("Package ID, Truck, City, ZipCode, DeadLine, Weight(Kilo), Time, Status")
    print("----------------------------------------------------------------------")
    '''
    This loop assigns flags to make it clear to the method, which package is in which truck
    '''

    for i in range(1, 41):
        if packageLookUp(i).ID in arr1Load:
            truk = "trk1"
            tRoute = "Truck 1 for First Route"
        elif packageLookUp(i).ID in arr2Load:
            truk = "trk2"
            tRoute = "Truck 2"
        elif packageLookUp(i).ID in arr1_2Load:
            truk = "trk1_2"
            tRoute = "Truck 1 for Second Route"
        else:
            truk = "no truck has loaded the package yet"

        '''
        The flags that are stored above are used to distinguish the status of each truck in the following 
        conditional sequence. 
        '''
        if myInputTime < packageLookUp(i).status[1]:
            packageLookUp(i).status[0] = "En Route"

        if myInputTime < trk2.startingTime and truk == "trk2":
            packageLookUp(i).status[0] = "At Hub"

        if myInputTime < trk1.time and truk == "trk1_2":
            packageLookUp(i).status[0] = "At Hub"

        if myInputTime >= "10:20:00":
            packageLookUp(9).addr = "410 S State St"
            packageLookUp(9).zipcode = "84111"

        if printFlag == 1:
            print("Package ID:", packageLookUp(i).ID,", on", tRoute, " --- ", packageLookUp(i).addr, ", ",packageLookUp(i).city, ", ",
                  packageLookUp(i).zipcode, ", ",packageLookUp(i).deadline, ", ",packageLookUp(i).weight , " --- ",
                  packageLookUp(i).status[0], " at ", packageLookUp(i).status[1]
                  if packageLookUp(i).status[0] == "Delivered" else myInputTime)

'''
This function "pretty" prints a single package when given the inputs: id and time in the form 00:00:00
'''
def packageLookUpByIdForTime(id, myInputTime):
    if packageLookUp(id).ID in arr1Load:
        tRoute = "Truck 1 for First Route"
    elif packageLookUp(id).ID in arr2Load:
        tRoute = "Truck 2"
    elif packageLookUp(id).ID in arr1_2Load:
        tRoute = "Truck 1 for Second Route"
    else:
        truk = "no truck has loaded the package yet"

    print("Package ID, Truck, City, ZipCode, DeadLine, Weight(Kilo), Status, Time")
    print("----------------------------------------------------------------------")
    if myInputTime < packageLookUp(id).status[1]:
        print(packageLookUp(id).ID, ", on", tRoute, " --- ", packageLookUp(id).addr, packageLookUp(id).city, packageLookUp(id).zipcode,
              packageLookUp(id).deadline, packageLookUp(id).weight, "---", packageLookUp(id).status[0], "at", myInputTime)
    else:
        print(packageLookUp(id).ID, ", on", tRoute, " --- ", packageLookUp(id).addr, packageLookUp(id).city, packageLookUp(id).zipcode,
              packageLookUp(id).deadline, packageLookUp(id).weight, "---",packageLookUp(id).status[0], "at" ,packageLookUp(id).status[1])

'''
USER INTERFACE:
---------------
The following code is all part of the user interface sequence. The first thing to input is the time for the 
packages you want to view 
'''
myTime = input("Enter time in the form of 00:00:00 -> ")
print("")

'''
infinite loop that will run all the methods and object instantiations needed to produce the 
correct results, and then display the USER INTERFACE.
'''
while True:
    '''
    create arrays that hold the distance table csv information
    '''
    city_arr2 = []
    weight_arr2 = []
    '''
    create an instance object of the hash table
    '''
    myHash = ChainingHashTable()

    '''
    load the data from the packageCSV.csv file. 
    '''
    loadPackageCSV("PackageCSV.csv")

    '''
    This address string needs to be reformatted to the following, because the original string is
    not supported by the array: city_arr2. The original string is: 5383 South 900 East #104. The 
    South produces a NoneType error, the following fixes that error
    '''
    myHash.search(25).addr = "5383 S 900 East #104"
    myHash.search(26).addr = "5383 S 900 East #104"

    '''
    load the data from the DistanceTableCSV.csv file. 
    '''
    loadDistanceTableCSV("DistanceTableCSV.csv")

    '''
    arr1Load, arr2Load, and arr1_2Load hold the packages permanently. This is needed because the truck package
    list is constantly sliced eventually having a length of 0 at the end of their routes.
    '''
    arr1Load = [15, 40, 37, 13, 14, 16, 20, 31, 34, 25, 19, 10, 8, 7]
    arr2Load = [1, 6, 29, 30, 3, 18, 36, 38, 11, 12, 17, 21]

    '''
    truck1 (first route), truck 2, and truck 1 (second route) instances are created
    '''
    trk1 = truck(1, arr1Load, "At Hub", "At Hub", "08:00:00", "08:00:00", 0)
    trk2 = truck(2, arr2Load, "At Hub", "At Hub", "09:05:00", "09:05:00", 0)

    '''
    calls deliver packages and stores the remaining time to hub into trk1TimeToHub, trk2TimeToHub, and truck1_2TimeToHub
    '''
    trk1TimeToHub = deliverPackages(trk1)
    trk2TimeToHub = deliverPackages(trk2)

    arr1_2Load = [2, 4, 5, 9, 22, 23, 24, 26, 27, 28, 32, 33, 35, 39]
    trk1_2 = truck(1, arr1_2Load, "At Hub", "At Hub", trk1.time, trk1.time, 0)

    truck1_2TimeToHub = deliverPackages(trk1_2)

    '''
    Print sequence that displays the total mileage and total time for each truck and the total mileage for 
    all trucks
    '''
    print("")
    print("Truck ", trk1.num, "has finished its first route with a mileage of: ", round(trk1.mileage, 1),
          ", and a time: ", trk1TimeToHub)
    print("Truck ", trk2.num, "has finished its first route with a mileage of: ", round(trk2.mileage, 1),
          ", and a time: ", trk2TimeToHub)
    print("Truck ", trk1_2.num, "has finished its second route with a mileage of: ", round(trk1_2.mileage, 1),
          ", and a time: ", truck1_2TimeToHub)
    print("The total Distance for all trucks is: ", round(trk1.mileage + trk2.mileage + trk1_2.mileage, 1))
    print("")

    '''
    --------------
    USER INTERFACE
    --------------
    '''
    print("Your time is: ", myTime, " Now please select your function: ")
    print("1: Package Lookup by ID")
    print("2: Print All Packages")
    print("3: Change Time")
    print("4: End Program")
    inputVal = int(input("Enter Choice: "))
    print("")

    if inputVal == 1:
        id = int(input("Enter a Package ID: "))
        printPackageStatusForAllPackages(myTime, 0)
        packageLookUpByIdForTime(id, myTime)
    elif inputVal == 2:
        printPackageStatusForAllPackages(myTime, 1)
    elif inputVal == 3:
        myTime = input("Enter time in the form of 00:00:00 -> ")
        print("")
    else:
        break