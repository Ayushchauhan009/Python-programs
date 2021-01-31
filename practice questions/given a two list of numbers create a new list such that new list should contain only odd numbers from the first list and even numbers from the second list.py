def mergelist(listone,listtwo):
    print("first list:",listone)
    print("second list:",listtwo)
    thirdlist=[]
    for num in listone:
        if (num%2!=0):
            thirdlist.append(num)
    for num in listtwo:
        if (num%2==0):
            thirdlist.append(num)
    return thirdlist
listone=[10,11,22,32,35,65,71]
listtwo=[32,34,77,87,56,88]
print("resultant list is:",mergelist(listone,listtwo))