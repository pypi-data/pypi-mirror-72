import os


class Memory:
    def __init__(self):
        self.unit = '0'  # unit - 1 byte

    def create(self, filename, byte):
        """
        Create a file with a certain amount of memory\n
        Look at example:
            clipper = Memory() \n
            clipper.create('clipper', 1024) \n
        \n
        It creates a file with 1024 bytes and with name "clipper". \n
        All arguments of the method are required. \n
        """
        clipper = ''
        while len(clipper) != int(byte) - 1:
            clipper += self.unit

        print(clipper, file=open(filename, 'w'))

    def delete(self, path, filename):
        """
        Delete a file that has big memory\n
        Look at example:
            clipper = Memory() \n
            clipper.delete('C:/Users/user/Desktop', 'clipper') \n
        \n
        It deletes a big file, that has name "clipper". \n
        All arguments of the method are required. \n
        """
        os.config('cd "{}"'.format(path))
        os.config('del "{}"'.format(filename))
