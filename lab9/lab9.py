#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import shuffle
from copy import deepcopy
import sys
from functools import reduce
from operator import mul
from itertools import permutations
from collections import namedtuple

from copy import copy

Factor = namedtuple("Factor", ["vars", "values"])


def print_factor(phi, indent="\t"):
    line = " | ".join(phi.vars + ["ϕ(" + ",".join(phi.vars) + ")"])
    sep = "".join(["+" if c == "|" else "-" for c in list(line)])
    print(indent + sep)
    print(indent + line)
    print(indent + sep)
    for values, p in phi.values.items():
        print(indent + " | ".join([str(v) for v in values] + [str(p)]))
    print(indent + sep)


# Examples

phi_ABC = Factor(vars=["A", "B", "C"],
                 values={(0, 0, 0): .1, (0, 0, 1): .9, (0, 1, 0): .8, (0, 1, 1): .2,
                         (1, 0, 0): .7, (1, 0, 1): .4, (1, 1, 0): .5, (1, 1, 1): .5})
phi_AB = Factor(vars=["A", "B"], values={
                (0, 0): .1, (0, 1): .9, (1, 0): .8, (1, 1): .2})
phi_BC = Factor(vars=["B", "C"], values={
                (0, 0): .2, (0, 1): .8, (1, 0): .5, (1, 1): .5})
phi_A = Factor(vars=["A"], values={(0,): .4, (1,): .6})
phi_C = Factor(vars=["C"], values={(0,): .6, (1,): .8})

print_factor(phi_ABC)
print("ϕ(A=1, B=0, C=0) = " + str(phi_ABC.values[(1, 0, 0)]))

# Multiplicarea a doi factori:

def multiply(phi1, phi2):
    assert isinstance(phi1, Factor) and isinstance(phi2, Factor)
    # Cerinta 1 :
    
    new_vars = list(set(phi1.vars) | set(phi2.vars))
    new_vars.sort()

    phi = Factor(vars = new_vars, values = {})

    for values1 in phi1.values:
        for values2 in phi2.values:
            products = copy(new_vars)
            goodPos = True
            
            for var in new_vars:
                if var in phi1.vars and var in phi2.vars:
                    if values1[phi1.vars.index(var)] != values2[phi2.vars.index(var)]:
                        goodPos = False
                        
            if goodPos:
                for key, var in enumerate(new_vars):
                    if (var in phi1.vars and var in phi2.vars) or var in phi1.vars:
                        products[key] = values1[phi1.vars.index(var)]
                    else:
                        products[key] = values2[phi2.vars.index(var)]
                        
                phi.values[tuple(products)] = phi1.values[values1] * phi2.values[values2]
                
    return phi


print_factor(phi_AB)
print("*")
print_factor(phi_BC)
print("=")
print_factor(multiply(phi_AB, phi_BC))

## Tests for multiply


def _check_factor(_phi, all_vars, control):
    assert sorted(_phi.vars) == sorted(all_vars), \
        "Wrong variables: " + \
        ','.join(_phi.vars) + " instead of " + ','.join(all_vars)
    assert len(_phi.values) == 2 ** len(all_vars), \
        "Wrong number of entries in phi.values: " + str(len(_phi.values))
    n = len(all_vars)
    if n > 0:
        for j in range(n + 1):
            vals = [0] * (n - j) + [1] * j
            keys = set([p for p in permutations(vals)])
            p = reduce(mul, [_phi.values[k] for k in keys])
            assert abs(p - control[j]) < 1e-9, \
                "Values for " + str(keys) + " are wrong!"
    else:
        assert abs(_phi.values[()] - control[0]) < 1e-9


def _test_multiply(name1, name2, all_vars, control, verbose=False):
    _phi = eval("multiply(deepcopy(phi_"+name1+"), deepcopy(phi_"+name2+"))")
    if verbose:
        print("Result of ϕ_"+name+" * ϕ_"+name2+":")
        print_factor(_phi)
    sys.stdout.write("Testing  ϕ_"+name1+" * ϕ_"+name2+" ... ")
    _check_factor(_phi, all_vars, control)
    print("OK!!")


_test_multiply("AB", "BC", ["A", "B", "C"],
               [.02, .00576, .0288, .1], verbose=False)
_test_multiply("A", "BC", ["A", "B", "C"], [.08, .00768, .0288, .3])
_test_multiply("A", "AB", ["A", "B"], [.04, .1728, .12])
_test_multiply("BC", "A", ["C", "A", "B"], [.08, .00768, .0288, .3])
_test_multiply("ABC", "BC", ["C", "A", "B"], [.02, .04032, .008, .25])
_test_multiply("C", "A", ["C", "A"], [.24, .1152, .48])
_test_multiply("A", "C", ["C", "A"], [.24, .1152, .48])
_test_multiply("C", "C", ["C"], [.36, .64])

print("\nMultiply seems ok!\n")


def sum_out(var, phi):
    assert isinstance(phi, Factor) and var in phi.vars
    # Cerinta 2:
    new_vars = copy(phi.vars)
    var_index = new_vars.index(var)
    new_vars.remove(var)

    new_phi = Factor(vars = new_vars, values ={})

    for l in phi.values:
        curr_list = []
        for i in range(len(l)):
            if i != var_index:
                curr_list.append(l[i])
        new_line = tuple(curr_list)

        if new_line in new_phi.values.keys():
            new_phi.values[new_line] += phi.values[l]
        else:
            new_phi.values[new_line] = phi.values[l]

    return new_phi

# Un exemplu


print("Însumând B afară din")
print_factor(phi_ABC)
print("=")
print_factor(sum_out("B", phi_ABC))

## Tests for sum_out


def _test_sum_out(var, name, left_vars, control, verbose=False):
    import sys
    from itertools import permutations
    from operator import mul
    from functools import reduce
    _phi = eval("sum_out('"+var+"', phi_"+name+")")
    if verbose:
        print_factor(_phi)
    sys.stdout.write("Testing  sum_"+var+" ϕ_"+name+" ... ")
    _check_factor(_phi, left_vars, control)
    print("OK!!")


_test_sum_out("A", "ABC", ["C", "B"], [.8, 1.69, .7], verbose=False)
_test_sum_out("B", "ABC", ["A", "C"], [.9, 1.32, .9], verbose=False)
_test_sum_out("C", "C", [], [1.4], verbose=False)
_test_sum_out("A", "A", [], [1.], verbose=False)
_test_sum_out("B", "BC", ["C"], [.7, 1.3], verbose=False)

print("\nSummations seems ok!\n")


def prod_sum(var, Phi, verbose=False):
    assert isinstance(var, str) and all(
        [isinstance(phi, Factor) for phi in Phi])
    # Cerinta 3:
    new_Phi = []
    for phi in Phi:
        if var in phi.vars:
            new_Phi.append(phi)

    result = new_Phi[0]
    for factor in new_Phi[1:]:
        result = multiply(result, factor)

    result = sum_out(var, result)

    ans = [result]

    for phi in Phi:
        if phi not in new_Phi:
            ans.append(phi)

    if (verbose):
        print_factor(ans)

    return ans

# Un exemplu
print("Elininând B din :")
print_factor(phi_AB)
print("și")
print_factor(phi_BC)
print("=>")
print_factor(prod_sum("B", [phi_AB, phi_BC])[0])

## Test prod_sum

sys.stdout.write("Testing prod-sum (I) ... ")
result = prod_sum("B", [deepcopy(_phi)
                        for _phi in [phi_A, phi_C, phi_ABC, phi_BC]])
assert len(result) == 3
for _phi in result:
    if sorted(_phi.vars) == ["A", "C"]:
        assert abs(_phi.values[(0, 0)] - 0.42) < 1e-9
        assert abs(_phi.values[(0, 1)] * _phi.values[(1, 0)] - 0.3198) < 1e-9
        assert abs(_phi.values[(1, 1)] - 0.57) < 1e-9
    elif sorted(_phi.vars) == ["A"]:
        assert abs(_phi.values[(0,)] - 0.4) < 1e-9
        assert abs(_phi.values[(1,)] - 0.6) < 1e-9
    elif sorted(_phi.vars) == ["C"]:
        assert abs(_phi.values[(0,)] - 0.6) < 1e-9
        assert abs(_phi.values[(1,)] - 0.8) < 1e-9
print("OK!")

sys.stdout.write("Testing prod-sum (II) ... ")
result = prod_sum("A", [deepcopy(_phi)
                        for _phi in [phi_A, phi_C, phi_ABC, phi_BC]])
assert len(result) == 3
for _phi in result:
    if sorted(_phi.vars) == ["B", "C"]:
        assert abs(
            _phi.values[(0, 0)] - 0.2) < 1e-9 or abs(_phi.values[(0, 0)] - 0.46) < 1e-9
        assert abs(_phi.values[(0, 1)] * _phi.values[(1, 0)] - 0.4) < 1e-9 or \
            abs(_phi.values[(0, 1)] * _phi.values[(1, 0)] - 0.372) < 1e-9
        assert abs(
            _phi.values[(1, 1)] - 0.5) < 1e-9 or abs(_phi.values[(1, 1)] - 0.38) < 1e-9
    elif sorted(_phi.vars) == ["C"]:
        assert abs(_phi.values[(0,)] - 0.6) < 1e-9
        assert abs(_phi.values[(1,)] - 0.8) < 1e-9
print("OK!")
print("Prod-Sum seems ok!")


def variable_elimination(Phi, Z, verbose=False):
    # Cerinta 4:

    new_Phi = copy(Phi)
    for z in Z:
        new_Phi = prod_sum(z, new_Phi)

    result = new_Phi[0]
    for factor in new_Phi[1:]:
        result = multiply(result, factor)

    return result

## Testing Variable elimination


def _test_variable_elimination(Phi, Vars, left_vars, control, verbose=False):

    var_list = '["' + '", "'.join(Vars) + '"]'
    factor_list = '[' + ','.join([("deepcopy(phi_"+name + ")")
                                  for name in Phi]) + ']'
    name_list = '[' + ','.join([("ϕ_"+name) for name in Phi]) + ']'
    _phi = eval("variable_elimination("+factor_list+", "+var_list+")")
    if verbose:
        print_factor(_phi)
    sys.stdout.write("Testing  eliminate_var " +
                     var_list+" from "+name_list+" ... ")
    _check_factor(_phi, left_vars, control)
    print("OK!!")


_test_variable_elimination(["A", "C"], ["C"], ["A"], [0.56, 0.84])
_test_variable_elimination(["ABC", "BC", "AB", "A"], [
                           "C", "B"], ["A"], [0.2096, 0.2808])
_test_variable_elimination(["ABC", "BC", "AB", "A"], [
                           "C", "B", "A"], [], [0.4904])
_test_variable_elimination(["ABC", "AB", "BC", "A"], [
                           "A", "B", "C"], [], [0.4904])
_test_variable_elimination(["ABC"], ["A", "B", "C"], [], [4.1])


def condition_factors(Phi, Z, verbose=False):
    # Cerinta 5
    new_Phi = deepcopy(Phi)

    for var in Z:
        for factor in new_Phi:
            if var not in factor.vars:
                continue
            var_index = factor.vars.index(var)

            toDelete = []
            for line in factor.values:
                if line[var_index] != Z[var]:
                    toDelete.append(line)
            print toDelete

            for line in toDelete:
                del factor.values[line]
    return new_Phi

# Un exemplu
print("Aplicand B=0 in factorul")
print_factor(phi_ABC)
print("=>")
print_factor(condition_factors([phi_ABC], {"B": 0})[0])

# Teste pentru condition_factors

phi_ABC = Factor(vars=["A", "B", "C"],
                 values={(0, 0, 0): .1, (0, 0, 1): .9, (0, 1, 0): .8, (0, 1, 1): .2,
                         (1, 0, 0): .7, (1, 0, 1): .4, (1, 1, 0): .5, (1, 1, 1): .5})

_phi = condition_factors([phi_ABC], {"B": 0})[0]
assert sorted(_phi.vars) == ["A", "B", "C"]
assert len(_phi.values) == 4 and abs(_phi.values[(0, 0, 0)] - .1) < 1e-7
_phi = condition_factors([phi_ABC], {"B": 0, "A": 1})[0]
assert sorted(_phi.vars) == ["A", "B", "C"] and len(_phi.values) == 2
print("Condition factors seems ok!")


def query(X, Y, Z, Phi, Other=None, verbose=False):
    """
    X - full list of variables
    Y - query variables
    Z - dictionary with observations
    Phi - the list with all factor
    Ohter - an order over variables in X \ (Y U Z); None to pick a random one
    verbose - display factors as they are created
    """

    if verbose:
        print("\n-------------\nInitial factors:")
        for phi in Phi:
            print_factor(phi)

    # Condition factors on Z=z
    Phi = condition_factors(Phi, Z, verbose=verbose)

    if Other is None:
        # Variables that need to be eliminated
        Other = [x for x in X if (x not in Y and x not in Z)]
        shuffle(Other)
    else:
        assert sorted(Other) == sorted(
            [x for x in X if (x not in Y and x not in Z)])
    if verbose:
        print("\n-------------\nEliminating variables in the following order: " + ",".join(Other))

    # Eliminate other variables then Y and Z
    phi = variable_elimination(Phi, Other, verbose=verbose)

    # Normalize factor to represent the conditional probability p(Y|Z=z)
    s = sum(phi.values.values())
    prob = Factor(vars=phi.vars, values={
                  k: v / s for (k, v) in phi.values.items()})
    print("\n-----------------\nProbabilitatea ceruta:")
    print_factor(prob)


phi_a = Factor(vars=["A"], values={(0,): .7, (1,): .3})
phi_b = Factor(vars=["B"], values={(0,): .5, (1,): .5})
phi_c = Factor(vars=["C"], values={(0,): .4, (1,): .6})

phi_d = Factor(vars=["A", "B", "D"],
               values={(0, 0, 0): .75, (0, 0, 1): .25, (0, 1, 0): .7, (0, 1, 1): .3,
                       (1, 0, 0): .6, (1, 0, 1): .4, (1, 1, 0): .2, (1, 1, 1): .8
                       })
phi_e = Factor(vars=["C", "E"],
               values={(0, 0): .25, (0, 1): .75, (1, 0): .75, (1, 1): .25})

phi_f = Factor(vars=["A", "D", "F"],
               values={(0, 0, 0): .6, (0, 0, 1): .4, (0, 1, 0): .4, (0, 1, 1): .6,
                       (1, 0, 0): .7, (1, 0, 1): .3, (1, 1, 0): .8, (1, 1, 1): .2
                       })
phi_g = Factor(vars=["D", "E", "G"],
               values={(0, 0, 0): .1, (0, 0, 1): .9, (0, 1, 0): .2, (0, 1, 1): .8,
                       (1, 0, 0): .5, (1, 0, 1): .5, (1, 1, 0): .4, (1, 1, 1): .6
                       })

all_vars = ["A", "B", "C", "D", "E", "F", "G"]
Phi = [phi_a, phi_b, phi_c, phi_d, phi_e, phi_f, phi_g]
# Algoritmul ar trebui să ajungă la probabilitățile din tabele

# Verificati ca algoritmul "ajunge" corect la valorile din tabele
query(all_vars, ["F"], {"A": 0, "D": 1}, Phi)
query(all_vars, ["G"], {"D": 0, "E": 1}, Phi)

# Exemplul din PDF-ul atașat

query(all_vars, ["C", "F"], {"G": 0}, Phi,
      Other=["E", "B", "A", "D"], verbose=True)
