#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Dimensiunile matricei
from math import sqrt, log
from random import choice
from functools import reduce
from copy import deepcopy
HEIGHT, WIDTH = 6, 7

# Pozițiile din tuplul ce constituie o stare
BOARD, NEXT_PLAYER = 0, 1

# Jucătorii
RED, BLUE = 1, 2
name = ["", "ROȘU", "ALBASTRU", "REMIZĂ"]

# Funcție ce întoarce o stare inițială


def init_state():
    return ([[0 for row in range(HEIGHT)] for col in range(WIDTH)], RED)

# Funcție ce afișează o stare


def print_state(state):
    for row in range(HEIGHT-1, -1, -1):
        ch = " RA"
        l = map(lambda col: ch[state[BOARD][col][row]], range(WIDTH))
        print("|" + "".join(l) + "|")
    print("+" + "".join("-" * WIDTH) + "+")
    print("Urmează: %d - %s" % (state[NEXT_PLAYER], name[state[NEXT_PLAYER]]))


# Se afișează starea inițială a jocului
print("Starea inițială:")
print_state(init_state())

# Funcție ce întoarce acțiunile valide dintr-o stare dată


def get_available_actions(state):
    # TODO <1>
    result = []
    for col in range(WIDTH):
        if 0 in state[BOARD][col]:
            result.append(col)

    return result


# Funcție ce întoarce starea în care se ajunge prin aplicarea unei acțiuni

def apply_action(state, action):
    if action >= len(state[BOARD]) or 0 not in state[BOARD][action]:
        print("Action " + str(action) + " is not valid.")
        return None
    new_board = deepcopy(state[BOARD])
    new_board[action][new_board[action].index(0, 0)] = state[NEXT_PLAYER]
    return (new_board, 3 - state[NEXT_PLAYER])


# Se afișează starea la care se ajunge prin aplicarea unor acțiuni
somestate = reduce(apply_action, [3, 4, 3, 2, 2, 6, 3, 3, 3, 3], init_state())
print_state(somestate)
get_available_actions(somestate)

# Funcție ce verifică dacă o stare este finală


def is_final(state):
    # Verificăm dacă matricea este plină
    if not any([0 in col for col in state[BOARD]]):
        return 3
    # Jucătorul care doar ce a mutat ar putea să fie câștigător
    player = 3 - state[NEXT_PLAYER]

    def ok(pos): return all([state[BOARD][c][r] == player for (r, c) in pos])
    # Verificăm orizontale
    for row in range(HEIGHT):
        for col in range(WIDTH - 4):
            if ok([(row, col + i) for i in range(4)]):
                return player
    # Verificăm verticale
    for col in range(WIDTH):
        for row in range(HEIGHT - 4):
            if ok([(row + i, col) for i in range(4)]):
                return player
    # Verificăm diagonale
    for col in range(WIDTH - 4):
        for row in range(HEIGHT - 4):
            if ok([(row + i, col + i) for i in range(4)]):
                return player
    for col in range(WIDTH-4):
        for row in range(HEIGHT-4):
            if ok([(row + i, col + 4 - i) for i in range(4)]):
                return player
    return False


# Afișăm o stare finală oarecare

rand_state = init_state()
while not is_final(rand_state):
    actions = get_available_actions(rand_state)
    if not actions:
        break
    action = choice(get_available_actions(rand_state))
    rand_state = apply_action(rand_state, action)

print_state(rand_state)
print("Învingător: %s" % (name[is_final(rand_state)]))

# Exemplu: Se afișează starea obținută prin aplicarea unor acțiuni
all_actions = [1, 2, 1, 3, 1, 4, 2, 5]
some_state = reduce(apply_action, all_actions, init_state())
print_state(some_state)
print("Învingător: %s" % (name[is_final(some_state)]))

# Constante

N = 'N'
Q = 'Q'
PARENT = 'parent'
ACTIONS = 'actions'


def print_tree(tree, indent=0):
    if not tree:
        return
    tab = "".join(" " * indent)
    print("%sN = %d, Q = %f" % (tab, tree[N], tree[Q]))
    for a in tree[ACTIONS]:
        print("%s %d ==> " % (tab, a))
        print_tree(tree[ACTIONS][a], indent + 3)

# Funcție ce întoarce un nod nou,
# eventual copilul unui nod dat ca argument


def init_node(parent=None):
    return {N: 0, Q: 0, PARENT: parent, ACTIONS: {}}


CP = 1.0 / sqrt(2.0)

# Funcție ce alege o acțiune dintr-un nod


def select_action(node, c=CP):
    N_node = node[N]

    slectedAction = -1
    maximumScore = -1
    
    # TODO <2>
    # Se caută acțiunea a care maximizează expresia:
    # Q_a / N_a  +  c * sqrt(2 * log(N_node) / N_a)
    for action in node[ACTIONS]:
        q_action = node[ACTIONS][action][Q]
        n_action = node[ACTIONS][action][N]
        
        actionScore = q_action / n_action + c * sqrt(2 * log(N_node) / n_action)
        
        if actionScore > maximumScore:
            maximumScore = actionScore
            slectedAction = action
    return slectedAction


# Scurtă testare
test_root = {N: 6, Q: 0.75, PARENT: None, ACTIONS: {}}
test_root[ACTIONS][3] = {N: 4, Q: 0.9, PARENT: test_root, ACTIONS: {}}
test_root[ACTIONS][5] = {N: 2, Q: 0.1, PARENT: test_root, ACTIONS: {}}

print(select_action(test_root, CP))  # ==> 5 (0.8942 < 0.9965)
print(select_action(test_root, 0.3))  # ==> 3 (0.50895 > 0.45157)

# Algoritmul MCTS (UCT)
#  state0 - starea pentru care trebuie aleasă o acțiune
#  budget - numărul de iterații permis
#  tree - un arbore din explorările anterioare
#  opponent_s_action - ultima acțiune a adversarului


def mcts(state0, budget, tree, opponent_s_action=None):
    # TODO <3>
    # DACĂ există un arbore construit anterior ȘI
    #   acesta are un copil ce corespunde ultimei acțiuni a adversarului,
    if tree is not None and opponent_s_action in tree[ACTIONS]:
        # ATUNCI acel copil va deveni nodul de început pentru algoritm.
        tree = tree[ACTIONS][opponent_s_action]
    
    # ALTFEL, arborele de start este un nod gol.
    else:
        tree = init_node()

    #---------------------------------------------------------------

    for x in range(budget):
        # Punctul de start al simulării va fi rădăcina de start
        state = state0
        node = tree

        # TODO <4>
        while True:
            # Coborâm în arbore până când ajungem la o stare finală
            # sau la un nod cu acțiuni neexplorate.
            possibleActions = get_available_actions(state)

            availableActionsFlag = False
            for action in possibleActions:
                if action not in node[ACTIONS]:
                    availableActionsFlag = True

            if is_final(state) or availableActionsFlag is True:
                break

            selectedAction = select_action(node)
            node = node[ACTIONS][selectedAction]
            state = apply_action(state, selectedAction)
        #---------------------------------------------------------------

        # TODO <5>
        # Dacă am ajuns într-un nod care nu este final și din care nu s-au
        # `încercat` toate acțiunile, construim un nod nou.
        if not is_final(state):
            actions = get_available_actions(state)
            notMadeBeforeActions = []

            for action in actions:
                if action not in node[ACTIONS]:
                    notMadeBeforeActions.append(action)

            chosenAction = choice(notMadeBeforeActions)

            new_node = init_node(node)
            node[ACTIONS][chosenAction] = new_node

            node = new_node
            state = apply_action(state, chosenAction)

        #---------------------------------------------------------------

        # TODO <6>
        # Se simulează o desfășurare a jocului până la ajungerea într-o
        # starea finală. Se evaluează recompensa în acea stare.
        while not is_final(state):
            state = apply_action(state, choice(get_available_actions(state)))

        winner = is_final(state)
        if winner == state0[NEXT_PLAYER]:
            reward = 1
        elif winner == (3 - state0[NEXT_PLAYER]):
            reward = 0.0
        elif winner == 3:
            reward = 0.25
        else:
            reward = 0.5
        #---------------------------------------------------------------

        # TODO <7>

        # Se actualizează toate nodurile de la node către rădăcină:
        while node:
            #  - se incrementează valoarea N din fiecare nod
            node[N] += 1
            #  - se adaugă recompensa la valoarea Q
            node[Q] += reward
            node = node[PARENT]
        #---------------------------------------------------------------

    if tree:
        final_action = select_action(tree, 0.0)
        return (final_action, tree[ACTIONS][final_action])
    # Acest cod este aici doar ca să nu dea erori testele mai jos; în mod normal tree nu trebuie să fie None
    if get_available_actions(state0):
        return (get_available_actions(state0)[0], init_node())
    return (0, None)


# Testare MCTS
(action, tree) = mcts(init_state(), 20, None, None)
print(action)
if tree:
    print_tree(tree[PARENT])


def play_games(games_no, budget1, budget2, verbose=False):
    # Efortul de căutare al jucătorilor
    budget = [budget1, budget2]

    score = {p: 0 for p in name}

    for i in range(games_no):
        # Memoriile inițiale
        memory = [None, None]

        # Se desfășoară jocul
        state = init_state()
        last_action = None

        while state and not is_final(state):
            p = state[NEXT_PLAYER] - 1
            (action, memory[p]) = mcts(
                state, budget[p], memory[p], last_action)
            state = apply_action(state, action)
            last_action = action

        # Cine a câștigat?
        if(state):
            winner = is_final(state)
            score[name[winner]] += + 1

        # Afișăm
        if verbose and state:
            print_state(state)
            if winner == 3:
                print("Remiză.")
            else:
                print("A câștigat %s" % name[winner])

    # Afișează scorul final
    print("Scor final: %s." % (str(score)))


#play_games(5, 2, 30, True)  # ne așteptăm să câștige ALBASTRU
play_games(5, 30, 2, True) # ne așteptăm să câștige ROȘU
