#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Lab05 import make_var, make_const, make_atom, make_or, make_neg, \
    is_variable, is_constant, is_atom, is_function_call, \
    print_formula, get_args, get_head, get_name, get_value,\
    unify, substitute
from Lab07fct import add_statement, is_positive_literal, is_negative_literal, \
    make_unique_var_names, print_KB
from LPTester import *


def get_sports_kb():
    sports_kb = []
    # Predicatul 'Consecutive'
    add_statement(sports_kb, make_atom(
        'Consecutive', make_const('Luni'), make_const('Marti')))
    add_statement(sports_kb, make_atom(
        'Consecutive', make_const('Marti'), make_const('Miercuri')))
    add_statement(sports_kb, make_atom(
        'Consecutive', make_const('Miercuri'), make_const('Joi')))
    add_statement(sports_kb, make_atom(
        'Consecutive', make_const('Joi'), make_const('Vineri')))
    add_statement(sports_kb, make_atom(
        'Consecutive', make_const('Vineri'), make_const('Sambata')))
    add_statement(sports_kb, make_atom(
        'Consecutive', make_const('Sambata'), make_const('Duminica')))
    # Predicatul 'Weekend'
    add_statement(sports_kb, make_atom('Weekend', make_const('Sambata')))
    add_statement(sports_kb, make_atom('Weekend', make_const('Duminica')))
    # Predicatul 'Ploua'
    add_statement(sports_kb, make_atom('Ploua', make_const('Vineri')))
    # TODO 2.1: Dacă a plouat două zile la rând, a treia zi va fi frumos.
    #

    add_statement(sports_kb, 
        make_atom('Ploua', make_var('day1')),
        make_atom('Ploua', make_var('day2')),
        make_atom('Frumos', make_var('day3')),
        make_atom('Consecutive', make_var('day1'), make_var('day2')),
        make_atom('Consecutive', make_var('day2'), make_var('day3')))
    # Predicatul 'Frumos'
    add_statement(sports_kb, make_atom('Frumos', make_const('Luni')))
    add_statement(sports_kb, make_atom('Frumos', make_const('Marti')))
    add_statement(sports_kb, make_atom('Frumos', make_const('Miercuri')))
    # TODO 2.2: Dacă a fost frumos trei zile la rând, în cea de-a patra zi va ploua.
    #

    add_statement(sports_kb,
                  make_atom('Ploua', make_var('day4')),
                  make_atom('Frumos', make_var('day1')),
                  make_atom('Frumos', make_var('day2')),
                  make_atom('Frumos', make_var('day3')),
                  make_atom('Consecutive', make_var('day1'), make_var('day2')),
                  make_atom('Consecutive', make_var('day2'), make_var('day3')),
                  make_atom('Consecutive', make_var('day3'), make_var('day4')))

    # Predicatul 'Student'
    add_statement(sports_kb, make_atom('Student', make_const('Nectarie')))
    add_statement(sports_kb, make_atom('Student', make_const('Arsenie')))
    # MergeLaMunte (cine, cand)
    # TODO 2.3: Un student merge întotdeauna la munte dacă este frumos într-o zi de weekend.
    #
    add_statement(sports_kb,
                  make_atom('MergeLaMunte', make_var('x'), make_var('y')),
                  make_atom('Student', make_var('x')),
                  make_atom('Frumos', make_var('y')),
                  make_atom('Weekend', make_var('y')))
    # Predicatul 'SportDeVara'
    add_statement(sports_kb, make_atom('SportDeVara', make_const('Volei')))
    # Predicatul 'SportDeIarna'
    add_statement(sports_kb, make_atom('SportDeIarna', make_const('Schi')))
    add_statement(sports_kb, make_atom('SportDeIarna', make_const('Sanie')))
    # Predicatul 'PracticaSport'
    add_statement(sports_kb, make_atom('PracticaSport',
                                       make_const('Nectarie'), make_const('Schi')))
    add_statement(sports_kb, make_atom('PracticaSport',
                                       make_const('Nectarie'), make_const('Sanie')))
    add_statement(sports_kb, make_atom('PracticaSport',
                                       make_const('Arsenie'), make_const('Schi')))
    add_statement(sports_kb, make_atom('PracticaSport',
                                       make_const('Arsenie'), make_const('Volei')))
    # Predicatul 'Activitate'
    add_statement(sports_kb, make_atom('Activitate', make_var('who'), make_var('what'), make_var('when')),
                  make_atom('MergeLaMunte', make_var('who'), make_var('when')),
                  make_atom('PracticaSport', make_var('who'), make_var('what'))
                  )
    make_unique_var_names(sports_kb)
    return sports_kb


print("Baza de cunoștințe se prezintă astfel:")
skb = get_sports_kb()
print_KB(skb)
print("==================== \n Baza de cunoștințe arată intern astfel:")
print("" + "".join([(str(s) + "\n") for s in skb]))


def get_premises(formula):
    premises = []
    for arg in get_args(formula):
        if is_negative_literal(arg):
            premises.append(arg)
    return premises


def get_conclusion(formula):
    for arg in get_args(formula):
        if is_positive_literal(arg):
            return arg

def is_fact(formula):
    return is_positive_literal(formula)


def is_rule(formula):
    return get_head(formula) == 'or' or get_head(formula) == 'and'

# Test!
# formula: P(x) ^ Q(x) -> R(x)
f = make_or(make_neg(make_atom("P", make_var("x"))), make_neg(
    make_atom("Q", make_var("x"))), make_atom("R", make_var("x")))
print(" ; ".join([print_formula(p, True)
                  for p in get_premises(f)]))  # Should be P(?x) ; Q(?x)
print_formula(get_conclusion(f))  # Should be R(?x)
print(is_rule(f))  # must be True
print(is_fact(f))  # must be False
print(is_fact(get_conclusion(f)))  # must be True
print(is_rule(get_conclusion(f)))  # must be False


def equal_terms(t1, t2):
    if is_constant(t1) and is_constant(t2):
        return get_value(t1) == get_value(t2)
    if is_variable(t1) and is_variable(t2):
            return get_name(t1) == get_name(t2)
    if is_function_call(t1) and is_function(t2):
        if get_head(t1) != get_head(t2):
            return all([equal_terms(get_args(t1)[i], get_args(t2)[i]) for i in range(len(get_args(t1)))])
    return False


def is_equal_to(a1, a2):
    # verificăm atomi cu același nume de predicat și același număr de argumente
    if not (is_atom(a1) and is_atom(a2) and get_head(a1) == get_head(a2) and len(get_args(a1)) == len(get_args(a2))):
        return False
    return all([equal_terms(get_args(a1)[i], get_args(a2)[i]) for i in range(len(get_args(a1)))])

from copy import deepcopy
# from __future__ import print_function

def apply_rule(rule, facts):
    print(facts)

    resulting_facts = []
    premises = list(map(lambda x: get_args(x)[0], get_premises(rule)))
    print premises
    substitutions = []

    for premise in premises:
        print('*** premise ***')
        print(premise)
        print('*** end premise ***')

        new_substitutions = []
        for fact in facts:
            print('*** premise ***')
            print(fact)
            print('*** end premise ***')

            res = unify(premise, fact)
            if res:
                substitutions.append(res)
            for substitution in substitutions:
                res = unify(premise, fact, substitution)
                if res:
                    new_substitutions.append(res)

        for new_subst in new_substitutions:
            substitutions.append(new_subst)
        print(substitutions)

    for subst in substitutions:
        res = substitute(get_conclusion(rule), subst)
        if res and res not in resulting_facts:
            resulting_facts.append(res)

    return resulting_facts

# Test!
# Rule: P(x) => Q(x)
# Facts: P(1)
print("Expected: ", print_formula(make_atom('Q', make_const(1)), True), "Result:")
for f in apply_rule( 
        make_or(make_neg(make_atom("P", make_var("x"))), make_atom("Q", make_var("x"))), \
        [make_atom("P", make_const(1))]):
    print_formula(f) # should be Q(1)
print("=====")
# Rule: P(x) ^ Q(x) => R(x)
# Facts: P(1), P(2), P(3), Q(3), Q(2)
print("Expected: ", print_formula(make_atom('R', make_const(2)), True), ";",
      print_formula(make_atom('R', make_const(3)), True), "Result:")
for f in apply_rule( 
        make_or(
            make_neg(make_atom("P", make_var("x"))),
            make_neg(make_atom("Q", make_var("x"))),
            make_atom("R", make_var("x"))),
        [make_atom("P", make_const(x)) for x in [1, 2, 3]] + \
        [make_atom("Q", make_const(x)) for x in [3, 2]]):
    print_formula(f) # should be R(2) and R(3)
print("=====")
# Rule: P(x) ^ Q(y) ^ R(x, y) => T(x, y)
# Facts: P(1), P(2), P(3), Q(3), Q(2), R(3, 2)
print("Expected: ", print_formula(make_atom('T', make_const(3), make_const(2)), True), "Result:")
for f in apply_rule( 
        make_or(
            make_neg(make_atom("P", make_var("x"))),
            make_neg(make_atom("Q", make_var("y"))),
            make_neg(make_atom("R", make_var("x"), make_var("y"))),
            make_atom("T", make_var("x"), make_var("y"))),
        [make_atom("P", make_const(x)) for x in [1, 2, 3]] + \
        [make_atom("Q", make_const(x)) for x in [3, 2]] + \
        [make_atom("R", make_const(3), make_const(2))]):
    print_formula(f) # should be T(3, 2)
print("=====")
# Rule: P(x) ^ Q(y) ^ R(x, y, z) => T(z)
# Facts: P(1), P(2), P(3), Q(3), Q(2), R(1, 1, 1), R(2, 1, 2), R(2, 3, 5), R(4, 2, 3), R(1, 2, 6)
print("Expected: ", print_formula(make_atom('T', make_const(5)), True), ";", 
      print_formula(make_atom('T', make_const(6)), True), "Result:")
for f in apply_rule( 
        make_or(
            make_neg(make_atom("P", make_var("x"))),
            make_neg(make_atom("Q", make_var("y"))),
            make_neg(make_atom("R", make_var("x"), make_var("y"), make_var("z"))),
            make_atom("T", make_var("z"))),
        [make_atom("P", make_const(x)) for x in [1, 2, 3]] + \
        [make_atom("Q", make_const(x)) for x in [3, 2]] + \
        [make_atom("R", make_const(x), make_const(y), make_const(z)) \
             for x, y, z in [(1, 1, 1), (2, 1, 2), (2, 3, 5), (4, 2, 3), (1, 2, 6)]]):
    print_formula(f) # should be T(5) and T(6)


def forward_chaining(kb, theorem, verbose=True):
    # Salvăm baza de date originală, lucrăm cu o copie
    local_kb = deepcopy(kb)
    # Două variabile care descriu starea căutării
    got_new_facts = True   # s-au găsit fapte noi la ultima căutare
    is_proved = False      # a fost demostrată teorema
    # Verificăm dacă teorema este deja demonstrată
    for fact in filter(is_fact, local_kb):
        if unify(fact, theorem):
            if verbose:
                print("This already in KB: " + print_formula(fact, True))
            is_proved = True
            break
    while (not is_proved) and got_new_facts:
        got_new_facts = False
        for rule in filter(is_rule, local_kb):
            # Pentru fiecare regulă
            new_facts = apply_rule(rule, list(filter(is_fact, local_kb)))
            new_facts = list(filter(lambda fact: not any(
                list(filter(lambda orig: is_equal_to(fact, orig), local_kb))), new_facts))
            if new_facts:
                if verbose:
                    print("Applied rule: " + print_formula(rule, True) +
                          ", obtained " + str(len(new_facts)) + " new facts.")
                if any(filter(lambda t: is_variable(t), get_args(get_conclusion(rule)))) and \
                        any(filter(lambda fact: is_equal_to(fact, get_conclusion(rule)), new_facts)):
                        print("Demonstration is too general, the conclusion is not instantiated (facts obtained:",
                              ",".join([print_formula(f, True) for f in new_facts]), ").")
                        return False
                got_new_facts = True
                for fact in new_facts:
                    #if verbose: print("New fact: " + print_formula(fact, True))
                    if unify(fact, theorem) != False:
                        is_proved = True
                        add_statement(local_kb, fact)
                        if verbose:
                            print("Now in KB: " + print_formula(fact, True))
                        break
                    add_statement(local_kb, fact)
            if is_proved:
                break
    if verbose:
        if is_proved:
            print("The theorem is TRUE!")
        else:
            print("The theorem is FALSE!")
    return is_proved


def test_result(result, truth):
    print("Test OK!" if result == truth else "Test FAILED!")


test_kb = skb
print("================== 0")
test_result(forward_chaining(deepcopy(test_kb),
                             make_atom("Frumos", make_var("x")), True), True)
print("================== 1")
test_result(forward_chaining(deepcopy(test_kb),
                             make_atom("Ploua", make_var("x")), True), True)
print("================== 2")
test_result(forward_chaining(deepcopy(test_kb), make_atom(
    "Ploua", make_const("Joi")), True), True)
print("================== 3")
test_result(forward_chaining(deepcopy(test_kb), make_atom(
    "Frumos", make_const("Sambata")), True), True)
print("================== 4")
test_result(forward_chaining(deepcopy(test_kb),
                             make_atom("Activitate",
                                       make_const("Arsenie"), make_var("sport"), make_const("Sambata")), True), True)


