from maya import cmds

from .._core import CNode
from .. import Settings


class PartManager(CNode.CNode):

    def __init__(self, node) -> None:

        if isinstance(node, CNode.CNode):

            node_base = node.node

        if isinstance(node, str):

            node_base = node

        super().__init__(node_base)

    def __len__(self) -> int:

        return len(cmds.listRelatives(self.node, c=True))

    def __getitem__(self, value: str):

        for typ in Settings.Settings.part():

            if typ.check(self.node, value):

                return typ(self.node, value)

    def __iter__(self):

        for name in cmds.listRelatives(self.node):

            yield self[name]
