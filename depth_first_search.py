import numpy as np

# -------------------------------------
try:
    from IPython import get_ipython

    get_ipython().magic('clear')
    get_ipython().magic('reset -f')
except:
    pass
# -------------------------------------
#       VARIABLES
# -------------------------------------

SingleItems = np.array(["A","B","C","D","E"])

# ---------------------------------------------------
def DFS_LOOP(itm, NumOfItems, ITEMSETS):
    tmp = itm[-1]
    for itx in range(tmp + 1 , NumOfItems):
        NewItem = np.hstack((itm, itx))
        ITEMSETS.append(SingleItems[NewItem])
        # print('itm:',itm,'tmp:',tmp,'itx:',itx,'NewItem:',NewItem,'itemsets:', ITEMSETS[-1])
        print('itemsets:', ITEMSETS[-1])
        (ITEMSETS) = DFS_LOOP(NewItem, NumOfItems, ITEMSETS)
    return ITEMSETS
# ---------------------------------------------------

NumOfItems = SingleItems.shape[0]
ITEMSETS = []

for itm in range(0, NumOfItems):
    itm = np.array([itm])
    ITEMSETS.append(SingleItems[itm])
    print('itemsets:', ITEMSETS[-1])
    (ITEMSETS) = DFS_LOOP(itm, NumOfItems, ITEMSETS)