from fdbm.fdb_manager import FDBManager

class FDBModel(object):
    path = ''
    manager = None

    @staticmethod
    def initialize(pathi):
        FDBModel.path = pathi
        FDBModel.manager = FDBManager(pathi)