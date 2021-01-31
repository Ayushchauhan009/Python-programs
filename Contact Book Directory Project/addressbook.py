try:
    import cPickle as pickle
except:
    import pickle
from hashlib import sha256

__author__ = 'Muhammad Arslan <rslnkrmt2552@gmail.com>'


class addressbook():
    """Class : Addressbook"""
    def __init__(self, name):
        try:
            self.__name = self.createName(name)+ '.db'
            self.__db = open(self.__name, 'rb')
            self.__entries = pickle.load(self.__db)
            self.__db.close()
        except:
            self.__db = open(self.__name, 'wb')
            self.__entries = {}
            self.__db.close()

    def __update(self):
        self.__db = open(self.__name, 'wb')
        pickle.dump(self.__entries, self.__db, -1)
        self.__db.close()

    def addEntry(self, contact):
        name = contact.getFirstName()
        if name in self.__entries:
            return '\nContact already present.\n'
        else:
            self.__entries[name] = contact
            self.__update()
            return '\nContact added successfully.\n'

    def removeEntry(self, name):
        if name in self.__entries:
            del self.__entries[name]
            self.__update()
            return '\nContact removed successfully.\n'
        else:
            return '\nName not found.\n'

    def searchEntry(self, name):
        name = name.lower()
        if name in self.__entries:
            return ('Contact found.', self.__entries[name])
        else:
            return ('Contact not found.', None)

    def updateEntry(self, name, param, val):
        name = name.lower()
        val = val.lower()

        if name in self.__entries:
            k = self.__entries[name]
            funcs = [k.setFirstName, k.setLastName, k.setName, k.setNumber, k.setEmail]
            funcs[param-1](val)
            return '\nContact updated successfully.\n'
        else:
            return '\nName not found.\n'

    @staticmethod
    def createName(mName):
        hsh = sha256(mName).hexdigest()
        return ''.join(hsh[1::3])