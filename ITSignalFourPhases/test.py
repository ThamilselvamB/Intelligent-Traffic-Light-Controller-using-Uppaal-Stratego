import pandas as pd
data = pd.read_csv("Data2.txt",delimiter='\t')
# print(data.keys())
# print(data[data['geo']<6])
# print("compare:",data['dat'].values.tolist().split)

def distictNumberCheking(list2):
    lst3 = []
    lst3 = list(set(list2))
    return len(lst3)

# def disCheck(list3):
#     count = 0
#     for i in range(len(list3):
#         for k in list3:


listDate = data.values.tolist()
print("list here:",listDate)
# print(listDate[0][3].split(':'))
newList = []
count = 0
for i in range(len(listDate)):
    # if int(listDate[i][3].split(':')[1]) == 5:
    if int(listDate[i][4]) == 7:
        newList.append(listDate[i])
        # print("Here:",listDate[i])
        count = count +1
tuple=0
distNewList = []
for i in range(len(newList)):
    distNewList.append(newList[i][tuple])
# print("distNewlist:",distNewList)
print("final count:",count)
# print("new list:",newList)
print("distinct number:",distictNumberCheking(distNewList) )
# print("distinct number:",distictNumberCheking(newList[2])) )

# print(data['dat'])
# compare = int(listDate[0].split(':')[1])
# if compare == 12:
#     print("Compare",compare)
# print("list",listDate[0].split(':'))