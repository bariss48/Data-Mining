# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 00:18:54 2021

@author: Mustafa
"""

try:
    from pytictoc import TicToc
    import numpy as np
    import pickle
except:
    pass


elapsed = TicToc()

with open('DATABASE_863144x42.pckl', 'rb') as f:
    DATABASE, SingleItems = pickle.load(f)

# ------------------------------------------------------------------------------


def DoesExist(itm, transaction):

    if sum(transaction[itm]) == len(itm):
        E = 1
    else:
        E = 0
    return E

# ------------------------------------------------------------------------------


def CalcAbsSupp(itm, DATABASE):
    absSupp = 0
    for i in range(0, DATABASE.shape[0]):
        transaction = DATABASE[i, :]
        if DoesExist(itm, transaction):
            absSupp += 1
    return absSupp

# ------------------------------------------------------------------------------


def CandidateGeneration(fkm1):
    ck = []
    for i in range(0, len(fkm1)-1):
        for j in range(i+1, len(fkm1)):

            itemset1 = fkm1[i]
            itemset2 = fkm1[j]

            if all(itemset1[1:] == itemset2[:-1]):
                NewItem = np.hstack(
                    (np.array(itemset1), np.array(itemset2[-1])))
                ck.append(NewItem)
    return ck

# ------------------------------------------------------------------------------


def ShowDATABASE(DATABASE, SingleItems):
    for i in range(DATABASE.shape[0]):
        tr = DATABASE[i, :]
        I = np.nonzero(tr > 0)[0]
        print(i, ':', SingleItems[I])
    return


# DATABASE = np.array([[1, 0, 1, 0, 0, 1],
#                      [0, 1, 0, 1, 1, 0],
#                      [0, 0, 1, 1, 1, 0],
#                      [1, 0, 1, 0, 1, 1],
#                      [1, 1, 0, 1, 0, 0],
#                      [1, 0, 1, 0, 1, 1],
#                      [1, 0, 1, 1, 1, 1],
#                      [1, 1, 0, 1, 1, 0],
#                      [0, 1, 1, 0, 1, 0],
#                      [1, 0, 0, 1, 0, 1],
#                      [0, 1, 1, 1, 0, 0]], )

#				      A  B  C  D  E  F
# DATABASE = np.array([[1, 0, 1, 1, 0],
#                      [0, 1, 1, 0, 1],
#                      [1, 1, 1, 0, 1],
#                      [0, 1, 0, 0, 1],
#                      [1, 1, 1, 0, 1],
#                      ], )

# SingleItems = np.array(["A", "B", "C", "D", "E"])
# -----------------------------------------------------------------------------
minsupp = 777777

elapsed.tic()

NumOfTransaction = DATABASE.shape[0]

# sum columns values
initial_SUPPORTSs = np.sum(DATABASE, axis=0)

# items to be remained
ItemsToBeRemained = np.nonzero(minsupp <= initial_SUPPORTSs)[0]

# new database
DATABASE = DATABASE[:, ItemsToBeRemained]

# new items
SingleItems = SingleItems[ItemsToBeRemained]


FREQUENTITEMSETS = []
SUPPORTS = []
fk = []

NumOfItems = DATABASE.shape[1]
NumOfTrs = DATABASE.shape[0]

# remained columns indices
ItemsetIndices = np.arange(0, NumOfItems)

# k=1

# ------------------------------------------------------------------------------
# first FK
for i in range(0, NumOfItems):
    itm = np.array([i])
    abssupp = CalcAbsSupp(itm, DATABASE)
    if abssupp >= minsupp:
        fk.append(itm)
        FREQUENTITEMSETS.append(itm)
        SUPPORTS.append(abssupp)

# print(fk)
# k=2
loop = 1

# actual work is done here
while loop:
    fkm1 = fk
    fk = []
    ck = CandidateGeneration(fkm1)
    # print(ck)
    for i in range(0, len(ck)):
        adayOgeseti = ck[i]
        abssupp = CalcAbsSupp(adayOgeseti, DATABASE)
        if abssupp >= minsupp:
            fk.append(adayOgeseti)
            FREQUENTITEMSETS.append(adayOgeseti)
            SUPPORTS.append(abssupp)
            #k += 1
    if len(ck)*len(fk) == 0:
        loop = 0

elapsed.toc()

# ------------------------------------------------------------------------------
# revers sort of supports
I = np.argsort(-np.array(SUPPORTS))

FREQUENTITEMSETS = [FREQUENTITEMSETS[i] for i in I]


SUPPORTS = [SUPPORTS[i] for i in I]
for i in range(0, len(FREQUENTITEMSETS)):
    itemset = FREQUENTITEMSETS[i]
    tmp = " "
    for j in itemset:
        tmp = tmp + SingleItems[j]
    print('#', i+1, tmp, 'Supp:', (SUPPORTS[i]*2)/10, ' => ', SUPPORTS[i])


with open('FIMresults', 'wb') as f:
    pickle.dump([FREQUENTITEMSETS, SUPPORTS, SingleItems, DATABASE], f)
