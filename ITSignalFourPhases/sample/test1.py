# Load the Pandas libraries with alias 'pd'
import pandas as pd
# Read data from file 'filename.csv'
# (in the same directory that your python process is based)
# Control delimiters, rows, column names with read_csv (see later)


def rangeChaneking(list1,num1,num2):
    count = 0
    for i in list1:
        if i in range(num1,num2+1):
            count = count +1

    return count

def distictNumberCheking(list2):
    lst3 = []
    lst3 = list(set(list2))
    return len(lst3)

data = pd.read_csv("Data1.txt",delimiter='   ')
# Preview the first 5 lines of the loaded data
print(data.keys())
# print(data['IPAdd'])
lst22 = data.values.tolist()
print("output:",lst22)
# lst22 = []
lst2 =[]
for i in range(len(lst22)):
    lst2.append(lst22[i][0])
print("list output:",lst2)
list2 = []
for k in lst2:
    list2.append(k.split('\t'))
print("Final list",list2[1][3])
tuple = 2
tuple2 = 3
finalList = []
for ii in range(len(list2)):
    # finalList.append(int(list2[ii][tuple]))
    finalList.append([int(list2[ii][tuple]),(list2[ii][tuple2])])


print("Required Out:",finalList[0][1].split(':')[1])
# print("rangeValue",rangeChaneking(finalList,77,77))
# print("Distinct Number:", distictNumberCheking(finalList))

# print(lst22[0][0])
# print("list of IP",len(lst2))
# lst3 = list(set(lst2))
# print("distinct Ip Address:",len(lst3))

# print("rangeValue",rangeChaneking(lst2,60,99))


# print(rangeChaneking([4,2,2,3,4,5,6],2,5))