def loadSimpDat():
      simpDat = [['r', 'z', 'h', 'j', 'p'],
                 ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
                 ['z'],
                 ['r', 'x', 'n', 'o', 's'],
                 ['y', 'r', 'x', 'z', 'q', 't', 'p'],
                 ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]
      return simpDat
  
def createInitSet(dataSet):
     retDict = {}
     for trans in dataSet:
         fset = frozenset(trans)
         retDict.setdefault(fset, 0)
         retDict[fset] += 1
     return retDict
class treeNode:
     def __init__(self, nameValue, numOccur, parentNode):
         self.name = nameValue
         self.count = numOccur
         self.nodeLink = None
         self.parent = parentNode
         self.children = {}
 
     def inc(self, numOccur):
         self.count += numOccur
 
     def disp(self, ind=1):
         print('   ' * ind, self.name, ' ', self.count)
         for child in self.children.values():
             child.disp(ind + 1)
 
def createTree(dataSet, minSup=1):
     headerTable = {}
     #Buarada her bir veri öğesinin yolunu oluşturmak için veri kümesi dolaşılır
     for trans in dataSet:
         for item in trans:
             headerTable[item] = headerTable.get(item, 0) + 1
 
     #minimum support'a göre verileri filtleriyoruz
     lessThanMinsup = list(filter(lambda k:headerTable[k] < minSup, headerTable.keys()))
     for k in lessThanMinsup: del(headerTable[k])
 
     freqItemSet = set(headerTable.keys())
     #Eğer hiçbir veri minimum supporttu geçemiyorsa None , None yani boş dönüyoruz
     if len(freqItemSet) == 0:
         return None, None
 
     for k in headerTable:
         headerTable[k] = [headerTable[k], None]
 
     retTree = treeNode('φ', 1, None)
     #İkinci kez verisetini dolaşıyoruz ağacı oluşturmak için
     for tranSet, count in dataSet.items():
         localD = {}
         for item in tranSet:
             if item in freqItemSet:
                 localD[item] = headerTable[item][0] 
         if len(localD) > 0:
             orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p: (p[1],p[0]), reverse=True)]
             updateTree(orderedItems, retTree, headerTable, count)
     return retTree, headerTable
 
 
def updateTree(items, inTree, headerTable, count):
     if items[0] in inTree.children:  # buarada ağacın çocuğu olup olmadığına bakıyoruz varsa countu 1 artırıyoruz
         inTree.children[items[0]].inc(count)  # count 1 arttırılır
     else:  # yeni bir çocuk oluşturulur
         inTree.children[items[0]] = treeNode(items[0], count, inTree)
         if headerTable[items[0]][1] == None:  # update header table
             headerTable[items[0]][1] = inTree.children[items[0]]
         else:
             updateHeader(headerTable[items[0]][1], inTree.children[items[0]])
 
     if len(items) > 1:  # recursive çağrı ile bütün ağaca aynı işlemi uyguluyoruz
         updateTree(items[1:], inTree.children[items[0]], headerTable, count)
 
 
def updateHeader(nodeToTest, targetNode):  # burada recursive kullanmadan Header Tablosunu güncelliyoruz
     while (nodeToTest.nodeLink != None):  
         nodeToTest = nodeToTest.nodeLink
     nodeToTest.nodeLink = targetNode  
   
#Aşağıda yukarıda tanımladığımız datayı yüklüyoruz.     
simpDat = loadSimpDat()
#itemsetleri oluşturuyoruz
dictDat = createInitSet(simpDat)
#ağacı oluşturuyoruz
myFPTree,myheader = createTree(dictDat, 3)
myFPTree.disp()

def ascendTree(leafNode, prefixPath): #yapraktan köke giden yolu bulmamızı sağlayan fonksyion
    if leafNode.parent != None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent, prefixPath)

def findPrefixPath(basePat, treeNode): #hangi node'un nereden geldiğini anlamızı sağlayan fonksiyon
    condPats = {}
    while treeNode != None:
        prefixPath = []
        ascendTree(treeNode, prefixPath)
        if len(prefixPath) > 1: 
            condPats[frozenset(prefixPath[1:])] = treeNode.count
        treeNode = treeNode.nodeLink
    return condPats

findPrefixPath('r', myheader['r'][1])



