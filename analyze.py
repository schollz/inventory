foods = {}
with open('list.csv','r') as f:
    for line in f:
        csvs = line.split(',')
        if '/' in csvs[0]:
            monthDate = csvs[0].split()[0]
            days = 30*int(monthDate.split('/')[0])
            days += 1*int(monthDate.split('/')[1])
            days += 365*int(monthDate.split('/')[2])
            for food in csvs[1:]:
                f = food.strip()
                if f not in foods:
                    foods[f] = []
                foods[f].append(days)

print(foods)
