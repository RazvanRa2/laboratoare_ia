import matplotlib.pyplot as pyplot
import networkx as nx
from functools import reduce
import operator
# Dimensiunea mediului
width = 2
height = 1

# Initial, intreg spatiul este murdar.
env = [[1 for x in range(width)] for y in range(height)]

start = (0, 0)
#env[start[1]][start[0]] = 0

moves = ['Left', 'Right', 'Clean']

# efect is a tuple of:
#  delta-x
#  delta-y
#  cleanness of current cell if current cell was clean
#  cleanness of cell to the right if current cell was clean
#  cleanness of current cell if current cell was dirty
#  cleanness of cell to the right if current cell was dirty

# deterministic effects:
effectD = {}
effectD['Left'] = [(-1, 0, -1, -1, -1, -1)]
effectD['Right'] = [(+1, 0, -1, -1, -1, -1)]
effectD['Clean'] = [(0, 0, 0, -1, 0, -1)]

# non-deterministic effects:
effectN = {}
effectN['Left'] = effectD['Left']
effectN['Right'] = effectD['Right']
effectN['Clean'] = [(0, 0, 0, -1, 0, -1), (0, 0, 1, -1, 0, 0)]


# Intoarce adevarat daca celula este o celula in interiorul spatiului.

def is_good(state):
    return state[0] >= 0 and state[0] < width and state[1] >= 0 and state[1] < height

# Intoarce adevarat daca toate celulele din mediu sunt curate.


def env_clean(env): return 0 == len(
    list(filter(lambda x: x > 0, reduce(operator.add, env, []))))

# Intoarce o lista de tupluri (stare-noua, mediu-nou), continand ca singur element efectul
#    realizarii mutarii deterministe specificate. Daca mutarea nu poate fi realizata, lista este nula.
# Mediul intors este o copie (instanta noua) a parametrului dat.


def compute_effectD(state, env, move):
    return compute_effects(state, env, move, effectD)

# Intoarce o lista de tupluri (stare-noua, mediu-nou), continand efectele realizarii mutarii nedeterministe specificate.
# Lista poate contine zero (daca mutarea nu este posibila), unul sau mai multe elemente distincte.
# Mediul intors este o copie (instanta noua) a parametrului dat.


def compute_effectN(state, env, move):
    return compute_effects(state, env, move, effectN)


def compute_effects(state, env, move, effects):
    effects = [compute_effect(state, env, effect) for effect in effects[move]]
    effects = list(filter(lambda e: e is not None, effects))
    if len(effects) == 2 and effects[0] == effects[1]:
        return effects[:1]
    return effects


def compute_effect(state, env, effect):
    new_env = [line[:] for line in env]
    (x, y) = state
    new_state = tuple([state[idx] + effect[idx] for idx in range(2)])
    if not is_good(new_state):
        return None

    for d in range(2):
        clean_effect = effect[2 + d + env[y][x] * 2]
        if clean_effect >= 0 and is_good((x + d, y)):
            new_env[y][x + d] = clean_effect
    return (new_state, new_env)


printX = 1
print(env_clean(env))
print([compute_effectD((printX, 0), env, m) for m in moves])
print(compute_effectD((printX, 0), env, 'Clean'))
print(compute_effectN((printX, 0), env, 'Clean'))

TYPE = 0
STATE = 1
ENV = 2
CHILDREN = 3
TAG = 4
PATH = 5


counter = 0
labels = {}
nodes = []
edges = []


# reprezentam un nod din arbore ca o lista
# [move, state, environment, children, tag(None/SUCCESS/LOOP), path]
# formata din mutarea realizata în nodul părinte, stare în urma mutării, starea mediului în urma mutării,
#   lista de copii ai nodului (tot noduri), etichetă, reprezentare a căii din rădăcină până în nod


# afișează un arbore format din noduri definite ca mai sus (se dă rădăcina arborelui, care conține și copiii, etc)
# parametrul onlyOR indică dacă arborele este format doar din noduri SAU (altfel, este interpretat ca arbore ȘI-SAU)
def printTree(root, onlyOR=True):
    G=nx.Graph()

    printTreeEx(root, 0, onlyOR, None)

    #G.add_nodes_from(nodes)
    #G.add_edges_from(edges)
    #nx.draw(G)
    #pyplot.show() # display


def printTreeEx(node, indent, onlyOR, parent):
    global counter
    line = ""
    for i in range(indent):
        line += "   "
    if node[TYPE] == "OR":
        line += "|  "
        line += str(node[STATE]) + " : " + str(node[ENV])
    else:
        line += ". " + node[TYPE] + " -> "
        if onlyOR:
            line += str(node[STATE]) + " : " + str(node[ENV])
    if node[TAG] is not None:
        line += " " + node[TAG]
    print(line)
    counter += 1
    nodes.append(counter)
    if parent is not None:
        edges.append((parent, counter))
    labels[counter] = line
    for child in node[CHILDREN]:
        printTreeEx(child, indent + 1, onlyOR, node)


def printNode(node):
    tag = ""
    if node[TAG] is not None:
        tag = node[TAG]
    print(str(node[TYPE]) + " : " + str(node[STATE]) + " : " +
          str(node[ENV]) + " (" + str(len(node[CHILDREN])) + ") [" + tag + "]")


# Întoarce un arbore al căutării în spațiul env, pornind din starea start
def makeTree(start, env):

    root = ["OR", start, env, [], None, [(start, env)]]

    #TODO
    queue = [root]

    while queue:
        currentNode = queue.pop(0)
        if currentNode[TYPE] == 'OR':
            for move in moves:
                children = [move, currentNode[STATE],
                            currentNode[ENV], [], None, currentNode[PATH]]
                currentNode[CHILDREN].append(children)
                queue.append(children)
        else:
            effects = compute_effectN(
                currentNode[STATE], currentNode[ENV], currentNode[TYPE])
            for effect in effects:
                children = ['OR', effect[0], effect[1],
                            [], None, currentNode[PATH] + [effect]]
                if env_clean(currentNode[ENV]):
                    children[TAG] = 'SUCCESS'
                elif effect in currentNode[PATH]:
                    children[TAG] = 'LOOP'
                else:
                    queue.append(children)
    return root


tree = makeTree(start, env)
print(tree)
printTree(tree, False)


# Întoarce un plan de acțiuni care, conform arborelui ȘI-SAU dat, duc la realizarea scopului. Planul este textual.
# Exemplu: "Clean; if env is [0, 0] then [DONE]; if env is [0, 1] then [Right; Clean]"
def makePlan(node):
    result = ""
    # TODO
    if node[TYPE] == "OR":
        if node[TAG] == "SUCCESS":
            return True
        if node[TAG] == "LOOP":
            return False

        for children in node[CHILDREN]:
            plan = makePlan(children)
            if (not plan == False):
                node[TAG] = "SUCCESS"
                return True
            node[TAG] = "LOOP"
            return False
    else: # if node[TYPE] == "AND"
        for children in node[CHILDREN]:
            plan = makePlan(children)
            if (plan == False):
                node[TAG] = "LOOP"
                return False
        # if logic reached here, than all children returned successfuly 
        node[TAG] = "SUCCESS"
        return True 
    return result


makePlan(tree)
