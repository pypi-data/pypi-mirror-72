import os

from pathlib import Path
from mexp.manager import find
from jpfmanager.jpf import FileManager
from fdbm.structure.object_indexer import ObjectIndexer

class FDBManager(object):

    def __init__(self, path):      
        self.__listObjects = []
        self.__path = path
        self.indexFile = str((Path(path) / type(self).__name__).absolute()) + '.index'
        self.__filteredObjectsListWithPath = {}
        self.__filteredObjectsList = []

    @property
    def listObjects(self):
        """ Represent a list of indexing file
        Returns:
            list of type ObjectIndexer
        """
        if len(self.__listObjects) == 0:
            self.getFiles()
        return self.__listObjects

    def addElement(self, fileWithPath, classType, isLoaded):
        """ Add a list of indexing file
        Args:
            fileWithPath: full file path
            classType: type of instance
            isLoaded: is object loaded to the context
        Returns:
            bool of the state of the save operation
        """
        existedO = find(self.__listObjects, full_path = fileWithPath)
        if any(existedO):
            self.removeElement(existedO[0])
        self.__listObjects.append(ObjectIndexer(fileWithPath, classType, isLoaded))
        return self.save()

    def save(self):
        """ Save a list of indexing file
        Returns:
            bool of the state of the save operation
        """
        return FileManager.save(self.__listObjects, self.indexFile)

    def removeElement(self, element):
        """ Remove an element from indexing file list
        Args:
            element: indexing file element
        Returns:
            bool of the state of the save operation
        """
        if any(self.__listObjects):
            self.__listObjects.remove(element)
            return self.save()
            
    def removeElements(self, elementsList):
        """ Remove elements from indexing file list
        Args:
            elementsList: indexing file elements
        Returns:
            bool of the state of the save operation
        """
        if any(self.__listObjects):
            for element in elementsList:
                self.__listObjects.remove(elementsList)
            return self.save()

    def getFiles(self):
        """ Get elements from indexing file list
        Returns:
            indexing file list
        """
        if os.path.exists(self.indexFile):
            fileIndex = FileManager.get(self.indexFile)
            if fileIndex != None and fileIndex != False:
                self.__listObjects = fileIndex
    
    def getAllObjects(self, classType):
        """ Get all  elements from indexing file list
        Args:
            classType: type of instance
        """
        fdbObjectsFromIndexer = list(filter(lambda objectF: objectF.object_type == classType and objectF.is_loaded == False, self.listObjects))
        self.__partial_seach_is_used = False
        if fdbObjectsFromIndexer != None and any(fdbObjectsFromIndexer):
            for lightItem in fdbObjectsFromIndexer:
                fdbObject = FileManager.get(lightItem.full_path)
                self.__filteredObjectsListWithPath.update({lightItem.full_path:fdbObject})
                self.__filteredObjectsList.append(fdbObject)
                self.addElement(lightItem.full_path, classType, True)

    def find(self, type_of, **kwargs):
        """ Find any element that match properties values
        Args:
            type_of: type of instance
            kwargs: properties with values you want to use as filter
        Returns:
            A filtered list of objects that match any of the filter properties
        """        
        resultMapping = None
        self.getAllObjects(type_of.__name__)
        listToFilter = list(filter(lambda o: type(o) == type_of, self.__filteredObjectsList))
        resultMapping = find(listToFilter, **kwargs)
        return resultMapping

    def getAll(self, type_of):
        """ Get all elements from indexing file list of a specific type
        Args:
            type_of: type of instance
        Returns:
            A filtered list of all class objects
        """
        self.getAllObjects(type_of.__name__)
        return self.__filteredObjectsListWithPath

    def count(self, type_of):
        """ Count all elements of a specific type
        Args:
            type_of: type of instance
        Returns:
            Length of all elements of a specific type
        """
        return len([objectF for objectF in self.listObjects if objectF.object_type == type_of.__name__])
            
    def delete(self, target):
        """ Delete an element of a specific type
        Args:
            target: string target for path or provide the target instance class type
        Returns:
            bool of the state of the save operation
        """
        #string or object
        fdbObjectFromIndexer = None
        if type(target) is str:
            fileWithPath = os.path.join(self.__path, target)
        else:
            fileWithPath = self.findObjectPath(target)
        fdbObjectFromIndexer = next(o for o in self.listObjects if o.full_path == fileWithPath)
        result = FileManager.delete(fdbObjectFromIndexer.full_path)
        if result:
            self.removeElement(fdbObjectFromIndexer)
            o = self.__filteredObjectsListWithPath[fdbObjectFromIndexer.full_path]
            if o in self.__filteredObjectsList: self.__filteredObjectsList.remove(o)
            del self.__filteredObjectsListWithPath[fdbObjectFromIndexer.full_path]
            
        return result

    def deleteAll(self, type_of):
        """ Delete all elements of a specific type
        Args:
            type_of: type of instance
        Returns:
            bool of the state of the save operation
        """
        fdbObjectsFromIndexer = filter(lambda objectF: objectF.object_type == type_of.__name__, self.listObjects)
        result = False
        listOffdbObjects = list(fdbObjectsFromIndexer)
        for lightItem in listOffdbObjects:
            result = FileManager.delete(lightItem.full_path)
            if result:
                self.removeElement(lightItem)
                o = self.__filteredObjectsListWithPath[lightItem.full_path]
                if o in self.__filteredObjectsList: self.__filteredObjectsList.remove(o)
                del self.__filteredObjectsListWithPath[lightItem.full_path]
                
            else:
                raise Exception("some objects have not been deleted.")

        return result
        
    def get(self, fileName):
        """ Get target instance using its fileName
        Args:
            fileName: instance file name
        Returns:
            instance of the object from where it is saved in a file
        """
        fdbObjectFromIndexer = None
        try:
            fdbObjectFromIndexer = next(o for o in self.listObjects if o.full_path == os.path.join(self.__path, fileName))
        except StopIteration:
            pass
        fdbObject = None
        if fdbObjectFromIndexer != None:
            if not fdbObjectFromIndexer.is_loaded:
                fdbObject = FileManager.get(fdbObjectFromIndexer.full_path)
                self.__filteredObjectsListWithPath.update({fdbObjectFromIndexer.full_path:fdbObject})
                self.__filteredObjectsList.append(fdbObject)
                self.addElement(fdbObjectFromIndexer.full_path, type(fdbObject).__name__, True)
            else:
                try:
                    fdbObject = self.__filteredObjectsListWithPath[fdbObjectFromIndexer.full_path]
                except StopIteration:
                    pass
            pass
        if fdbObject == False:
            return None
        return fdbObject

    def findObjectPath(self, target):
        """ find path of an instance using its type
        Args:
            target: instance
        Returns:
            path sting
        """
        for oPath, obj in self.__filteredObjectsListWithPath.items():
            if obj == target:
                return oPath