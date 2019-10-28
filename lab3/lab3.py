from copy import copy, deepcopy
from itertools import combinations

VarsA = ["A", "B", "C", "D", "E"]
DomainsA = {v: [i for i in range(10)] for v in VarsA}
ConstraintsA = [(list(p), lambda x, y: x != y)
                for p in combinations(VarsA, 2)]  # toate valorile diferite
ConstraintsA.append((["A", "B"], lambda a, b: a + b == 10))
ConstraintsA.append((["B", "D"], lambda b, d: b + d == 6))
ConstraintsA.append((["C"], lambda c: c < 5))
ConstraintsA.append((["A"], lambda a: a > 5))
ConstraintsA.append((["A", "B", "C", "D", "E"], lambda a,
                     b, c, d, e: a + b + c + d + e == 30))
MathProblem = {"Vars": VarsA, "Domains": DomainsA, "Constraints": ConstraintsA}

VarsC = ["France", "Germany", "Loux", "Belgium", "Netherlands"]
DomainsC = {v: ["blue", "red", "yellow", "green"] for v in VarsC}
ConstraintsC = []
for (a, b) in [("France", "Germany"), ("France", "Belgium"), ("France", "Loux"),
               ("Belgium", "Netherlands"), ("Belgium",
                                            "Loux"), ("Belgium", "Germany"),
               ("Loux", "Germany"), ("Netherlands", "Germany")]:
    ConstraintsC.append(([a, b], lambda a, b: a != b))
ColoringProblem = {"Vars": VarsC,
                   "Domains": DomainsC, "Constraints": ConstraintsC}


def get_constraints(var, constraints):
    newCons = []
    for constraint, lambdafunction in constraints:
        if var in constraint:
            newCons.append((constraint, lambdafunction))
    return newCons

print get_constraints("France", ConstraintsC)


def fixed_constraints(solution, constraints):
    varsInSolution = []
    for k in solution:
        varsInSolution.append(k)
    
    fixed_constraints = []
    for (variables, lambdafunc) in constraints:
        append = True
        for variable in variables:
            if (variable not in varsInSolution):
                append = False
                break
        if append:
            fixed_constraints.append((variables, lambdafunc))
    return fixed_constraints


print(fixed_constraints({"France": "blue", "Belgium": "green"}, ConstraintsC))
print(fixed_constraints({"A": "1", "C": "2"}, ConstraintsA))

def check_constraint(solution, constraint):
    (constraintParams, constraintLambda) = constraint
    constraintVals = []
    for constraintParam in constraintParams:
        constraintVals.append(solution[constraintParam])
    
    return apply(constraintLambda, constraintVals)


print(check_constraint(
    {"France": "blue", "Belgium": "green"}, ConstraintsC[1]))  # => True
# => False
print(check_constraint({"France": "blue", "Belgium": "blue"}, ConstraintsC[1]))
print(check_constraint({"C": 10, "A": 10}, ConstraintsA[-2]))  # => True
print(check_constraint({"C": 10, "A": 3}, ConstraintsA[-2]))  # => False

def PCSP(vars, domains, constraints, acceptable_cost, solution, cost):
    global best_solution
    global best_cost
    if not vars:
        # Daca nu mai sunt variabile, am ajuns la o solutie mai buna
        print("New best: " + str(cost) + " - " + str(solution))
        # TODO: salvati solutia nou-descoperita
        best_solution = solution
        best_cost = cost
        # TODO: daca este suficient de buna, functia intoarce True
        if best_cost < acceptable_cost:
            return True

    elif not domains[vars[0]]:
        # Daca nu mai sunt valori in domeniu, am terminat cautarea
        return False
    elif cost == best_cost:
        # Daca am ajuns deja la un cost identic cu cel al celei mai bune solutii,
        # nu mergem mai departe
        return False
    else:
        # TODO: Luam prima variabila si prima valoare din domeniu
        var = vars[0]
        val = domains[var].pop(0)

        # TODO: Construim noua solutie
        new_solution = deepcopy(solution)
        new_solution[var] = val
        # TODO: Obtinem lista constrangerilor ce pot fi evaluate acum
        constraintsForVal = get_constraints(var, constraints)
        fixedConstraints = fixed_constraints(new_solution, constraintsForVal)

        # TODO:  Calculam costul noii solutii partiale (fiecare constrangere incalcata = 1)
        new_cost = cost
        for constraint in fixedConstraints:
            if not check_constraint(new_solution, constraint):
                new_cost = new_cost + 1

        # Verificam daca noul cost este mai mic decat cel mai bun cost
        if new_cost < best_cost:
            # TODO:
            # Daca noul cost este mai mic decat cel mai bun cunoscut, rezolvam pentru restul variabilelor
            # Daca apelul recursiv intoarce True, a fost gasita o solutie suficient de buna, deci intoarcem True
            new_vars = deepcopy(vars[1:])
            var_domain = domains.pop(var)

            new_domain = deepcopy(domains)

            result = PCSP(new_vars, new_domain, constraints,
            acceptable_cost, new_solution, new_cost)

            if result:
                return True
            
            domains[var] = var_domain
        # Verificam pentru restul valorilor
        # TODO:
        PCSP(vars, deepcopy(domains), constraints,
             acceptable_cost, solution, cost)

# Un wrapper care sa instantieze variabilele globale
def run_pcsp(problem, acceptable_cost):
    global best_solution
    global best_cost

    [vars, domains, constraints] = [problem[e]
                                    for e in ["Vars", "Domains", "Constraints"]]

    best_solution = {}
    best_cost = len(constraints)

    if PCSP(vars, deepcopy(domains), constraints, acceptable_cost, {}, 0):
        print("Best found: " + str(best_cost) + " - " + str(best_solution))
    else:
        print("Acceptable solution not found; " + "Best found: " +
              str(best_cost) + " - " + str(best_solution))


# Rulam magaria
run_pcsp(MathProblem, 1)
run_pcsp(ColoringProblem, 1)
