#!/usr/bin/env python

from __future__ import division
import argparse
import random
import pickle
import queue

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

"""
Class Heuristics
Takes in a Class C
"""


"""
Item Heuristics
Takes in resale value as resale, the cost of the item as cost, the weight of the item as weight
Returns {some heuristic value}
"""
def calcItemHeuristic(resale, cost, weight):
  profit = resale - cost
  return profit / (weight + 1) + profit / (cost + 1)

"""
Greedy Knapsack Solver
Takes in list of tuples as items; weight constraint as P, cost constraint as M
Returns list of items that makes approximately the most profit
"""
def greedyKnapsack(items, P, M):
  solution = set()
  itemHeuristics = queue.PriorityQueue()
  for i in range(len(items)):
    item = items[i]
    assert type(item) is tuple
    itemHeuristics.put(items[i], calcItemHeuristic(items[i][4], items[i][3], items[i][2]))
  for i in range(len(items)):
    item = itemHeuristics.get()
    if P > 0 and item[2] < P:
      if M > 0 and item[3] < M:
        solution.add(item[0])
        P = P - item[2]
        M = M - item[3]
  return list(solution)

"""
# Random greedy algorithm
# Picks an independent (compatible) set of classes from problem id.
"""
def pickSet(id):
  with open("problem_graphs/" + str(id) + ".pickle", 'rb') as handle:
    class_constraint_map = pickle.load(handle)
    P, M, N, C, items, constraints = read_input("project_instances/problem" + str(id) + ".in")
    itemscopy = list(items)

    for item in itemscopy:
      if item[4] - item[3] <= 0 or item[2] > P or item[3] > M:
        items.remove(item)
    
    classes = dict()
    for i, item in enumerate(items):
      if item[1] in classes:
        classes[item[1]].add(i)
      else:
        classes[item[1]] = {i}
    
    # Some features we might want to use
    totalValue = lambda c: sum([items[item][4] for item in classes[c]])
    totalWeight = lambda c: sum([items[item][2] for item in classes[c]])
    totalCost = lambda c: sum([items[item][3] for item in classes[c]])
    
    def heuristic(c):
      value = (totalValue(c) - totalCost(c)) / (totalWeight(c) + 1)
      return value

    result = []
    
    # Greedy
    remaining = len(classes)
    while len(classes) > 0:
      next_class = max(classes.keys(), key=lambda c: heuristic(c))
      for neighbor in class_constraint_map[next_class]:
        if neighbor in classes:
          del classes[neighbor]
      
      class_items = classes[next_class]
      del classes[next_class]
      for it in class_items:
        result.append(items[it])
      assert len(classes) < remaining
      remaining = len(classes)
  return result

"""
Scorer takes in id, and output_file
"""
def scorer(id):
  item_map = pickle.load(open("item_map/" + str(id) + ".pickle", "rb"))
  score = 0
  return []


def solve(id):
  """
  Write your amazing algorithm here.

  Return: a list of strings, corresponding to item names.
  """
  P, M, N, C, items, constraints = read_input(generateFilePath(id))
  """
  To make the item dictionaries
  item_dict = dict()
  for item in items:
    item_dict[item[0]] = item
  pickle.dump(item_dict, open("item_map/" + str(id) + ".pickle", "wb"))
  return [] 
  """
  indSet = pickSet(id)
  write_output("outputs/problem" + str(id) + ".out", greedyKnapsack(indSet, P, M))

def generateFilePath(id):
  return "project_instances/problem" + str(id) + ".in"
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

  items_chosen = solve(args.id)
  write_output(args.output_file, items_chosen)
