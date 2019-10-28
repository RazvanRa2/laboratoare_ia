#!/usr/bin/env python
# -*- coding: utf-8 -*-

from operator import add
from Lab05tester import test_batch
import Queue
### Reprezentare - construcție

CONSTANT = 'constant'
VARIABLE = 'variable'
FUNCTION = 'function'
ATOM = 'atom'
FORMULA = 'formula'
NEG = 'not'
OR = 'or'
AND = 'and'
# întoarce un termen constant, cu valoarea specificată.


def make_const(value):
    return [CONSTANT, value]

# întoarce un termen care este o variabilă, cu numele specificat.


def make_var(name):
    return [VARIABLE, name, None]

# întoarce un termen care este un apel al funcției specificate, pe restul argumentelor date.
# E.g. pentru a construi termenul add[1, 2, 3] vom apela
#  make_function_call(add, make_const(1), make_const(2), make_const(3))
# !! ATENȚIE: python dă args ca tuplu cu restul argumentelor, nu ca listă. Se poate converti la listă cu list(args)


def make_function_call(function, *args):
    return [FUNCTION, function, list(args)]

# întoarce o formulă formată dintr-un atom care este aplicarea predicatului dat pe restul argumentelor date.
# !! ATENȚIE: python dă args ca tuplu cu restul argumentelor, nu ca listă. Se poate converti la listă cu list(args)


def make_atom(predicate, *args):
    return [FORMULA, ATOM, predicate, list(args)]

# întoarce o formulă care este negarea propoziției date.
# get_args(make_neg(s1)) va întoarce [s1]


def make_neg(sentence):
    return [FORMULA, NEG, [sentence]]
# întoarce o formulă care este conjuncția propozițiilor date (2 sau mai multe).
# e.g. apelul make_and(s1, s2, s3, s4) va întoarce o structură care este conjuncția s1 ^ s2 ^ s3 ^ s4
#  și get_args pe această structură va întoarce [s1, s2, s3, s4]


def make_and(sentence1, sentence2, *others):
    return [FORMULA, AND, [sentence1, sentence2] + list(others)]
# întoarce o formulă care este disjuncția propozițiilor date.
# e.g. apelul make_or(s1, s2, s3, s4) va întoarce o structură care este disjuncția s1 V s2 V s3 V s4
#  și get_args pe această structură va întoarce [s1, s2, s3, s4]


def make_or(sentence1, sentence2, *others):
    return [FORMULA, OR, [sentence1, sentence2] + list(others)]

# întoarce o copie a formulei sau apelul de funcție date, în care argumentele au fost înlocuite
#  cu cele din lista new_args.
# e.g. pentru formula p(x, y), înlocuirea argumentelor cu lista [1, 2] va rezulta în formula p(1, 2).
# Noua listă de argumente trebuie să aibă aceeași lungime cu numărul de argumente inițial din formulă.


def replace_args(formula, new_args):
    if formula[0] == FUNCTION:
        return [FUNCTION, formula[1], list(new_args)]
    elif formula[0] == FORMULA:
        if formula[1] == ATOM:
            return [FORMULA, ATOM, formula[2], list(new_args)]
        else:
            return [formula[0], formula[1], list(new_args)]
    return formula


### Reprezentare - verificare

# întoarce adevărat dacă f este un termen.
def is_term(f):
    return is_constant(f) or is_variable(f) or is_function_call(f)

# întoarce adevărat dacă f este un termen constant.


def is_constant(f):
    return f[0] == CONSTANT

# întoarce adevărat dacă f este un termen ce este o variabilă.


def is_variable(f):
    return f[0] == VARIABLE

# întoarce adevărat dacă f este un apel de funcție.


def is_function_call(f):
    return f[0] == FUNCTION

# întoarce adevărat dacă f este un atom (aplicare a unui predicat).


def is_atom(f):
    return f[0] == FORMULA and f[1] == ATOM

# întoarce adevărat dacă f este o propoziție validă.


def is_sentence(f):
    return f[0] == FORMULA

# întoarce adevărat dacă formula f este ceva ce are argumente.


def has_args(f):
    return is_function_call(f) or is_sentence(f)


### Reprezentare - verificare

# pentru constante (de verificat), se întoarce valoarea constantei; altfel, None.
def get_value(f):
    if is_constant(f):
        return f[1]
    return None

# pentru variabile (de verificat), se întoarce numele variabilei; altfel, None.
def get_name(f):
    if is_variable(f):
        return f[1]
    return None

# pentru apeluri de funcții, se întoarce funcția;
# pentru atomi, se întoarce numele predicatului;
# pentru propoziții compuse, se întoarce un șir de caractere care reprezintă conectorul logic (e.g. ~, A sau V);
# altfel, None
def get_head(f):
    if is_function_call(f):
        return f[1]
    elif f[0] == FORMULA:
        if is_atom(f):
            return f[2]
        else:
            return f[1]
    return None

# pentru propoziții sau apeluri de funcții, se întoarce lista de argumente; altfel, None.
# Vezi și "Important:", mai sus.
def get_args(f):
    if is_function_call(f):
        return f[2]
    elif is_atom(f):
        return f[3]
    elif is_sentence(f):
        return f[2]
    return None

test_batch(0, globals())

# Afișează formula f. Dacă argumentul return_result este True, rezultatul nu este afișat la consolă, ci întors.


def print_formula(f, return_result=False):
    ret = ""
    if is_term(f):
        if is_constant(f):
            ret += str(get_value(f))
        elif is_variable(f):
            ret += "?" + get_name(f)
        elif is_function_call(f):
            ret += str(get_head(f)) + "[" + "".join(
                [print_formula(arg, True) + "," for arg in get_args(f)])[:-1] + "]"
        else:
            ret += "???"
    elif is_atom(f):
        ret += str(get_head(f)) + "(" + \
            "".join([print_formula(arg, True) +
                     ", " for arg in get_args(f)])[:-2] + ")"
    elif is_sentence(f):
        # negation, conjunction or disjunction
        args = get_args(f)
        if len(args) == 1:
            ret += str(get_head(f)) + print_formula(args[0], True)
        else:
            ret += "(" + str(get_head(f)) + \
                "".join([" " + print_formula(arg, True)
                         for arg in get_args(f)]) + ")"
    else:
        ret += "???"
    if return_result:
        return ret
    print(ret)
    return
    return


# Verificare construcție și afișare
# Ar trebui ca ieșirea să fie similară cu: (A (V ~P(?x) Q(?x)) T(?y, <built-in function add>[1,2]))
formula1 = make_and(
    make_or(make_neg(make_atom("P", make_var("x"))),
            make_atom("Q", make_var("x"))),
    make_atom("T", make_var("y"), make_function_call(add, make_const(1), make_const(2))))
print_formula(formula1)

# Aplică în formula f toate elementele din substituția dată și întoarce formula rezultată


def substitute(f, substitution):
    if substitution is None:
        return None
    if is_variable(f) and (get_name(f) in substitution):
        return substitute(substitution[get_name(f)], substitution)
    if has_args(f):
        return replace_args(f, [substitute(arg, substitution) for arg in get_args(f)])
    return f


def test_formula(x, copyy=False):
    fun = make_function_call(add, make_const(1), make_const(2))
    return make_and(make_or(make_neg(make_atom("P", make_const(x))), make_atom("Q", make_const(x))),
                    make_atom("T", fun if copyy else make_var("y"), fun))


# Test (trebuie să se vadă efectele substituțiilor în formulă)
test_batch(1, globals())

# Verifică dacă variabila v apare în termenul t, având în vedere substituția subst.
# Întoarce True dacă v apare în t (v NU poate fi înlocuită cu t), și False dacă v poate fi înlocuită cu t.
def occur_check(v, t, subst):
    if v == t:
        return True
    if get_name(t) in subst:
        return occur_check(v, substitute(t, subst), subst)
    if is_function_call(t):
        for arg in t[2]:
            if occur_check(v, arg, subst):
                return True
    return False

# Test!
test_batch(2, globals())

# Unifică formulele f1 și f2, sub o substituție existentă subst.
# Rezultatul unificării este o substituție (dicționar nume-variabilă -> termen),
#  astfel încât dacă se aplică substituția celor două formule, rezultatul este identic.
def unify(s, t, subst=None):
    if subst is None:
        subst = {}
    S = []
    S.append((s, t))
    while len(S) > 0:
        (s, t) = S.pop()
        
        while get_name(s) in subst:
            s = substitute(s, subst)
        while get_name(t) in subst:
            t = substitute(t, subst)
        
        if not s == t:
            if is_variable(s):
                if occur_check(s, t, subst):
                    return False
                else:
                    subst[get_name(s)] = t
            elif is_variable(t):
                if occur_check(t, s, subst):
                    return False
                else:
                    subst[get_name(t)] = s
            
            elif has_args(s) and has_args(t):
                hs = get_args(s)
                ht = get_args(t)
                
                if get_head(s) == get_head(t) and len(hs) == len(ht):
                    n = len(hs)
                    for _ in range(n):
                        S.append((hs[_], ht[_]))
                else:
                    return False
            else:
                return False
    return subst

# Test!
test_batch(3, globals())
