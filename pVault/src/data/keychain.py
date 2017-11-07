from difflib import SequenceMatcher
from data.encoding import encryptior

class KeyChain:

    startElement = 0
    length = 0
    matchquality = 0.4

    def __init__(self):
        """nothing"""
        # self.append("entry 1", "12", "123")
        # self.append("ag", "adfga", "afdgda")

    def append(self, name, login, password):
        """appends an element to the end of the list"""
        enigma = encryptior()
        name = enigma.encryptAES(name)
        login = enigma.encryptAES(login)
        password = enigma.encryptAES(password)
        if self.startElement == 0:
            self.startElement = KeyChainElement(0, name, login, password)
            self.length = self.length + 1
        else:
            listElement = self.startElement
            while listElement.nextElement:
                listElement = listElement.nextElement
            listElement.nextElement = KeyChainElement(listElement, name, login, password)
            self.length = self.length + 1
            # todo: check if name already exists

    def _privateappend(self, encryptedname, encryptedlogin, encryptedpassword):
        if self.startElement == 0:
            self.startElement = KeyChainElement(0, encryptedname, encryptedlogin, encryptedpassword)
            self.length = self.length + 1
        else:
            listElement = self.startElement
            while listElement.nextElement:
                listElement = listElement.nextElement
            listElement.nextElement = KeyChainElement(listElement, encryptedname, encryptedlogin, encryptedpassword)
            self.length = self.length + 1

    def remove(self, name):
        """removes a specified element"""

        # find the element
        element = self.startElement
        while element.nextElement and element.name != name:
            element = element.nextElement

        if self.startElement == element:
            self.startElement = self.startElement.nextElement
            self.startElement.lastElement = 0
            del element

        elif not element.nextElement:
            if element.name == name:
                element.lastElement.nextElement = 0
                del element
            else:
                print("The system has encountered an error. Account not found")
                return False

        else:
            element.lastElement.nextElement = element.nextElement
            element.nextElement.lastElement = element.lastElement
            del element

        return True

    def find(self, text):
        """returns a list of found elements"""

        element = self.startElement
        resultlist = KeyChain()

        enigma = encryptior()

        # search for a match better than a certain quota
        while element:
            if SequenceMatcher(None, text, enigma.decryptAES(element.name)).ratio() > self.matchquality:
                print(enigma.decryptAES(element.name))
                resultlist._privateappend(element.name, element.login, element.password)

            element = element.nextElement

        return resultlist

    def findElementByID(self, number):
        """finds an elment by ID"""
        if (number <= self.length) and (number >= 0):
            i = 0
            element = self.startElement
            while number > i:
                element = element.nextElement
                i = i+1
            return element
        else:
            return False

    def list(self):
        """lists all existing elements within the keychain"""

        enigma = encryptior()

        iterator = 0
        listElement = self.startElement
        while listElement:
            print(iterator, ": ", enigma.decryptAES(listElement.name), sep='')
            iterator = iterator + 1
            listElement = listElement.nextElement


class KeyChainElement:
    """describes a single element of a keychain which represents one login"""
    lastElement = 0
    nextElement = 0
    name = 0
    login = 0
    password = 0

    def __init__(self, lastElement, name, login, password):
        """Constructor"""

        self.lastElement = lastElement
        self.name = name
        self.login = login
        self.password = password







