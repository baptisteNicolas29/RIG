from maya import cmds

from .._core import CNode


class PartManager(CNode.CNode):

    __MANAGED = []

    @classmethod
    def append_managed(cls, value):

        if value not in cls.__MANAGED:
            cls.__MANAGED.insert(0, value)

    @classmethod
    def get(cls, node: str):

        for typ in cls.__MANAGED:
            if typ.check(node):
                return typ(node)

    def __init__(self, node) -> None:

        if isinstance(node, CNode.CNode):
            node_base = node.node

        if isinstance(node, str):
            node_base = node

        super().__init__(node_base)

    def __len__(self) -> int:

        return len(cmds.listRelatives(self.node, ad=True))

    def __getitem__(self, value: str):

        if value not in cmds.listRelatives(self.node, ad=True):
            raise NameError(f'{value} is not a child of {self.node}')

        for typ in self.__MANAGED:
            if typ.check(value):
                return typ(value)

    def __iter__(self):

        for name in cmds.listRelatives(self.node):
            yield self[name]
