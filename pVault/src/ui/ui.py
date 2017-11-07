from data.users import UserList
from data.keychain import KeyChain
from data.encoding import encryptior
from subprocess import call
from data.persistence import Persistence
import os
import time


class CmdUI:

    __chain = 0
    __userobj = 0
    __mainmenu = ["Show all Accounts", "Find Accounts", "Add an Account", "Exit"]

    def __init__(self):
        """initialise all contents for ui handling"""

        os.system('cls')

        # init variables
        self.__userobj = Persistence.from_serial("users.pvlt")
        if self.__userobj:
            self.__userobj.login()
        else:
            self.__userobj = UserList()
            self.initUser()

        user = self.__userobj.getUser()
        self.__chain = Persistence.from_serial(user+"chain.pvlt")

        if not self.__chain:
            self.__chain = KeyChain()

        self.mainMenu()

    def __del__(self):
        """destructor for ui object, saves keychain as a file when program ends"""

        user = self.__userobj.getUser()
        result = Persistence.to_serial(self.__chain, user+"chain.pvlt")
        if not result:
            print("Data could not be saved and is lost. Forever ....")
        else:
            print("saved")

    def mainMenu(self):
        """main menu with all options"""
        i = 0

        os.system('cls')
        print("\npVault by Max\n")
        for item in self.__mainmenu:
            print(i, ": \t", item, sep='')
            i = i+1
        selection = input()

        if selection == "0":
            self.accountsMenu()
        elif selection == "1":
            self.findMenu()
        elif selection == "2":
            self.addEntryMenu()
        elif selection == "3":
            #print("Are you sure? y/n")
            print("notice me senpai")
            time.sleep(0.2)
            os.system('cls')
            return True
        else:
            print("menu does not exist")
        self.mainMenu()

    def accountsMenu(self):
        """Shows Accounts"""

        os.system('cls')
        print("Account Menu\n")
        self.__chain.list()
        print("\n")
        user = input()

        if user == "..":
            return True
        elif self.__toint(user):
            user = int(user)
            print("selected element", user)
            a = self.__chain.findElementByID(user)
            self.detailViewMenu(a)
            self.accountsMenu()
            return True
        else:
            print('nothing selected')
        self.accountsMenu()
        return True

    def findMenu(self, search=0):
        """finds keychain entries"""

        if search == 0:
            os.system('cls')
            print("Find Menu\n")
            print("enter a filter:")
            search = input()

        os.system('cls')
        print("Find Menu\nSearching: ", search, "\n")

        tempchain = self.__chain.find(search)

        if tempchain.length != 0:
            tempchain.list()
            print("\n")
            user = input()
            if user == "..":
                return True
            elif self.__toint(user):
                user = int(user)
                # print("selected element", user)
                a = tempchain.findElementByID(user)
                self.detailViewMenu(a, tempchain)
            else:
                print('nothing selected')
        else:
            print("Nothing Found")
            self.findMenu()
            return True
        self.findMenu(search)
        return True

    def addEntryMenu(self):
        """add keychain entry"""
        print("add menu\n")
        print("Please enter a name")
        name = input()
        if name == "..":
            return True

        print("Please enter the login")
        login = input()
        if login == "..":
            return True

        print("Please enter the password")
        password = input()
        if password == "..":
            return True

        self.__chain.append(name, login, password)

        print("Account Information for", name, "was added to the pVault")

        return True

    def detailViewMenu(self, element, tempchain=False):
        """Displays a single menu option with password"""

        enigma = encryptior()

        os.system('cls')
        print("\nAccount Details\n")
        print("Details:\t\t", enigma.decryptAES(element.name), "\nLogin:\t\t\t", enigma.decryptAES(element.login), "\t\t\tPassword:\t", enigma.decryptAES(element.password), sep='')
        user = input()
        if user == "..":
            return True
        elif user == "help":
            # call help menu
            print('')
        elif user == "cp":
            clipstring = enigma.decryptAES(element.password)
            call("echo " + clipstring + "| clip", shell=True)
        elif user == "del":
            self.__chain.remove(element.name)
            if tempchain:
                tempchain.remove(element.name)
            return True
        else:
            print("does not exist")
        self.detailViewMenu(element)
        return True

    def initUser(self):
        """Handles if there was no user, ever."""
        os.system('cls')
        password = ""
        print("\npVault by Max\n")
        print("Since this is your first session, please enter a new user name:")
        user = input()

        while password == "":
            print("Please enter your password:")
            pw1 = input()
            print("Please confirm your password:")
            pw2 = input()
            if pw1 == pw2:
                password = pw1
            else:
                print("passwords not identical, please try again")
        self.__userobj.addUser(user, password)
        return True

    def __toint(self, str):
        """utility to return an int if value is an int"""
        try:
            int(str)
            return True
        except ValueError:
            return False
