__author__ = 'Muhammad Arslan <rslnkrmt2552@gmail.com>'

class Contact(object):
    """Initialize a new contact object.
    Takes in name and phone number. Other arguments are optional."""
    def __init__(self, firstname, lastname, pNumber, email = ''):
        super(Contact, self).in__init__()
        self.__firstName = firstname.lower()
        self.__lastName = lastname.lower()
        self.__pNumber = pNumber
        self.__email = email

    def __str__(self):
        return self.getName() + '\t' + self.getNumber()

    def __eq__(self , other):
        return (self.getName() == other.getName()) or (self.getNumber() == other.getNumber())

    def getName(self):
        return self.__firstName[0].upper()+self.__firstName[1:] + ' ' + self.__lastName[0].upper() + self.__lastName[1:]

    def getFirstName(self):
        return self.__firstName

    def getLastName(self):
        return self.__lastName

    def getNumber(self):
        return self.__pNumber

    def getEmail(self):
        return self.__email

    def setFirstName(self, newFName):
        self.__firstName = newFName

    def setLastName(self, newLName):
        self.__lastName = newLName

    def setName(self, fullName):
        self.__firstName, self.__lastName = fullName.split(' ')

    def setNumber(self, newNumber):
        self.__pNumber = newNumber

    def setEmail(self, newEmail):
        self.__email = newEmail