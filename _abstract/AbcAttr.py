from abc import ABC, abstractclassmethod
import typing

from maya import cmds

from .._core import CNode


class AbcAttr(CNode.CNode, ABC):

    @abstractclassmethod
    def check(cls, node: str, attr: str) -> bool: pass

    @classmethod
    def generate(cls, node: CNode.CNode, **kwargs):

        cmds.addAttr(node.node, **kwargs)

        attr = kwargs.pop('shortName', None)
        attr = kwargs.pop('sn', attr)
        attr = kwargs.pop('longName', attr)
        attr = kwargs.pop('ln', attr)

        return cls(node.node, attr)

    def __init__(
            self, node: str, attr: int,
            index: typing.Optional[int] = None
            ) -> None:

        super().__init__(node)
        self.__attr = attr
        self.__index = index

    @property
    def attr(self) -> str:

        return self.__attr

    @property
    def item(self) -> str:

        if isinstance(self.__index, int):

            return f'{self.node}.{self.__attr}[{self.__index}]'

        return f'{self.node}.{self.attr}'

    def multi(self) -> bool:

        print(self.node, self.attr)
        return cmds.attributeQuery(self.attr, n=self.node, m=True)

    def remove(self) -> None:

        cmds.deleteAttr(self.node, at=self.attr)
        del self

    def __getitem__(self, v: int):

        if self.multi():

            return self.__class__(self.node, self.attr, v)

        else:

            raise NameError(f'{self.item} is not a multi attribute')

    def range(self, *args):

        for i in range(*args):

            yield self[i]
