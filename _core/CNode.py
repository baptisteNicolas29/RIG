from maya import cmds


class CNode:

    @classmethod
    def generate(cls, *args, **kwargs):

        return cls(cmds.createNode(*args, **kwargs))

    def __init__(self, node: str) -> None:

        self.__node = node

    @property
    def node(self) -> str:

        return self.__node

    def remove(self) -> None:

        cmds.delete(self.__node)
        del self
