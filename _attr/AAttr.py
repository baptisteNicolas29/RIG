from .._abstract import AbcAttr


class AAttr(AbcAttr.AbcAttr):
    '''
    test de documentation
    '''
    @classmethod
    def check(cls, node: str, attr: str) -> bool:

        return True
