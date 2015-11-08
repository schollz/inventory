from datetime import date
import numpy
import json

today = date.today()
foods = {}
allDays = []

with open('data.csv','r') as f:
    for line in f:
        csvs = line.split(',')
        if '/' in csvs[0]:
            monthDate = csvs[0].split()[0]
            day = date(2000+int(monthDate.split('/')[2]),int(monthDate.split('/')[0]),int(monthDate.split('/')[1]))
            days = abs(today-day).days
            allDays.append(days)
            for food in csvs[1:]:
                f = food.strip()
                if f not in foods:
                    foods[f] = []
                foods[f].append(days)


firstDay = max(allDays)
groceries = {}
for food in foods:
    groceries[food] = {}
    groceries[food]['meanWaitTime'] = numpy.mean(numpy.diff(sorted([0] + foods[food] + [firstDay])))
    groceries[food]['lastBought'] = min(foods[food])
    if groceries[food]['meanWaitTime'] < groceries[food]['lastBought']:
        print(food)

#print(json.dumps(groceries,indent=2))

