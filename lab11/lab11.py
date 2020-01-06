#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import choice, randint

D = 'Defect'
C = 'Cooperate'

rewards = {(C, C): (3, 3), (C, D): (0, 5), (D, C): (5, 0), (D, D): (2, 2)}

# O strategie de joc este caracterizată de o funcție care întoarce, la fiecare apel, acțiunea aleasă de strategie.
# Parametrul primit de funcție este o listă de tupluri care conține acțiunile jucate anterior în cursul aceluiași
# joc iterat.
# Fiecare tuplu din listă corespunde unui joc individual de dilema prizonierului și conține pe prima poziție
# acțiunea aleasă de acest agent și pe a doua acțiunea jucată de oponent.


def AllD(_):
    return D


def Random(_):
    return choice([D,C])


def TFT(information):
    if (information) == []:
        return C

    last_game_strategy = information[-1]
    mystrategy, oponentstrategy = last_game_strategy
    return oponentstrategy

jossroundcnt = 1
oponentDefected = False

def Joss(information):
    global jossroundcnt
    global oponentDefected

    if (jossroundcnt % 3 == 0):
        jossroundcnt += 1
        return D
    else:
        if (oponentDefected == True):
            return TFT(information)

    if (information == []):
        jossroundcnt += 1
        return C

    last_game_strategy = information[-1]
    mystrategy, oponentstrategy = last_game_strategy
    if (oponentstrategy == D):
        oponentDefected = True
        return TFT(information)

    jossroundcnt += 1
    return C

wantsToCooperateCount = 1
def Tester(information):
    global wantsToCooperateCount
    testerAnswer = None
    jossAnswer = Joss(information)
    if (jossAnswer == C and wantsToCooperateCount % 10 == 0):
        jossAnswer = D
    if (jossAnswer == C):
        wantsToCooperateCount += 1
    testerAnswer = jossAnswer
    
    return testerAnswer

# so sorry detective
def Lucifer(_):
    return D

dflag = False
def MassiveRetaliatoryStrike(information):
    global dflag

    if (information == []):
        return C
    
    last_game_strategy = information[-1]
    mystrategy, oponentstrategy = last_game_strategy
    
    if (oponentstrategy == 'D'):
        dflag = True
    
    if (dflag):
        return D

    return C

tftcnt = 1
def gTFT(information):
    global tftcnt
    tftRes = TFT(information)

    if tftRes == D:
        tftcnt += 1

        if (tftcnt % 5 == 0):
            return C
    
    return tftRes

eviltftcnt = 1
def evilTFT(information):
    global eviltftcnt

    tftRes = TFT(information)

    if tftRes == C:
        eviltftcnt += 1

        if (eviltftcnt % 20 == 0):
            return D
    
    return tftRes

tftBetrayed = False
def activEvilTFT(information):
    global tftBetrayed

    tftRes = TFT(information)

    if tftRes == D:
        tftBetrayed = True

    if tftBetrayed == True:
        return Joss(information)
        
    return tftRes

# TODO de activat strategiile aici
availableStrategies = [
    ('All-D', AllD),
    ('Random', Random),
    ('Tit-For-Tat', TFT),
    ('Joss', Joss),
    ('Tester', Tester),
    #('Lucifer', Tester),
    #('MRS', MassiveRetaliatoryStrike),
    #('Generous TFT', gTFT),
    #('Evil TFT', evilTFT),
    ('Activatable Evil TFT', activEvilTFT)
]

strategies = []
for (name, proc) in availableStrategies:
    strategies.append({'name': name, 'procedure': proc,
                       'wins': 0, 'score': 0, 'games': 0, 'plays': {}})

# joacă un joc între A și B, întoarce recompensele asociate


def play_game(players, verbose=False):
    choices = [p['strategy']['procedure'](p['information']) for p in players]
    for i in range(2):
        players[i]['information'].append((choices[i], choices[1 - i]))
    if verbose:
        print(players[0]['strategy']['name']+" vs "+players[1]['strategy']['name'] +
              " choices: "+str(choices)+" rewards: "+str(rewards[tuple(choices)]))
    return rewards[tuple(choices)]

# joacă `iterations` jocuri între A și B, întorcând scorul asociat întregului joc iterat


def play_iterated_pd(players, n_iterations, verbose=False):
    score = (0, 0)
    for i in range(n_iterations):
        rewardsAB = play_game(players, verbose)
        score = tuple([score[pi] + rewardsAB[pi] for pi in range(2)])
    if verbose:
        print("== result: "+str(score))
    return score

# joacă un turneu de n jocuri de câte n iterații, alegând aleator între strategiile date în `strategies`


def tournament(n_games, n_iterations, strategies, verbose=False):
    for game in range(n_games):
        agents = []
        strat = []
        for i in range(2):
            agents.append({'strategy': choice(strategies), 'information': []})
            strat.append(agents[i]['strategy'])
        for i in range(2):
            for j in range(2):
                if i != j:
                    if strat[j]['name'] not in strat[i]['plays']:
                        strat[i]['plays'][strat[j]['name']] = 1
                    else:
                        strat[i]['plays'][strat[j]['name']] += 1
        scores = play_iterated_pd(agents, n_iterations, verbose)
        result = (0, 0)
        if scores[0] > scores[1]:
            result = (1, 0)
        if scores[0] < scores[1]:
            result = (0, 1)
        for i in range(2):
            strat[i]['wins'] += result[i]
            strat[i]['score'] += scores[i]
            strat[i]['games'] += 1
    print('\n\n================ total games: ' + str(n_games))
    for s in strategies:
        print('\n strategy ' + s['name'])
        if s['games']:
            plays = ' played against '
            for s_op in strategies:
                if s_op['name'] in s['plays']:
                    plays += s_op['name'] + \
                        ' (' + str(s['plays'][s_op['name']]) + ') '
            print('\t' + plays)
            print(
                '\t played '+str(s['games'])+' times and won '+str(s['wins'])+' times with a global score of '+str(s['score']) +
                '\n\t score/games: '+str(round(float(s['score'])/s['games'], 2)) +
                '\t wins/games: '+str(round(float(s['wins'])/s['games'], 2)) +
                '\t score/wins: '+(str(round(float(s['score'])/s['wins'], 2)) if s['wins'] else "--"))
        else:
            print("\t played no games.")


# tournament(50, 10, strategies, True) # test, with Verbose
tournament(500, 100, strategies)  # short
tournament(5000, 100, strategies)  # long
