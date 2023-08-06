import os
import operator
from jpfmanager.jpf import FileManager
from mexp.manager import find
from fdbm.model_base import FDBModel

class FDBase(object):

    def __init__(self):
        self.__fileWithPath = None
        self.isInitialized = True
   
    def saveNew(self, name = None):
        """ Save instance of object to a file
        Args:
            name: if provided, a name to the file where the object will be saved            
        Returns:
            bool of the state of the save operation
        """
        is_saved = False
        if name == None:
            name =  type(self).__name__ + '_' + str(FDBModel.manager.count(type(self)))
        self.__fileWithPath = os.path.join(FDBModel.path, name)
        if os.path.exists(self.__fileWithPath):
            raise Exception("The file you want to save exists, please delete it or change its name then save again.")        
        is_saved  = FileManager.save(self, self.__fileWithPath)
        is_saved = is_saved and FDBModel.manager.addElement(self.__fileWithPath, type(self).__name__, False)
        return is_saved

    def update(self):
        """ Save instance of object and save the modification to the corresponding file             
        Returns:
            bool of the state of the save operation
        """
        return FileManager.save(self, FDBModel.manager.findObjectPath(self))