#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import reduce
import operator
NOT_PARTICLE = "NOT_"
PERSISTENCE_PARTICLE = "____"
PARTICLE_LENGTH = len(NOT_PARTICLE)

TYPE = "type"
STATE = "state"
ACTIONS = "actions"
MUTEX = "mutex"

# Calculează opusul lui P


def opposite(P):
    if P[:PARTICLE_LENGTH] == NOT_PARTICLE:
        return P[PARTICLE_LENGTH:]
    else:
        return NOT_PARTICLE + P


def NOT(P):
    return opposite(P)


print(NOT("Fact"))
print(NOT(NOT("Fact")))
print(NOT(NOT(NOT("Fact"))))

# Problemele din AIMA (pagina 396 pentru prima problemă; paginile 391 și 399 pentru a doua):

# How to perform two actions in order?
Basic = {}
Basic['init'] = ["NothingDone", NOT("PhaseOneDone"), NOT("PhaseTwoDone")]
Basic['goal'] = ["PhaseTwoDone"]
Basic['actions'] = {}
Basic['actions']["PhaseOne"] = ([], ["PhaseOneDone"])
Basic['actions']["PhaseTwo"] = (["PhaseOneDone"], ["PhaseTwoDone"])

# How to have cake and eat it too?
Cake = {}
Cake['init'] = ["HaveCake", NOT("EatenCake")]
Cake['goal'] = ["EatenCake", "HaveCake"]
Cake['actions'] = {}
Cake['actions']["EatCake"] = (["HaveCake"], [NOT("HaveCake"), "EatenCake"])
Cake['actions']["BakeCake"] = ([NOT("HaveCake")], ["HaveCake"])

# How to solve the problem of a flat tire?
FlatTire = {}
FlatTire['init'] = ["At(Flat,Axle)", "At(Spare,Trunk)", NOT(
    "At(Flat,Ground)"), NOT("At(Spare,Axle)"), NOT("At(Spare,Ground)")]
FlatTire['goal'] = ["At(Spare,Axle)"]
FA = {}
FA["Remove(Spare,Trunk)"] = (["At(Spare,Trunk)"], [
    NOT("At(Spare,Trunk)"), "At(Spare,Ground)"])
FA["Remove(Flat,Axle)"] = (["At(Flat,Axle)"], [
    NOT("At(Flat,Axle)"), "At(Flat,Ground)"])
FA["PutOn(Spare,Axle)"] = (["At(Spare,Ground)", NOT("At(Flat,Axle)")], [
    "At(Spare,Axle)", NOT("At(Spare,Ground)")])
FlatTire['actions'] = FA

# întoarce adevărat dacă setul smaller este inclus în setul bigger


def included(smaller, bigger):
    for x in smaller:
        if not x in bigger:
            return False
    return True

# întoarce adevărat dacă elementele el1 și el2 sunt mutal exclusive, conform listei mutex


def isMutex(el1, el2, mutex):
    return (el1, el2) in mutex or (el2, el1) in mutex

# întoarce adevărat dacă nu există în lista to_check nicio pereche de acțiuni mutual exclusive


def notAnyMutex(to_check, mutex):
    for x in to_check:
        for y in to_check:
            if isMutex(x, y, mutex):
                return False
    return True

# întoarce adevărat dacă o acțiune este de tip 'No OPeration'


def isNop(act):
    return len(act) > PARTICLE_LENGTH and act[:PARTICLE_LENGTH] == PERSISTENCE_PARTICLE

# întoarce faptul care este rezultatul unei acțiuni de tip 'No OPeration'


def removeNop(act):
    if isNop(act):
        return act[PARTICLE_LENGTH:]
    return False

# crează o acțiune de tip 'No OPeration', pe baza unui fapt


def makeNop(fact):
    return PERSISTENCE_PARTICLE + fact

# afișează graful.


def print_graph(graph, startLevel=0, indent=""):
    l = startLevel
    for level in graph:
        print(indent + "[ " + str(l) + " ] " + level[TYPE] + ":")
        for element in level[level[TYPE]]:
            out = indent + "\t" + element + "; mutex with "
            found = False
            for e in level[level[TYPE]]:
                if isMutex(e, element, level[MUTEX]):
                    out += e + ", "
                    found = True
            out = out + "None" if not found else out[:-2]
            print(out)
        l = l + 1
#print(included("abc", "adecbf"))
#print(included("abc", "adecf"))


DEBUG = False


def printd(i, *args):
    if DEBUG:
        pass
        #print(i, *args)

# întoarce adevărat dacă toate scopurile din goals se găsesc în ultimul nivel din graf și nu sunt mutual exclusive


def Maybe_completed(goals, graph):
    lLevel = len(graph) - 1
    if graph[lLevel][TYPE] != STATE:
        return False
    state = graph[lLevel][STATE]
    return included(goals, state) and notAnyMutex(goals, graph[lLevel][MUTEX])

# extrage soluția unei probleme, folosind un graf de planificare deja construit


def Extract_solution(goals, graph, problem, indent="\t"):
    global allgoals, allpotentialactions
    printd(indent, "=== checking; goals:", goals)
    if DEBUG:
        print_graph(graph, indent=indent)
    if len(graph) == 1:
        if included(goals, graph[0][STATE]):
            printd(indent, "## Done")
        return [] if included(goals, graph[0][STATE]) else False
    actions = graph[len(graph) - 2][ACTIONS]
    mutex_actions = graph[len(graph) - 2][MUTEX]
    all_actions = problem[ACTIONS]
    potential_actions = []
    first = True
    # all possible actions combinations
    allgoals += len(goals)
    for g in goals:
        goal_actions = [a for a in actions if removeNop(
            a) == g or (not isNop(a) and g in all_actions[a][1])]
        if first:
            potential_actions = [[a] for a in goal_actions]
            first = False
        else:
            pa = potential_actions
            potential_actions = []
            for a in goal_actions:
                for aa in pa:
                    potential_actions.append((aa + [a]) if a not in aa else aa)
        printd(indent, "## potential actions after checking goal",
               g, ":", potential_actions)
    # not-mutex actions
    printd(indent, "## all potential actions:", potential_actions)
    potential_actions = [
        comb for comb in potential_actions if notAnyMutex(comb, mutex_actions)]
    printd(indent, "## potential non-mutex actions:", potential_actions)
    allpotentialactions += reduce(operator.add,
                                  [len(a) for a in potential_actions], 0)
    for comb in potential_actions:
        new_goals = []
        for act in comb:
            if isNop(act):
                if removeNop(act) not in new_goals:
                    new_goals.append(removeNop(act))
            else:
                new_goals.extend(
                    [precond for precond in all_actions[act][0] if precond not in new_goals])
        printd(indent, "## attempt: actions:", comb)
        result = Extract_solution(
            new_goals, graph[:-2], problem, indent + ">\t")
        printd(indent, "## Result:", result)
        if result != False:
            return result + comb
    return False

# Construiește următoarele două niveluri (un nivel acțiune și un nivel stare) dintr-un graf de planificare,
#  pe baza ultimului nivel existent, care este de stare.
# Se dă lista tuturor acțiunilor descrise în problemă, ca un dicționar acțiune -> (precondiții, efecte)
# Funcția întoarce un tuplu format din cele două niveluri nou create.


def Extend_graph(graph, all_actions):
    lastLevel = len(graph) - 1
    # ultimul nivel din graf
    state = graph[lastLevel][STATE]
    mutex = graph[lastLevel][MUTEX]

    # Se creează următorul nivel după cele date: acțiunile disponibile pe nivelul de stare precedent

    # se calculează acțiunile aplicabile: toate acțiunile ale căror precondiții
    #  există în starea precedentă și nu sunt mutual exclusive (vezi funcția notAnyMutex).
    # Stocați acțiunile disponibile ca un dicționar nume -> (listă precondiții, listă efecte)

    # se adaugă acțiunile de tip 'No OPeration'
    actions = {makeNop(fact): ([fact], [fact]) for fact in state}
    # TODO: adăugați celelalte acțiuni disponibile

    for action in all_actions:
        preconditions = all_actions[action][0]

        if notAnyMutex(preconditions, mutex) and included(preconditions, state):
            actions[action] = all_actions[action]

# se calculează acțiunile mutual exclusive
    mutex_actions = []
    # TODO

    for a1 in actions:
        for a2 in actions:
            if a1 == a2:
                continue
                
            for a in actions[a1][0]:
                for b in actions[a2][0]:
                    if isMutex(a, b, mutex) or a == NOT(b):
                        mutex_actions.append((a1, a2))
                
            for a in actions[a1][1]:
                for b in actions[a2][1]:
                    if  a == NOT(b):
                        mutex_actions.append((a1, a2))
            
            for a in actions[a1][0]:
                for b in actions[a2][1]:
                    if a == NOT(b):
                        mutex_actions.append((a1, a2))

            for a in actions[a1][1]:
                for b in actions[a2][0]:
                    if a == NOT(b):
                        mutex_actions.append((a1, a2))

    # printuri utile
    #print("mutex " + str((a1,a2)) + ": inconsistent effects <" + effect + "> of " + a1 + " and <" + NOT(effect) + "> of " + a2)
    #print("mutex " + str((a1,a2)) + ": interferring precondition <" + precond + "> of " + a1 + " and effect <" + NOT(precond) + "> of " + a2)
    #print("mutex " + str((a1,a2)) + ": competing preconditions (needs) <" + precond + "> of " + a1 + " and <" + NOT(precond) + "> of " + a2)

    # Se creează al doilea următor nivel după cele date: starea generată de nivelul precedent de acțiuni

    # se calculează efectele acțiunilor de pe nivelul precedent
    # Stocați efectele ca un dicționar fapt -> listă acțiuni care produc efectul
    effects = {}
    # TODO
    for action in actions:
        for action_effect in actions[action][1]:
            if action_effect not in effects:
                effects[action_effect] = []
            effects[action_effect].append(action)

    # se calculează efectele mutual exclusive:
    # 2 efecte sunt mutex dacă nu pot rezulta din acțiuni care nu sunt mutual exclusive
    mutex_effects = []
    # TODO

    for e1 in effects:
        for e2 in effects:
            if e1 == e2:
                continue
            
            mutex_flag = True

            for a1 in effects[e1]:
                for a2 in effects[e2]:
                    if not isMutex(a1,a2, mutex_actions):
                        mutex_flag = False
            
            if mutex_flag is True:
                mutex_effects.append((e1,e2))

    # rezultat: ultimele două niveluri din graf, ca un tuplu
    return ({TYPE: ACTIONS, ACTIONS: actions.keys(), MUTEX: mutex_actions},
            {TYPE: STATE, STATE: effects.keys(), MUTEX: mutex_effects})


def Plan(Problem):
    LIMIT = 10
    graph = [{TYPE: STATE, STATE: Problem['init'], MUTEX: []}]
    print("first level: ")
    print_graph(graph)
    cLevel = 0

    while cLevel < LIMIT:
        if Maybe_completed(Problem['goal'], graph):
            solution = Extract_solution(Problem['goal'], graph, Problem)
            if solution:
                return [a for a in solution if not isNop(a)]
        print("======")
        new_levels = Extend_graph(graph, Problem['actions'])
        graph.extend(new_levels)
        print("new levels:")
        print_graph(graph[-2:], cLevel + 1)
        cLevel += 2
    if cLevel == LIMIT:
        print("## Limit reached.")
    return False


tests = [Basic, Cake, FlatTire]
solutions = [['PhaseOne', 'PhaseTwo'], ['EatCake', 'BakeCake'],
             ['Remove(Spare,Trunk)', 'Remove(Flat,Axle)', 'PutOn(Spare,Axle)']]
goal_efficiency = [[2, 2], [4, 3], [3, 3]]
for i in range(len(tests)):
    allgoals, allpotentialactions = 0, 0
    sol = Plan(tests[i])
    print("\n## Solution: " + str(sol))
    if sol == solutions[i]:
        print("## OK, solution found.")
        ideal_goals, ideal_actions = goal_efficiency[i]
        if allgoals > ideal_goals:
            print("BUT, there were", allgoals,
                  "goals generated instead of", ideal_goals)
        if allpotentialactions > ideal_actions:
            print("BUT, there were", allpotentialactions,
                  "action branches generated instead of", ideal_actions)
#         print("Goals", allgoals, "Potential actions", allpotentialactions)
        if i == len(tests) - 1:
            print("all done.")
    else:
        print("## NOT OK. Should be: " + str(solutions[i]))
        if i < len(tests) - 1:
             print("Solve this before moving on.")
        break
    print("\n===========================================")
