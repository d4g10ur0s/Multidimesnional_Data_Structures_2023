import csv
import random
import string
import range_tree as rt

#### Functions ####

#gia tin print tree: pre-order traversal
def pre_order(root, string=""):
    if root:
        print(string + str(root.coords) + "|Education:" + str(root.name))
        pre_order(root.left, "\t" + string + "-left-")
        pre_order(root.right, "\t" + string + "-right-")

#### Menu ####

#dialegoume real h simulated data
choose_data = int(input("0 - Real Data\n1 - Simulated Data\n-> "))

my_nodes = []
nodes_counter = 0

if choose_data == 0:
    
    filename = 'data\\data.csv'
    
    #diavazoume to arxeio kai dimiourgoume kateytheian node objects
    with open(filename, mode='r', encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            print(row[0])
            print(row[1])
            print(row[2])
            my_nodes.append(rt.Node([float(row[0].replace(',','.')), float(row[1].replace(',','.'))], row[2]))
            nodes_counter += 1
        print('Number of Nodes: ' + str(nodes_counter))
    
    #gia na mporoume na kanoume search me to name ston knn
    # with open(filename, mode='r', encoding="utf-8") as csv_file:
    #     csv_reader = csv.reader(csv_file, delimiter=';')
    #     hosp = hos.put_into_list(csv_file)
        
else:
    #tyxaia string gia ta onomata twn simulated data
    string_len = 5
    chars = string.ascii_lowercase
    
    for j in range(0,int(input("Give the number of Nodes you want to create: "))):
        coords = []
        name = ''.join((random.sample(chars, string_len)))
        for k in range(0, rt.DIMENSIONS):
            coords.append(random.randint(0,10))
            nodes_counter += 1
    
        my_nodes.append(rt.Node(coords, name))

#sortaroume tis syntetagmenes twn komvwn kai ftiaxnoume to dentro
sorted_nodes = sorted(my_nodes, key=lambda l:(l.coords[0], l.coords[1]))
my_root, _ = rt.create_range_tree(sorted_nodes)

#menu gia tis diadikasies tou dentrou
print("\nMENU")
print("0 - Print Tree")
print("-1 - Exit Program\n")

choice = int(input())

while choice != -1:

    # Print Tree
    if choice == 0:
        print('-----------------------')
        pre_order(my_root)
        print('-----------------------')
    choice = int(input())