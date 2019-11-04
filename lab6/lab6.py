#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Lab05 import *
from LPTester import *
from copy import deepcopy
from functools import reduce

# în această celulă se găsesc câteva funcții utilizate intern

dummy = make_atom("P")
[and_name, or_name, neg_name] = [get_head(s) for s in [make_and(dummy, dummy), make_or(dummy, dummy), make_neg(dummy)]]
def pFail(message, f):
    print(message + " <" + str(f) + ">")
    return False
def check_term(T):
    if is_constant(T):
        return (get_value(T) is not None) or pFail("The value of the constant is None", T)
    if is_variable(T):
        return (get_name(T) is not None) or pFail("The name of the variable is None", T)
    if is_function_call(T):
        return not [t for t in get_args(T) if not check_term(t)] and \
            (get_head(T) is not None or pFail("Function is not callable", T))
    return pFail("Term is not one of constant, variable or function call", T)
def check_atom(A):
    if is_atom(A):
        return not [t for t in get_args(A) if not check_term(t)] and \
            (get_head(A) is not None or pFail("Predicate name is None", A))
    return pFail("Is not an atom", A)
def check_sentence(S):
    if is_atom(S):
        return check_atom(S)
    if is_sentence(S):
        if get_head(S) in [and_name, or_name]:
            return (len(get_args(S)) >= 2 or pFail("Sentence has too few operands", S)) \
                and not [s for s in get_args(S) if not check_sentence(s)]
        if get_head(S) == neg_name:
            return (len(get_args(S)) == 1 or pFail("Negative sentence has not just 1 operand", S)) \
                and check_sentence(get_args(S)[0])
    return pFail("Not sentence or unknown type", S)

def add_statement(kb, conclusion, *hypotheses):
    s = conclusion if not hypotheses else make_or(*([make_neg(s) for s in hypotheses] + [conclusion]))
    if check_sentence(s):
        kb.append(s)
        print("OK: Added statement " + print_formula(s, True))
        return True
    print("-- FAILED CHECK: Sentence does not check out <"+print_formula(s, True)+"><" + str(s) + ">")
    return False

var_no = 0;

def assign_next_var_name():
    global var_no
    var_no += 1
    return "v" + str(var_no)

def gather_vars(S):
    return [get_name(S)] if is_variable(S) else \
        [] if not has_args(S) else reduce(lambda res, a: res + gather_vars(a), get_args(S), [])

def make_unique_var_names(KB):
    global var_no
    var_no = 0
    return [substitute(S, {var: make_var(assign_next_var_name()) for var in gather_vars(S)}) for S in KB]           
            
def print_KB(KB):
    print("KB now:")
    for s in KB:
        print("\t\t\t" + print_formula(s, True))
from LPTester import *
from Lab05 import *
from copy import deepcopy
from functools import reduce

# în această celulă se găsesc câteva funcții utilizate intern

dummy = make_atom("P")
[and_name, or_name, neg_name] = [get_head(s) for s in [make_and(
    dummy, dummy), make_or(dummy, dummy), make_neg(dummy)]]


def pFail(message, f):
    print(message + " <" + str(f) + ">")
    return False


def check_term(T):
    if is_constant(T):
        return (get_value(T) is not None) or pFail("The value of the constant is None", T)
    if is_variable(T):
        return (get_name(T) is not None) or pFail("The name of the variable is None", T)
    if is_function_call(T):
        return not [t for t in get_args(T) if not check_term(t)] and \
            (get_head(T) is not None or pFail("Function is not callable", T))
    return pFail("Term is not one of constant, variable or function call", T)


def check_atom(A):
    if is_atom(A):
        return not [t for t in get_args(A) if not check_term(t)] and \
            (get_head(A) is not None or pFail("Predicate name is None", A))
    return pFail("Is not an atom", A)


def check_sentence(S):
    if is_atom(S):
        return check_atom(S)
    if is_sentence(S):
        if get_head(S) in [and_name, or_name]:
            return (len(get_args(S)) >= 2 or pFail("Sentence has too few operands", S)) \
                and not [s for s in get_args(S) if not check_sentence(s)]
        if get_head(S) == neg_name:
            return (len(get_args(S)) == 1 or pFail("Negative sentence has not just 1 operand", S)) \
                and check_sentence(get_args(S)[0])
    return pFail("Not sentence or unknown type", S)


def add_statement(kb, conclusion, *hypotheses):
    s = conclusion if not hypotheses else make_or(
        *([make_neg(s) for s in hypotheses] + [conclusion]))
    if check_sentence(s):
        kb.append(s)
        print("OK: Added statement " + print_formula(s, True))
        return True
    print("-- FAILED CHECK: Sentence does not check out <" +
          print_formula(s, True)+"><" + str(s) + ">")
    return False


var_no = 0


def assign_next_var_name():
    global var_no
    var_no += 1
    return "v" + str(var_no)


def gather_vars(S):
    return [get_name(S)] if is_variable(S) else \
        [] if not has_args(S) else reduce(
            lambda res, a: res + gather_vars(a), get_args(S), [])


def make_unique_var_names(KB):
    global var_no
    var_no = 0
    return [substitute(S, {var: make_var(assign_next_var_name()) for var in gather_vars(S)}) for S in KB]


def print_KB(KB):
    print("KB now:")
    for s in KB:
        print("\t\t\t" + print_formula(s, True))


# KB 1
# based on an example in Artificial Intelligence - A Modern Approach
KB_America = []
#0 Mr West is a US general
add_statement(KB_America, make_atom("USGeneral", make_const("West")))
#1 General Awesome is also a US general
add_statement(KB_America, make_atom(
    "USGeneral", make_const("General_Awesome")))
#2 General Awesome is Awesome
add_statement(KB_America, make_atom("Awesome", make_const("General_Awesome")))
#3 Nono is an enemy of America
add_statement(KB_America, make_atom(
    "Enemy", make_const("Nono"), make_const("America")))
#4 M1 is a type of missile
add_statement(KB_America, make_atom("Missile", make_const("M1")))
#5 Nono has the M1 missile
add_statement(KB_America, make_atom(
    "Owns", make_const("Nono"), make_const("M1")))

#6 any US general is an American
add_statement(KB_America, make_atom("American", make_var("x")),
              make_atom("USGeneral", make_var("x")))
#7 any missle is a weapon
add_statement(KB_America, make_atom("Weapon", make_var("x")),
              make_atom("Missile", make_var("x")))
#8 if anyone owns a missile, it is General West that sold them that missile
add_statement(KB_America, make_atom("Sells", make_const("West"), make_var("y"), make_var(
    "x")), make_atom("Owns", make_var("x"), make_var("y")), make_atom("Missile", make_var("y")))
#9 any American who sells weapons to a hostile is a criminal
add_statement(KB_America, make_atom("Criminal", make_var("x")), make_atom("Weapon", make_var("y")), make_atom(
    "Sells", make_var("x"), make_var("y"), make_var("z")), make_atom("Hostile", make_var("z")), make_atom("American", make_var("x")))
#10 any enemy of America is called a hostile
add_statement(KB_America, make_atom("Hostile", make_var("x")),
              make_atom("Enemy", make_var("x"), make_const("America")))
#11 America is awesome if at least an American is awesome
add_statement(KB_America, make_atom("Awesome", make_const("America")), make_atom(
    "American", make_var("x")), make_atom("Awesome", make_var("x")))

KB_America = make_unique_var_names(KB_America)

print_KB(KB_America)

# KB 2
# din cursul de IA
KB_Faster = []


def the_greyhound():
    return make_const("Greg")


#0 horses are faster than dogs
add_statement(KB_Faster, make_atom("Faster", make_var("x"), make_var(
    "y")), make_atom("Horse", make_var("x")), make_atom("Dog", make_var("y")))
#1 there is a greyhound that is faster than any rabbit
add_statement(KB_Faster, make_atom("Faster", make_function_call(
    the_greyhound), make_var("z")), make_atom("Rabbit", make_var("z")))
#2 Harry is a horse
add_statement(KB_Faster, make_atom("Horse", make_const("Harry")))
#3 Ralph is a rabbit
add_statement(KB_Faster, make_atom("Rabbit", make_const("Ralph")))
#4 Greg is a greyhound
add_statement(KB_Faster, make_atom(
    "Greyhound", make_function_call(the_greyhound)))
#5 A greyhound is a dog
add_statement(KB_Faster, make_atom("Dog", make_var("y")),
              make_atom("Greyhound", make_var("y")))
#6 transitivity
add_statement(KB_Faster, make_atom("Faster", make_var("x"), make_var("z")),
              make_atom("Faster", make_var("x"), make_var("y")), make_atom("Faster", make_var("y"), make_var("z")))

KB_Faster = make_unique_var_names(KB_Faster)

print_KB(KB_Faster)

KB_test = []
add_statement(KB_test, make_atom("Q", make_var("x")),
              make_atom("P", make_var("x")))
add_statement(KB_test, make_atom("P", make_const("A")))

KB_test = make_unique_var_names(KB_test)
print_KB(KB_test)


def is_positive_literal(L):
    return is_atom(L)


def is_negative_literal(L):
    global neg_name
    return get_head(L) == neg_name and is_positive_literal(get_args(L)[0])


def is_literal(L):
    return is_positive_literal(L) or is_negative_literal(L)


def unify_literals(L1, L2):
    if is_positive_literal(L1) == is_positive_literal(L2):
        return False
    elif is_positive_literal(L1):
        return unify(make_neg(L1), L2)
    elif is_positive_literal(L2):
        return unify(L1, make_neg(L2))
    else:
        return False


def resolves(C1, C2):
    #print("testing " + print_formula(C1, True) + " and " + print_formula(C2, True))

    # întoarce un tuplu (literal-din-C1, literal-din-C2, substituție)
    # unde literal-din-C1 și literal-din-C2 unifică sub substituție

    if (is_literal(C1) and is_literal(C2)):
        subst = unify_literals(C1, C2)
        if subst is not False:
            return (C1, C2, subst)
    
    elif is_literal(C1):
        for arg in get_args(C2):
            subst = unify_literals(C1, arg)
            if subst is not False:
                return (C1, arg, subst)
    
    elif is_literal(C2):
        for arg in get_args(C2):
            subst = unify_literals(C2, arg)
            if subst is not False:
                return (arg, C2, subst)
    
    else:
        for arg1 in get_args(C1):
            for arg2 in get_args(C2):
                subst = unify_literals(arg1, arg2)
                if subst is not False:
                    return (arg1, arg2, subst)

    return False


# Test!
test_batch(4, globals())

# prints a 5-tuple resolvent representation (see below)


def print_r(R):
    if R is None:
        print("no resolvent")
    else:
        print("resolvent: " + print_formula(R[2], True) + "/" + print_formula(R[3], True)
              + " {" + ", ".join([(k + ": " + str(R[4][k]))
                                  for k in R[4]]) + "}"
              + "\n\t\t in " + print_formula(R[0], True) + "\n\t\t and " + print_formula(R[1], True))


VOID_CLAUSE = "The void clause"


def new_clause(resolvent):
    C1, C2, L1, L2, subst = resolvent
    C = None

    if (resolves(C1,C2) is False):
        return VOID_CLAUSE

    if is_literal(C1) and is_literal(C2):
        C = VOID_CLAUSE

    elif is_literal(C1):
        C2_args = get_args(C2)
        C2_args.remove(L2)
        C2_aux = replace_args(C2, C2_args)
        C2_aux = substitute(C2_aux, subst)
        #print_formula(C2_aux)

        if (C2_aux[1] == OR and len(get_args(C2_aux)) == 1):
            C2_aux = get_args(C2_aux)[0]

        C = C2_aux

    elif is_literal(C2):
        C1_args = get_args(C1)
        C1_args.remove(L1)
        C1_aux = replace_args(C1, C1_args)
        C1_aux = substitute(C1_aux, subst)
        print_formula(C1_aux)

        if (C1_aux[1] == OR and len(get_args(C1_aux)) == 1):
            C1_aux = get_args(C1_aux)[0]
        C = C1_aux

    else:
        C1_args = get_args(C1)
        C2_args = get_args(C2)
        C1_args.remove(L1)
        C2_args.remove(L2)
        C1_aux = replace_args(C1, C1_args)
        C2_aux = replace_args(C2, C2_args)
        C1_aux = substitute(C1_aux, subst)
        C2_aux = substitute(C2_aux, subst)
    
        if (C2_aux[1] == OR and len(get_args(C2_aux)) == 1):
            C2_aux = get_args(C2_aux)[0]

        if (C1_aux[1] == OR and len(get_args(C1_aux)) == 1):
            C1_aux = get_args(C1_aux)[0]

        C = C1_aux + C2_aux

    print_formula(C)
    return C


# Test!
test_batch(5, globals())


def solve_problem(hypotheses, conclusion):
    KB = hypotheses[:]
    # puteți adăuga și la sfârșit (în funcție de strategie)
    KB = [make_neg(conclusion)] + KB
    Effort = 50  # puteți crește efortul dacă este necesar

    while Effort > 0:
        Effort -= 1

        # Se aleg două clauze Clauza1 și Clauza2, care nu au mai fost alese anterior

        # Se calculează un rezolvent, ca tuplu (Clauza1, Clauza2, Literal-din-clauza1, Literal-din-clauza2, substituție)
        
        resolvent = None # TODO
        upper_break = False
        for clause1 in KB:
            for clause2 in KB:
                check = resolves(clause1, clause2)
                if check is not False:
                    (l1, l2, subst) = check
                    upper_break = True
                    resolvent = (clause1, clause2, l1, l2, subst)
                    break 
            if upper_break:
                break

        print_r(resolvent)   

        if resolvent is None:
            print("Failed. No resolving clauses. Effort left " + str(Effort))
            return False

        # Se calculează noua clauză de adăugat și se adaugă la baza de cunoștințe

        C = new_clause(resolvent)

        if C == VOID_CLAUSE:
            print("Done (effort left " + str(Effort) + ")")
            return True

        # update KB
        print("Added: " + print_formula(C, True))
        KB = [C] + KB

        print_KB(KB)
    print("Failed. Effort exhausted.")


#print_KB(KB_test)
solve_problem(deepcopy(KB_test), make_atom("Q", make_const("A")))
#print("==========================================")

#print_KB(KB_America)
solve_problem(deepcopy(KB_America), make_atom("Criminal", make_const("West")))
#print("==========================================")

#print_KB(KB_Faster)
solve_problem(deepcopy(KB_Faster), make_atom("Faster", make_const("Harry"), make_const("Ralph")))
print("==========================================")
