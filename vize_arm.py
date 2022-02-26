

# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 14:27:10 2021

@author: Mustafa
"""

import pickle
import numpy as np
from itertools import combinations

with open('FIMresults', 'rb') as f:
    frequentItemsets, Supports, SingleItems, database = pickle.load(f)

# -----------------------------------------------------------------------------


def ShowDatabase(database, SingleItems):
    for i in range(database.shape[0]):
        tr = database[i, :]
        I = np.nonzero(tr > 0)[0]
        print(i, ':', SingleItems[I])
    return

# -----------------------------------------------------------------------------


def FindIndex(itemset, frequentItemsets):
    I = []
    for k in range(0, len(frequentItemsets)):
        tmp = frequentItemsets[k]
        print('tmp:', tmp, ' - tmp.shape:',
              tmp.shape[0], '- itemset:', itemset, ' - itemset.shape', itemset.shape[0])
        if tmp.shape[0] == itemset.shape[0]:

            if all(itemset == tmp):
                I = k
                break
    return I


# -----------------------------------------------------------------------------
NumOfTrans = database.shape[0]
Supports = [support / NumOfTrans for support in Supports]

ShowDatabase(database, SingleItems)

minConf = 0.95
minKulc = 0.5

cnt = 0
for itemset in frequentItemsets:
    L = itemset.shape[0]
    print('########################################################################################')
    print('########################################', cnt,
          '############################################')
    cnt += 1
    print('L: ', L, ' - itemset:', itemset)
    if 1 < L:
        # find itemset index in supports
        I = FindIndex(itemset, frequentItemsets)
        suppItemset = Supports[I]

        for j in range(1, L):
            # np.arange(0,L) 0 dan L ye kadar olan sayılar
            # combinations(np.arange(0,L), j) 0 dan L ye kadar olan sayıların j li kombinasyonu
            cmbn = list(combinations(np.arange(0, L), j))
            print('list cmbn', cmbn)

            cmbn = np.matrix(cmbn)

            print('matrix cmbn:\n', cmbn)
            for k in range(0, len(cmbn)):

                # öncül indis
                premiseIndex = np.array(cmbn[k, :])[0]

                tmp = np.ones(L, dtype='int8')
                tmp[premiseIndex] = 0

                # ardıl indis
                consequentIndex = np.nonzero(tmp != 0)[0]

                # öncül
                premise = itemset[premiseIndex]

                # ardıl
                consequent = itemset[consequentIndex]

                print(
                    '-----------------------------------START[', k, ']-------------------------------------------')
                print('premiseIndex:', premiseIndex, ' - premise: ', premise, ' - consequentIndex: ',
                      consequentIndex, ' - consequent: ', consequent, '\ncbmn:\n', cmbn, '\ntmp: ', tmp)

                tmpPremise = ''
                for kk in range(0, np.size(premise)):
                    tmpPremise = tmpPremise + SingleItems[premise[kk]]

                tmpConsequent = ''
                for kk in range(0, np.size(consequent)):
                    tmpConsequent = tmpConsequent + \
                        SingleItems[consequent[kk]]

                print(tmpPremise, ' => ', tmpConsequent)

                I = FindIndex(premise, frequentItemsets)
                suppPremise = Supports[I]
                conf = suppItemset / suppPremise

                I = FindIndex(consequent, frequentItemsets)
                suppConsequent = Supports[I]

                kulc = 0.5 * (suppItemset/suppPremise +
                              suppItemset/suppConsequent)
                kulc = 2 * (kulc - 0.5)

                inte = abs(suppItemset-(suppPremise*suppConsequent))
                print('kulc:', kulc, ' - min kulc:',
                      minKulc, '- inte: ', inte)

                if minKulc <= kulc:
                    if minConf <= conf:
                        print(tmpPremise, "-->", tmpConsequent, '- inte: ', inte,
                              "Conf:", conf, "Kulc:", kulc, 'absSupp:', (suppItemset/suppPremise + suppItemset/suppConsequent), ' => ', suppItemset, '/', suppPremise, '+', suppItemset, '/', suppConsequent)
                print(
                    '--------------------------------------END-----------------------------------------------')
