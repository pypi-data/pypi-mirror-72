import sys


def set_path():
    mymod = sys.modules['__main__']
    
    #print(getattr(mymod, 'PATH', ''))
    path = getattr(mymod, 'PATH', '')
    if path != "":
        mymod = mod(path)
        from pgzero.runner import my_mod
        my_mod(mymod)
class mod:
    def __init__(self,file):
        self.__file__ = file
        pass




