#diastaseis dentrou
DIMENSIONS = 2

class Node:
	def __init__(self, coords, name=None, left=None, right=None, next_dimension=None):
		self.coords = coords
		self.name = name
		self.left = left
		self.right = right
		self.next_dimension = next_dimension


#eisodos: lista me tis syntetagmenes twn komvwn 
#eksodos: h riza tou dentrou kai mia lista gia ta dentra epomenis diastasis
def create_range_tree(nodes_list, dimension=0):

	if len(nodes_list) == 0 or dimension >= DIMENSIONS:
		return None, []

	#mesaio stoixeio gia riza dentrou
	mid = int(len(nodes_list)/2)
	root = nodes_list[mid]

    #aristero kai deksi ypodentro
	root.left, left_list = create_range_tree(nodes_list[:mid], dimension)
	root.right, right_list = create_range_tree(nodes_list[mid+1:], dimension)
    
    #gia tis epomenes diastaseis 
	merged_list = []

	if dimension + 1 < DIMENSIONS: #sti periptwsi mas tha stamatisei stis 2 diastaseis
		merged_list = merge(root, left_list, right_list, dimension + 1)

    #ftiaxnoume ti nea diastash me ta kainouria sorted nodes    
	root.next_dimension, _ = create_range_tree(merged_list, dimension + 1)

	return root, merged_list


#eisodos: riza kai duo sorted listes
#eksodos: mia sorted lista 
def merge(root, left_list, right_list, dimension=0):
    
    if dimension >= DIMENSIONS:
        return []
    
    final_list = []
    left_index = 0
    right_index = 0
    
    #theloume na enwsoume tis duo listes kratwntas to sort
    #kanoume xeirokinhta to sort twn syntetagmenwn opws me to lambda sto menu
    
    #oso uparxoun kai aristera kai deksia stoixeia
    while left_index < len(left_list) and right_index < len(right_list):
        if left_list[left_index].coords[dimension] < right_list[right_index].coords[dimension]:
            final_list.append(Node(left_list[left_index].coords, left_list[left_index].name))
            left_index = left_index + 1
        else:
            final_list.append(Node(right_list[right_index].coords, right_list[right_index].name))
            right_index = right_index + 1
            
    #an exoume mono aristera kai oxi deksia (mono i sinthiki 1)
    while left_index < len(left_list):
        final_list.append(Node(left_list[left_index].coords, left_list[left_index].name))
        left_index = left_index + 1
        
    #an exoume deksia kai oxi aristera (mono i sinthiki 2)
    while right_index < len(right_list):
     final_list.append(Node(right_list[right_index].coords, right_list[right_index].name))
     right_index = right_index + 1
        
    #afou ftiaksoume th lista theloume na vroume th thesh ths rizas
    #eite tha einai kapou mesa sto final list h sto telos
    for i in range(0, len(final_list)):
    	if root.coords[dimension] < final_list[i].coords[dimension]:
			#mesa
    		return final_list[:i] + [Node(root.coords, root.name)] + final_list[i:]
	
	#telos
    return final_list + [Node(root.coords, root.name)]
