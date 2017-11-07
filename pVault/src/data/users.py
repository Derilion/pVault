from data.encoding import encryptior
from Crypto.Random import get_random_bytes
from data.persistence import Persistence
import time
import getpass


class UserList:
    """The Class for User handling"""

    # Dictionary containing value pairs: user/password in plain text
    __user = ""
    __hash = ""
    __salt = ""

    def __init__(self):
        """Here the old userlist (__list) can be loaded"""

        # print("User List Initialised")

    def __del__(self):
        result = Persistence.to_serial(self, "users.pvlt")
        if not result:
            print("Data could not be saved and is lost. Forever ....")

    def checkPW(self, user, password):
         """Checks user and password"""

         if user == self.__user:
             crypto = encryptior()
             testkey, _ = crypto.setAESfromPW(password, self.__salt)
             crypto.setAES(testkey)
             testpw = crypto.decryptAES(self.__hash)
             if testpw == password:
                 return True
             else:
                 crypto.setAES(0)
                 print("Wrong Password")
                 return False
         else:
             print("no such user")
             return False

    def addUser(self, user, password):
        """adds new users"""
        if user == self.__user:
            print("user already exists")
        else:
            self.__user = user

            crypto = encryptior()

            # create salt
            self.__salt = get_random_bytes(16)

            # save hash & salt
            tempkey, self.__salt = crypto.setAESfromPW(password)#, self.__salt)
            crypto.setAES(tempkey)
            self.__hash = crypto.encryptAES(password)

    def login(self):
        """handles login behaviour"""
        print("Please enter your username:")
        username = input()
        print("and password:")
        password = input()
        if not self.checkPW(username, password):
            time.sleep(0.5)
            self.login()

    def getUser(self):
        """getter method for program user name"""
        return self.__user
