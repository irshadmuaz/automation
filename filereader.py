import csv

def write(store):
    with open('names.csv', 'w', newline='') as csvfile:
        fieldnames = [key for key in store[0].keys()]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in store:
            writer.writerow(row)
        

def read():
    store = []
    with open('names.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
           store.append(row)
    print('read names.csv successfully')
    return store
    