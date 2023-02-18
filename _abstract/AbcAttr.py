import re

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

    @classmethod
    def from_string(cls, attr_string: str):

        node = attr_string.split('.')[0]
        full_attr = '.'.join(attr_string.split('.')[1:])
        idx_match = re.search(r'\[([0-9]+)\]$', full_attr)

        if idx_match:
            attr = full_attr.rstrip(idx_match.group(0))
            idx = int(idx_match.group(1))
            return cls(node, attr, idx)

        else:
            return cls(node, full_attr)

    def __init__(
            self, node: str, attr: int,
            index: typing.Optional[int] = None
            ) -> None:

        super().__init__(node)
        self.__attr = attr
        self.__index = index

    @property
    def name(self):

        return self.__attr

    @property
    def attr(self) -> str:

        if isinstance(self.__index, int):
            return f'{self.__attr}[{self.__index}]'

        return self.__attr

    @property
    def item(self) -> str:

        return f'{self.node}.{self.attr}'

    def multi(self) -> bool:

        return cmds.attributeQuery(self.name, n=self.node, m=True)

    def remove(self) -> None:

        cmds.deleteAttr(self.node, at=self.name)
        del self

    def __getitem__(self, v: int):

        if self.multi():

            return self.__class__(self.node, self.name, v)

        else:

            raise NameError(f'{self.item} is not a multi attribute')

    def __len__(self) -> int:

        conn = cmds.listConnections(self.item, s=True, d=True, c=True) or []

        if not conn:
            return 0

        conn = [c for i, c in enumerate(conn) if i % 2 == 0]
        ids = [re.search(r"\[([0-9]+)\]", c).group(1) for c in conn]
        return max([int(i) for i in ids]) + 1

    def range(self, *args):

        for i in range(*args):

            yield self[i]
