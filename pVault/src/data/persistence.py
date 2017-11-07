import pickle


class Persistence:
    """offers static methods to import and export keychain information"""

    @staticmethod
    def to_serial(content, path):
        """converts any object to a serial representation, encrypts if needed"""
        try:
            handle = open(path, "wb")
        except IOError:
            return False

        pickle.dump(content, handle)
        return True

    @staticmethod
    def from_serial(path):
        """converts a serial object to the source object, decrypts if needed"""
        try:
            handle = open(path, "rb")
        except IOError:
            return False

        content = pickle.load(handle)
        return content


