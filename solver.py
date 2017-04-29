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

def recalcHeuristic(resale, cost, weight, P, M):
  profit = resale - cost
  cost_ratio = cost / M
  weight_ratio = weight / P
  return profit / (weight + 1) + profit / (cost + 1) - cost_ratio - weight_ratio

def greedyKnapsack2(items, P, M):
  solution = set()
  p70 = P * .7
  m70 = M * .7
  while P > p70 and M > m70 and len(items) > 0:
    random_item = random.choice(items)
    if random_item[2] < P and random_item[3] < M:
      solution.add(random_item[0])
      P = P - random_item[2]
      M = M - random_item[3]
      items.remove(random_item)
  heuristic_map = dict()
  for i in range(len(items)):
    item = items[i]
    assert type(item) is tuple
    heuristic_map[items[i]]= calcItemHeuristic(items[i][4], items[i][3], items[i][2])
  for i in range(len(items)):
    item = max(heuristic_map.keys(), key=lambda i: heuristic_map[i])
    del heuristic_map[item]
    if P > 0 and item[2] < P:
      if M > 0 and item[3] < M:
        solution.add(item[0])
        P = P - item[2]
        M = M - item[3]
        for item2 in heuristic_map:
          heuristic_map[item2] = recalcHeuristic(item2[4], item2[3], item2[2], P, M)
  return list(solution)  

"""
Greedy Knapsack Solver
Takes in list of tuples as items; weight constraint as P, cost constraint as M
Returns list of items that makes approximately the most profit
"""
def greedyKnapsack(items, P, M):
  solution = set()
  p70 = P * .7
  m70 = M * .7
  while P > p70 and M > m70 and len(items) > 0:
    random_item = random.choice(items)
    if random_item[2] < P and random_item[3] < M:
      solution.add(random_item[0])
      P = P - random_item[2]
      M = M - random_item[3]
      items.remove(random_item)
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
def pickSet(id, r=False):
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
      value = (totalValue(c) - totalCost(c)) / (totalCost(c) + 1)
      return value

    result = []
    
    # Greedy random
    numClasses = len(classes)
    classesPicked = 0
    while len(classes) > 0:
      # Pick randomly for first 5%
      while classesPicked < 5:
        next_class = random.choice(list(classes.keys()))
        for neighbor in class_constraint_map[next_class]:
          if neighbor in classes:
            del classes[neighbor]
        class_items = classes[next_class]
        del classes[next_class]
        for it in class_items:
          result.append(items[it])
        classesPicked += 1
      # Greedily pick for the rest
      next_class = max(classes.keys(), key=lambda c: heuristic(c))
      for neighbor in class_constraint_map[next_class]:
        if neighbor in classes:
          del classes[neighbor]
      
      class_items = classes[next_class]
      del classes[next_class]
      for it in class_items:
        result.append(items[it])
      classesPicked += 1
  print("problem", str(id) + ": ", classesPicked, "classes picked.")
  return result

"""
Scorer takes in id, and output_file
"""
def scorer(id, item_list):
  P, M, N, C, items, constraints = read_input("project_instances/problem" + str(id) + ".in")
  class_constraint_map = pickle.load(open("problem_graphs/"+str(id)+".pickle", "rb"))
  item_map = pickle.load(open("item_map/" + str(id) + ".pickle", "rb"))
  incompatibles = set()
  score = 0
  weight = 0
  cost = 0
  for item in item_list:
    itemObj = item_map[item]
    clas = itemObj[1]
    if clas in incompatibles or weight + itemObj[2] > P or cost + itemObj[3] > M:
      return 0
    score += itemObj[4]
    weight += itemObj[2]
    cost += itemObj[3]
    for neighbor in class_constraint_map[clas]:
      incompatibles.add(neighbor)
  print("value of items:", score)
  return score + M - cost


def solve(id):
  """
  Write your amazing algorithm here.

  Return: a list of strings, corresponding to item names.
  """
  f = open("outputs/best_scores.txt")
  bestScores = f.readlines()
  f.close()

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
  picked_items = greedyKnapsack2(indSet, P, M)
  this_score = round(scorer(id, picked_items), 2)
  if this_score > float(bestScores[id-1]):
    write_output("outputs/problem" + str(id) + ".out", picked_items)
    print("got better score!", this_score, "for problem", id, "whose best score was previously", bestScores[id-1])
    bestScores[id-1] = str(this_score)+"\n"

    f = open("outputs/best_scores.txt", 'w')
    for score in bestScores:
      f.write(score)
    f.close()
  else:
    print("got worse score", this_score, "for problem", id, "whose best score was", bestScores[id-1])


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
