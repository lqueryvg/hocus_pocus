#!/usr/bin/env python2

# Solve:
#
#     HOCUS
#     POCUS +
#    ------
#    PRESTO
#    ------
#
# Where:
# - each letter represents a single digit (0-9)
# - different letters represent different digits 
# - the same letter represents the same digit

from constraint import *

problem = Problem()

problem.addVariables(
        ["H", "O", "C", "U", "S", "P", "R", "E", "T"],
        [0,1,2,3,4,5,6,7,8,9]
)

problem.addConstraint(AllDifferentConstraint())

# Apply a bit of manual logic first.
problem.addConstraint(lambda p: p == 1, ["P"]) # P must be 1
problem.addConstraint(lambda h: h >= 8, ["H"]) # H >= 8 to cause a carry to P
problem.addConstraint(lambda r: r == 0, ["R"]) # since P=1, R must be 0

# The remaining constraints are based on column method addition.
problem.addConstraint(lambda s, o: (s + s) % 10 == o, ["S", "O"])
problem.addConstraint(lambda s,u,t: total([s+s, u+u]) % 10 == t,
        ["S", "U", "T"])
problem.addConstraint(lambda s,u,c: total([s+s, u+u, c+c]) % 10 == s,
        ["S", "U", "C"])
problem.addConstraint(lambda s,u,c,o,e: total([s+s, u+u, c+c, o+o]) % 10 == e,
        ["S", "U", "C", "O", "E"])
problem.addConstraint(lambda s,u,c,o,r: total([s+s, u+u, c+c, o+o]) / 10 == r,
        ["S", "U", "C", "O", "R"])

def total(columns):
    # For each column, add carry (initially zero) to column value,
    # then if the result is >= 10, discard the result and carry 1
    # to the next column, until we reach the last column where we return
    # the result.
    carry = 0
    for value in columns:
        value = value + carry
        carry = value / 10
    return value

solutions = problem.getSolutions()
print solutions
