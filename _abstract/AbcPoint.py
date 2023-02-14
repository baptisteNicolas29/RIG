from abc import abstractproperty, ABC


class AbcPoint(ABC):

    @abstractproperty
    def matrix(self): pass

    @abstractproperty
    def data(self): pass

    @abstractproperty
    def item(self): pass
