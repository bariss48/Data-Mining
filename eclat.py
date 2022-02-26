# -*- coding: utf-8 -*-
"""
Created on Fri Nov 19 04:28:28 2021

@author: Mustafa Z. Y. MAKARNACI
"""
"""
@algortithm: ECLAT
"""


# -----------------------------------------------------------------------------


import numpy as np
import pickle
from pytictoc import TicToc
t = TicToc()

# -----------------------------------------------------------------------------
with open('DATABASE_863144x42.pckl', 'rb') as f:
    DATABASE, SingleItems = pickle.load(f)

database = DATABASE
singleItems = SingleItems

# -----------------------------------------------------------------------------


def showDatabase(database, singleItems):
    for i in range(database.shape[0]):
        tr = database[i, :]
        I = np.nonzero(tr > 0)[0]
        print(i, ':', singleItems[I])
    return


# -----------------------------------------------------------------------------
 #                   A  B  C  D  E
# DATABASE = np.array([[1, 0, 1, 1, 0],
#                       [0, 1, 1, 0, 1],
#                       [1, 1, 1, 0, 1],
#                       [0, 1, 0, 0, 1],
#                       [1, 1, 1, 0, 1],
#                       ],)

# singleItems = np.array(["A", "B", "C", "D", "E"])
# trsItems = np.array(["T1", "T2", "T3", "T4", "T5"])
minSupp = 777777


# -----------------------------------------------------------------------------
def eclatDfsLoop(itemset, itemsetTIDList, TIDList, minSupp, frequentItemSets, supports, numOfItems):
    temp = itemset[-1]
    for i in range(temp+1, numOfItems):
        newItemSet = 1 * itemset
        newItemSet.append(i)
        newItemSetTIDList = []
        suffixTIDList = 1 * TIDList[i]
        newItemSetTIDList = np.intersect1d(itemsetTIDList, suffixTIDList)
        suppOfNewItemSet = len(newItemSetTIDList)
        if minSupp <= suppOfNewItemSet:
            frequentItemSets.append(newItemSet)
            supports.append(suppOfNewItemSet)
            (frequentItemSets, supports) = eclatDfsLoop(newItemSet, newItemSetTIDList,
                                                        TIDList, minSupp, frequentItemSets, supports, numOfItems)
    return frequentItemSets, supports
# -----------------------------------------------------------------------------


t.tic()

TIDList = []
frequentItemSets = []
supports = []

initialSupports = np.sum(DATABASE, axis=0)

# items to be remained
ItemsToBeRemained = np.nonzero(minSupp <= initialSupports)[0]

# new database with items to be remained
DATABASE = DATABASE[:, ItemsToBeRemained]

# new single items
singleItems = singleItems[ItemsToBeRemained]

# initial supports of items to be remained
initialSupports = initialSupports[ItemsToBeRemained]

# num of items of to be remained
numOfItems = singleItems.shape[0]

# determine TID list
for i in range(0, numOfItems):
    idx = np.nonzero(DATABASE[:, i] > 0)[0]
    TIDList.append(list(idx))


# preperation frequent item sets and supports
for i in range(0, numOfItems):
    frequentItemSets.append([i])
    supports.append(initialSupports[i])

# eclat dfs starting down here
for item in range(0, numOfItems):
    itemset = [item]
    itemsetTIDList = TIDList[item]
    (frequentItemSets, supports) = eclatDfsLoop(itemset, itemsetTIDList,
                                                TIDList, minSupp, frequentItemSets, supports, numOfItems)


t.toc()

I = np.argsort(-np.array(supports))
frequentItemSets = [frequentItemSets[i] for i in I]
supports = [supports[i] for i in I]
print('\nSUPPORTS:\n')
for i in range(0, len(frequentItemSets)):
    itemset = frequentItemSets[i]
    tmp = " "
    for j in itemset:
        tmp = tmp + singleItems[j]
    print('#', i+1, tmp, 'Supp:', (supports[i]*2)/10, ' => ', supports[i])


with open('EclatResults', 'wb') as f:
    pickle.dump([frequentItemSets, supports,
                singleItems, DATABASE], f)
