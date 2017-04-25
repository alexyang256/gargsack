#!/usr/bin/env python

from __future__ import division
import argparse
import random
import numpy as np
import scipy.io as io 

"""
===============================================================================
  Please complete the following function.
===============================================================================
"""
def writeGraph(item_constraints, filename, id):
  file = open(filename, 'w')
  for item, incompatible in item_constraints.items():
    toWrite = str((item, incompatible))+'\n'
    file.write(toWrite)
  file.close()

#####KNAPSACK SOLVER#####
def knapsackSolver(items, P, M):
  solution = []
  knapsack_matrix = np.zeros((len(items), P, M))
  for i in range(len(items)):
    for w in range(P):
      for c in range(M):
        items[i][2]

def generateMatrices(id, P, M, N, C, items, constraints):
  """
  Write your amazing algorithm here.

  Return: a list of strings, corresponding to item names.
  """
  graphDest = "problem_graphs/problem" + str(id) + ".mat"
  itemscopy = list(items)

  for item in itemscopy:
    if item[4] - item[3] <= 0 or item[2] > P or item[3] > M:
      items.remove(item)

  classes = set()
  for item in items:
    classes.add(item[1])

  # Adj list
  class_constraint_map = dict()
  for clas in classes:
    class_constraint_map[clas] = set()

  count = 0
  for clas in classes:
    
    for constraint in constraints:
      if clas in constraint:
        incompatibles = constraint.copy()
        incompatibles.remove(clas)
        for incompatible in incompatibles:
          class_constraint_map[clas].add(incompatible)
    count += 1
  """
  # Adj list items
  item_constraint_map = dict()
  for item in items:
    item_constraint_map[item[0]] = set()

  print(len(class_constraint_map), '***')
  for item in items:
    for item2 in items:
      if item2[1] in class_constraint_map[item[1]]:
        item_constraint_map[item[0]].add(item2[0])
  writeGraph(item_constraint_map, "problem_graphs/problem3.graph")
  solution = []
  print(min(items, key=lambda item: item[3]))
  """
  iterations = 0
  
  item_matrix = np.zeros((len(items), len(items)))
  for i in range(len(items)):
    for j in range(i):
      if items[j][1] in class_constraint_map[items[i][1]]:
        item_matrix[i][j] = 1
        item_matrix[j][i] = 1

  io.savemat(graphDest, {"graph": item_matrix})

  return []

"""
  while iterations < len(items) and len(items) > 0 and P >= min(items, key=lambda item: item[2])[2] and M >= min(items, key=lambda item: item[3])[3]:

    item = max(items, key=lambda item: (item[4] - item[3])/max(0.01, item[2]))
    while item[2] > P and item[3] > M:
      items.remove(item)
      item = max(items, key=lambda item: (item[4] - item[3])/max(0.01, item[2]))

    solution.append(item[0])
    P -= item[2]
    M -= item[3]
    for incompatible in item_constraint_map[item]:
      if incompatible in items:
        items.remove(incompatible)
    iterations += 1
  return solution
  """
"""
===============================================================================
  No need to change any code below this line.
===============================================================================
"""

def read_input(filename):
  """
  P: float
  M: float
  N: integer
  C: integer
  items: list of tuples
  constraints: list of sets
  """
  with open(filename) as f:
    P = float(f.readline())
    M = float(f.readline())
    N = int(f.readline())
    C = int(f.readline())
    items = []
    constraints = []
    for i in range(N):
      name, clas, weight, cost, val = f.readline().split(";")
      items.append((name, int(clas), float(weight), float(cost), float(val)))
    for i in range(C):
      constraint = set(eval(f.readline()))
      constraints.append(constraint)
  return P, M, N, C, items, constraints

def write_output(filename, items_chosen):
  with open(filename, "w") as f:
    for i in items_chosen:
      f.write("{0}\n".format(i))

if __name__ == "__main__":

  parser = argparse.ArgumentParser(description="PickItems solver.")
  parser.add_argument("input_file", type=str, help="____.in")
  parser.add_argument("output_file", type=str, help="____.out")
  parser.add_argument("id", type=str)
  args = parser.parse_args()

  P, M, N, C, items, constraints = read_input(args.input_file)
  items_chosen = generateMatrices(args.id, P, M, N, C, items, constraints)
  write_output(args.output_file, items_chosen)
