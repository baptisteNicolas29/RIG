from maya import cmds

from .._core import CNode
from .. import Settings


class PartManager(CNode.CNode):

    def __len__(self) -> int:

        return len(cmds.listRelatives(self.node, c=True))

    def __getitem__(self, value: str):

        for typ in Settings.Settings.part():

            if typ.check(self.node, value):

                return typ(self.node, value)

    def __iter__(self):

        for name in cmds.listRelatives(self.node):

            yield self[name]
