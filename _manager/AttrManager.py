from maya import cmds

from .._core import CNode


class AttrManager(CNode.CNode):

    __MANAGED = []

    @classmethod
    def append_managed(cls, value):

        if value not in cls.__MANAGED:
            cls.__MANAGED.insert(0, value)

    def __init__(self, node) -> None:

        if isinstance(node, CNode.CNode):
            node_base = node.node

        if isinstance(node, str):
            node_base = node

        super().__init__(node_base)

    def __len__(self) -> int:

        list_attr = cmds.listAttr(self.node, ud=True)
        list_attr = list(filter(lambda x: '.' not in x, list_attr))
        return len(list_attr)

    def __getitem__(self, value: str):

        for typ in self.__MANAGED:
            if typ.check(self.node, value):
                return typ(self.node, value)

    def __iter__(self):

        list_attr = cmds.listAttr(self.node, ud=True)
        list_attr = list(filter(lambda x: '.' not in x, list_attr))

        for a in list_attr:
            yield self[a]
