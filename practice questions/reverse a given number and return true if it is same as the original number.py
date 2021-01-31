'''def number(num):
    print("original number:", num)
    originalnum=num    
    reversenum=0
    while(originalnum > 0):
        reminder=originalnum%10
        reversenum=(reversenum*10)+reminder
        originalnum=originalnum//10
        if originalnum==reversenum:
            return True
print("The original and the reverse number is the same:", number(111))'''
def reverseCheck(number):
    print("original number", number)
    originalNum = number
    reverseNum = 0
    while (number > 0):
        reminder = number % 10
        reverseNum = (reverseNum * 10) + reminder
        number = number // 10
    if (originalNum == reverseNum):
        return True
    else:
        return False

print("The original and reverse number is the same:", reverseCheck(121))
 