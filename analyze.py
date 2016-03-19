from datetime import date
import json
from math import sqrt

# Definition for mean/standard deviation
# from http://blog.zinctech.com/?q=node/86
# (there are packages that do this, but we don't need that yet)
def meanstdv(x):
    std = []
    for value in x:
        std.append(pow((value - (sum(x)/len(x))), 2))
    stddev = sqrt(sum(std)/len(std))
    mean = (sum(x)/len(x))
    return float(mean), float(stddev)

# Get today's date
today = date.today()

# Initialize the inventory
inventory = {}

# Initialize a list to keep track of all the days
allDays = []

# Open the inventory file
with open('inventory.txt','r') as f:
    # Iterate over each line
    for line in f:
        # Split the line by the comma
        csvs = line.split(',')
        # Check if it has a date (it should have a slash)
        if '/' in csvs[0]:
            # Parse the day
            monthDate = csvs[0].split()[0]
            day = date(2000+int(monthDate.split('/')[2]),int(monthDate.split('/')[0]),int(monthDate.split('/')[1]))
            # Calculate the number of days passed since this order
            days = abs(today-day).days
            allDays.append(days)
            # For each item in this line, add it to the inventory state that it was ordered this many days ago
            for item in csvs[1:]:
                item = item.strip()
                if item not in inventory: # Need to initialize if its not in the inventory
                    inventory[item] = {}
                    inventory[item]['daysSincePurchase'] = []
                inventory[item]['daysSincePurchase'].append(days)


### Calculate the mean time between purchasing and the last bought time
lastDayBought = max(allDays)
groceries = {}
for item in inventory:
    # Add in the last time bought to inventory dictionary
    inventory[item]['lastBought'] = min(inventory[item]['daysSincePurchase'])
    # Only calculate things that have more than one dates
    if len(inventory[item]['daysSincePurchase']) > 1:
        # Find difference between dates
        diffDates = []
        sortedDates = sorted(inventory[item]['daysSincePurchase'])
        for i in range(1,len(sortedDates)):
            diffDates.append(sortedDates[i]-sortedDates[i-1])
        # Calculate mean time between puchases
        meanWaitTimeToPurchase, foo = meanstdv(diffDates)
        # Add this to the inventory dictionary
        inventory[item]['meanWaitTime'] = meanWaitTimeToPurchase
    else:
        # Not enough data to say the mean time yet
        inventory[item]['meanWaitTime'] = -1


### Print full inventory as JSON type
print("-"*10 + "JSON of inventory dictionary" + "-"*10)
print(json.dumps(inventory,indent=2))
print("-"*30)


### Application: print mean time between purchases, and time of next purcahse
for item in inventory:
    # (Remember that 'today' is defined as 0 days since purchase)
    if inventory[item]['meanWaitTime'] < 0:
        print("%s was purchased %d days ago." % (item,inventory[item]['lastBought']))
    else:
        daysTillNextPurchase = inventory[item]['meanWaitTime'] - inventory[item]['lastBought']
        if daysTillNextPurchase > 0:
            print("%s was purchased %d days ago. The mean time between purchases is %d days so you should buy more in %d days." % (item,inventory[item]['lastBought'],inventory[item]['meanWaitTime'],daysTillNextPurchase))
        else:
            print("%s was purchased %d days ago. The mean time between purchases is %d days so you should buy more now." % (item,inventory[item]['lastBought'],inventory[item]['meanWaitTime']))
