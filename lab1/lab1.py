from heapq import heappop, heappush
import matplotlib.pyplot as pyplot
from functools import reduce
from math import sqrt

### INTRO

# in 1
a = 10
print (a)
a += 3
print (a)

# in 2
l1 = [1,2,3,4]
l2 = [x*x for x in range(4)]
l3 = [(chr(i), j) for i in range(ord('a'), ord('c') + 1) for j in range(1,3)]
l4 = l1 + l2 + l3

print(l4)
print(l4[3:-3])


# labirint

height = 10
width = 20
labyrinth = [[0 for c in range(width)] for r in range(height)]

for r in range(2,7):
    labyrinth[r][6] = 1
    labyrinth[6][r] = 1
labyrinth[2][7] = 1

pyplot.imshow(labyrinth, cmap='Greys', interpolation='nearest')
#pyplot.show()


# define start and end points
start = (5,5)
final = (8,8)

# is_final test
is_final = lambda position : position == final
print(list(map(is_final, [(1, 1), (3, 6), (8, 8)])))

# filter
print(list(filter(lambda x : x % 3 == 2, range(20))))

#reduce
print(reduce(lambda x,y: [y] + x, [7,8,9], []))

print('------------------------------')
### A* HELPERS

def is_good(pos):
    if (pos[0] >= 0 and pos[0] < height and pos[1] >= 0 and pos[1] < width):
        return labyrinth[pos[0]][pos[1]] == 0
    return False        

print(list(map(is_good, [(-1, 2), (height, 3), (width, 4), (5, 5), (6, 6)])))

def get_neighbours(pos):
    (r,c) = pos
    return (list(filter(is_good, [(r - 1, c),
                                  (r, c - 1),
                                  (r, c + 1),
                                  (r + 1, c)])))


print([get_neighbours(p) for p in [(0, 9), (5, 5)]])


def euclidean_distance(a, b):
    (ay, ax) = a
    (by, bx) = b
    return (sqrt((ay - by) * (ay - by) + (ax - bx) * (ax - bx)))

print(euclidean_distance((2, 3), (4, 7)))

def manhattan_distance(a,b):
    (ay, ax) = a
    (by, bx) = b
    return (abs(ay-by) + abs(ax-bx))

print(manhattan_distance((2, 3), (4, 0)))

def shitty_heuristic(a,b):
    (ay, ax) = a
    (by, bx) = b
    return 1 / (5 + (abs(ay-by) + abs(ax-bx)) * (abs(ay-by) + abs(ax-bx)) * 10) - 4000

def no_heuristic(a,b):
    return 0

priority_queue = []
heappush(priority_queue, (2, 'A'))
heappush(priority_queue, (1, 'B'))
heappush(priority_queue, (1.5, 'C'))

print(heappop(priority_queue)) 
print(heappop(priority_queue))
print(heappop(priority_queue))

d = {}
d['doi'] = 2
d['trei'] = 3

print(d['doi'])

print(d.get('trei'))
print(d.get('patru', 'Nu am gasit!'))

for (key, value) in d.items():
    print(key, " -> ", value)

### A* actual algo

# obs: euristica folosita trebuie sa fie una optimista pentru a da rezultate bune
# distanta euclidiana: optimista pentru ca ma misc doar stg/dreapta/sus/jos
# distanca manhattan: optimista pentru ca nu tine cont de obstacole

# cat timp mai am noduri in frontiera

    # scot un nod din forntiera

    # daca nodul e de final
        # break
    
    # daca nu e nodul final
    # pentru fiecare vecin:
        # daca vecinul e nod neexplorat
        # calculez f cost
        # il marchez ca explorat + pus in frontiera

        # daca nodul era deja descoperit
            # recalculez g cost si actualizez in frontiera + actualizez in discovered

def astar(start, end, h):
    # Frontiera, ca lista (heap) de tupluri (cost-total-estimat, nod)
    frontier = []
    heappush(frontier, (0 + h(start, end), start))
    # Nodurile descoperite ca dictionar nod -> (parinte, cost-pana-la-nod)
    discovered = {start: (None, 0)}
    while frontier:
        (crtFCost, crtNode) = heappop(frontier)
        crtGCost = crtFCost - h(crtNode, end)

        if (crtNode == end):
            print('found end!')
            break

        for childNode in get_neighbours(crtNode):
            childNodeGCost = 1 + crtGCost

            if (not(childNode in discovered)):
                childNodeHCost = h(childNode, end)
                childNodeFCost = childNodeGCost + childNodeHCost

                discovered[childNode] = (crtNode, childNodeGCost)

                if (not (childNode in (elem[1] for elem in frontier))):
                    heappush(frontier, (childNodeFCost, childNode))
            else:
                if (childNodeGCost < discovered[crtNode][1]):
                    discovered[childNode] = (crtNode, childNodeGCost)
                    newFCost = childNodeGCost + h(childNode, end)
                    heappush(frontier, (newFCost, childNode))

    cost_map = [[discovered[(r, c)][1] if (
        r, c) in discovered else 0 for c in range(width)]for r in range(height)]
    pyplot.imshow(cost_map, cmap='Greys', interpolation='nearest')
    pyplot.show()

    # Refacem drumul
    path = []
    crtPathNode = end
    while (crtPathNode is not None):
        path.append(crtPathNode)
        crtPathNode = discovered[crtPathNode][0]    
    return path  # drumul, ca lista de pozitii

euclidPath = astar(start, final, euclidean_distance)
print(euclidPath)
euclid_map = [[1 if (r,c) in euclidPath else 0 for c in range(width)]
for r in range(height)]
pyplot.imshow(euclid_map, cmap='Greys', interpolation='nearest')
pyplot.show()

manhattanPath = astar(start, final, manhattan_distance)
print(manhattanPath)
manhattan_map = [[1 if (r, c) in manhattanPath else 0 for c in range(width)]
              for r in range(height)]
pyplot.imshow(manhattan_map, cmap='Greys', interpolation='nearest')
pyplot.show()

badPath = astar(start, final, shitty_heuristic)
print(badPath)
bad_map = [[1 if (r, c) in badPath else 0 for c in range(width)]
                 for r in range(height)]
pyplot.imshow(bad_map, cmap='Greys', interpolation='nearest')
pyplot.show()

nohpath = astar(start, final, no_heuristic)
print(nohpath)
noh_map = [[1 if (r, c) in nohpath else 0 for c in range(width)]
                 for r in range(height)]
pyplot.imshow(noh_map, cmap='Greys', interpolation='nearest')
pyplot.show()
