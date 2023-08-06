* FDBM
* File data base system used to save/update/delete/find class objects to files easly.
* After you create your class you can do save, update, delete and find objects of that class instance without having to write code for these opertaions.


**Exemple:**

file `test_fdb.py`:
```
from pathlib import Path
from fdbm.model_base import FDBModel, FDBManager
from automotive_structure import Car, Engine


if __name__ == "__main__":
    
    #Set model path
    pathi = str((Path(__file__).parent).absolute())
    
    #Init model
    FDBModel.initialize(pathi)

    #Save class object
    myCar = Car('Peugeot', '504GL', 1970, 'Essence')
    myCar.saveNew()
    myCarObj = FDBModel.manager.find(type_of=Car, brand='Peugeot')

    #Save class object with subobject
    myEngine = Engine('Essence', 2.4, 'France')
    myCar = Car('Peugeot', '505GL', 1980, myEngine)
    myCar.saveNew()
    myCarObjList = FDBModel.manager.find(type_of=Car, brand='Peugeot')

    #Save class object with sub object with path arguemnt

    myEngine = Engine('Essence', 1.8, 'France')
    myCar = Car('Peugeot', '504GL', 1970, myEngine)
    myCar.saveNew('peugeot.pgt')
    myCarObjList = FDBModel.manager.get('peugeot.pgt')
      
    #Edit class object with sub object
    myCarObjList = FDBModel.manager.find(type_of=Car, brand='Peugeot')
    myCarObjList[2].model = '305'
    #sub object modification
    myCarObjList[2].engine.size = 1.6
    myCarObjList[2].update()

    myCarObjList = FDBModel.manager.find(type_of=Car, brand='Peugeot')

    #Delete one speicifc object
    isDeleted = FDBModel.manager.delete(myCarObjList[2])

    #List will have only two element
    myCarObjList = FDBModel.manager.find(type_of=Car, brand='Peugeot')

    #Delete all objects of type Car
    isDeleted = FDBModel.manager.deleteAll(type_of=Car)

    #List will have Zero element
    myCarObjList = FDBModel.manager.find(type_of=Car, brand='Peugeot')

    print('Done!')
```

File `automotive_structure.py`
```
from fdbm.fdb_base import FDBase
class Car(FDBase):
    
    def __init__(self, brand, model, year, engine):
        self.brand = brand
        self.model = model
        self.year = year
        self.engine = engine

class Engine(FDBase):
    
    def __init__(self, type, size, origine):
        self.type = type
        self.size = size
        self.origine = origine
```

[**FDBM repo**](https://github.com/IbrahimABBAS85/fdb)