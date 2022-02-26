import numpy as np
from itertools import combinations
import pickle 

with open('FIMresults','rb') as f:
    FREQUENTITEMSETS, SUPPORTS, SingleItems, DATABASE = pickle.load(f)

try:
    from IPython import get_ipython
    get_ipython().magic('clear')
    get_ipython().magic('reset -f')
except:
    pass

def ShowDatabase(DATABASE,SingleItems):
    for i in range(0,DATABASE.shape[0]):
        tr = DATABASE[i,:]
        I = np.nonzero(tr>0)[0]
        itemset = ''
        for itm in SingleItems[I]:
            itemset = itemset + str(itm)
        print(i,':',itemset)
    return 

def FindIndex(itemset, FREQUENTITEMSETS):
    I = []
    for k in range(0,len(FREQUENTITEMSETS)):
        tmp = FREQUENTITEMSETS[k]
        if tmp.shape[0] == itemset.shape[0]:
            if all(itemset==tmp):
                I = k
                break 
    return I 

NumOfTransaction = DATABASE.shape[0]
SUPPORTS = [support/ NumOfTransaction for support in SUPPORTS]


MinKulc = 0.40
MinConf = 0.50


for itemset in FREQUENTITEMSETS:
    L = itemset.shape[0]
    if 1 < L:
        I = FindIndex(itemset, FREQUENTITEMSETS)
        SUPPORTitemset = SUPPORTS[I]
        for j in range(1, L):
            CBMN = list(combinations(np.arange(0, L), j))
            CBMN = np.matrix(CBMN)
            for k in range(0, len(CBMN)):
                PrefixIndex = np.array(CBMN[k, :])[0]
                tmp = np.ones(L, dtype='int8')
                tmp[PrefixIndex] = 0
                SuffixIndex = np.nonzero(tmp == 1)[0]
                Prefix = itemset[PrefixIndex]
                Suffix = itemset[SuffixIndex]

                tmpPrefix = ''
                for kk in range(0, np.size(Prefix)):
                    tmpPrefix = tmpPrefix + SingleItems[Prefix[kk]]

                tmpSuffix = ''
                for kk in range(0, np.size(Suffix)):
                    tmpSuffix = tmpSuffix + SingleItems[Suffix[kk]]

                I = FindIndex(Prefix, FREQUENTITEMSETS)
                SUPPORTPrefix = SUPPORTS[I]
                Confidence = SUPPORTitemset / SUPPORTPrefix

                I = FindIndex(Suffix, FREQUENTITEMSETS)
                SUPPORTSuffix = SUPPORTS[I]

                Kulc = 0.5 * (SUPPORTitemset / SUPPORTPrefix + SUPPORTitemset / SUPPORTSuffix)
                Kulc = 2 * (Kulc - 0.5)
                if MinKulc <= Kulc:
                    if MinConf <= Confidence:
                        print(tmpPrefix, '-->', tmpSuffix, '  supp.:' ,"{:.3f}".format(SUPPORTitemset), 'conf.:', "{:.3f}".format(Confidence), 'Kulc.:', "{:.3f}".format(Kulc))